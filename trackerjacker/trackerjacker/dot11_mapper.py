#!/usr/bin/env python3
# pylint: disable=C0103, C0111, W0703, C0413, R0902

import time
import copy
import threading
import collections
from functools import reduce
from datetime import datetime
import redis

import pyaml
import ruamel.yaml
from . import dot11_frame  # pylint: disable=E0401
from . import ieee_mac_vendor_db  # pylint: disable=E0401
from .common import MACS_TO_IGNORE


def trim_frames_to_window(frames, window, now=None):
    if not now:
        now = time.time()
    oldest_time_in_window = now - window
    oldest_in_window = -1  # Assume everything is in the window
    for index, frame in enumerate(frames):
        if frame[0] >= oldest_time_in_window:
            oldest_in_window = index
            break
    return frames[oldest_in_window:]


class Dot11Map:
    """Represents the observed state of the 802.11 radio space."""

    def __init__(self, remove_unseen_devices=False):
        # Used for determining when to trim frame lists
        self.frame_count_by_device = collections.Counter()
        self.trim_every_num_frames = 50  # empirically-derived
        self.device_fall_off_window = 60 * 5 # 5 Minute
        self.remove_unseen_devices = remove_unseen_devices
        self.window = 10  # seconds

        self.redis_live = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.db_history = redis.StrictRedis(host='localhost', port=6379, db=0)

        self.lock = threading.RLock()

        # Needed for efficiently determining if there is no ssid known for a given bssid
        self.bssids_associated_with_ssids = set()

        # 'linksys' -> {'90:35:ab:1c:25:19', '80:81:a6:f5:29:22'}
        self.ssid_to_access_point = {}

        self.access_points = {}
        self.devices = {}

        self.mac_vendor_db = ieee_mac_vendor_db.MacVendorDB()

    def add_frame(self, frame):
        with self.lock:
            # Update Access Point data
            if frame.bssid:
                self.update_access_point(frame.bssid, frame)

            # Update Device data
            for mac in frame.macs - {frame.bssid}:
                self.update_device(mac, frame)

            # Enrich the frame by adding the ssid if not already there and if we know it
            if not frame.ssid and frame.bssid in self.access_points:
                ssid = self.access_points[frame.bssid].get('ssid', None)
                if ssid:
                    frame.ssid = ssid

        # TODO: Make sure beacons add 1 to frame counts (so that if looking for a threshold of 1 bytes they show up)

    def get_dev_node(self, mac):
        """Returns ap_node associated with mac in a thread-safe manner."""
        device_node = None
        with self.lock:
            if mac in self.devices:
                device_node = copy.deepcopy(self.devices[mac])
            return device_node

    def get_ap_by_bssid(self, bssid):
        """Returns ap_node associated with mac in a thread-safe manner."""
        ap_node = None
        with self.lock:
            if bssid in self.access_points:
                ap_node = copy.deepcopy(self.access_points[bssid])
            return ap_node

    def get_ap_nodes_by_ssid(self, ssid):
        ap_nodes = None
        with self.lock:
            if ssid in self.ssid_to_access_point:
                ap_bssid_list = self.ssid_to_access_point[ssid]
                ap_nodes = [self.get_ap_by_bssid(bssid) for bssid in ap_bssid_list]
            return ap_nodes

    def get_channels_by_mac(self, mac):
        dev_node = self.get_dev_node(mac)
        return dev_node.get('channels', ()) if dev_node else ()

    def get_channels_by_bssid(self, bssid):
        ap_node = self.get_ap_by_bssid(bssid)
        return ap_node.get('channels', ()) if ap_node else ()

    def get_channels_by_ssid(self, ssid):
        ap_nodes = self.get_ap_nodes_by_ssid(ssid)
        return reduce(lambda acc, ap_chans: acc+ap_chans, [ap.get('channels', ()) for ap in ap_nodes], [])

    def update_access_point(self, bssid, frame):
        if bssid in MACS_TO_IGNORE:
            return

        if bssid not in self.access_points:
            ap_node = {'bssid': bssid,
                       'ssid': frame.ssid,
                       'vendor': self.mac_vendor_db.lookup(bssid),
                       'channels': {frame.channel},
                       'frames': []}
            self.access_points[bssid] = ap_node

        else:
            ap_node = self.access_points[frame.bssid]

        # Associate with ssid if ssid available
        if frame.ssid:
            if frame.ssid in self.ssid_to_access_point:
                self.ssid_to_access_point[frame.ssid] |= {bssid}
            else:
                self.ssid_to_access_point[frame.ssid] = {bssid}

            self.bssids_associated_with_ssids |= {bssid}

            # Make sure we didn't previously categorize this as an unknown_ssid
            missing_ssid_name = 'unknown_ssid_{}'.format(bssid)
            if missing_ssid_name in self.ssid_to_access_point:
                self.ssid_to_access_point[frame.ssid] |= self.ssid_to_access_point.pop(missing_ssid_name)
        elif bssid not in self.bssids_associated_with_ssids:
            # If no ssid is known, use the ssid name "unknown_ssid_80:21:46:af:28:66"
            missing_ssid_name = 'unknown_ssid_{}'.format(bssid)
            if missing_ssid_name in self.ssid_to_access_point:
                self.ssid_to_access_point[missing_ssid_name] |= {bssid}
            else:
                self.ssid_to_access_point[missing_ssid_name] = {bssid}

        if frame.signal_strength:
            ap_node['signal'] = frame.signal_strength

        # Only associate with channels and devices for data packets since, for example, APs
        # send beacons on channels that they don't actually communicate on.
        if frame.frame_type() == dot11_frame.Dot11Frame.DOT11_FRAME_TYPE_DATA:
            ap_node['channels'] |= {frame.channel}

        # Trim old frames (those that are older than window)
        self.frame_count_by_device[bssid] += 1
        if self.frame_count_by_device[bssid] % self.trim_every_num_frames == 0:
            ap_node['frames'] = trim_frames_to_window(ap_node['frames'], self.window)

        ap_node_redis = copy.deepcopy(ap_node)
        ap_node_redis['channels'] = str(ap_node_redis['channels'])
        ap_node_redis['frames'] = str(ap_node_redis['frames'])
        ap_node_redis['ssid'] = str(ap_node_redis['ssid'])

        try:
            self.redis_live.hmset(f"ap:{bssid}", ap_node_redis)
        except Exception as ex:
            print("Error:", ex, flush=True)
            print('AP not valid', ap_node_redis, flush=True)

    def update_device(self, mac, frame):
        if mac in MACS_TO_IGNORE:
            return

        if mac not in self.devices:
            dev_node = {'mac': mac,
                        'vendor': self.mac_vendor_db.lookup(mac),
                        'signal': frame.signal_strength,
                        'last_seen': time.time(),
                        'channel': frame.channel,
                        'frames_in': [],
                        'frames_out': [],
                        'time': datetime.now().strftime("%H:%M:%S %d/%m/%Y"),
                        'bssid': frame.bssid}
            self.devices[mac] = dev_node
        else:
            self.devices[mac]['last_seen'] = time.time()
            self.devices[mac]['time'] = datetime.today().strftime("%d/%m/%Y")
            dev_node = self.devices[mac]

        dev_node['signal'] = frame.signal_strength

        if mac == frame.src:
            dev_node['frames_out'].append((time.time(), frame.frame_bytes))
        elif mac == frame.dst:
            dev_node['frames_in'].append((time.time(), frame.frame_bytes))

        # Trim old frames (those that are older than window)
        self.frame_count_by_device[mac] += 1
        if self.frame_count_by_device[mac] % self.trim_every_num_frames == 0:
            dev_node['frames_out'] = trim_frames_to_window(dev_node['frames_out'], self.window)
            dev_node['frames_in'] = trim_frames_to_window(dev_node['frames_in'], self.window)

        dev_node_redis = copy.deepcopy(dev_node)
        dev_node_redis['frames_out'] = str(dev_node_redis['frames_out'])
        dev_node_redis['frames_in'] = str(dev_node_redis['frames_in'])

        dev_node_redis['bssid'] = str(dev_node_redis['bssid'])
        
        try:
            self.redis_live.hmset(f"device:{mac}", dev_node_redis)
        except Exception as ex:
            print("Error:", ex, flush=True)
            print('Device not valid', flush=True)

    @staticmethod
    def _with_frames_summed(dev_node):
        """Helper function to aid in serialization."""
        dev_node = copy.deepcopy(dev_node)
        frames_in = sum([num_bytes for _, num_bytes in dev_node.pop('frames_in', ())])
        frames_out = sum([num_bytes for _, num_bytes in dev_node.pop('frames_out', ())])
        dev_node['bytes'] = frames_in + frames_out
        return dev_node
