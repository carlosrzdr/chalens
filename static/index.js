var chartDevices;
var chartBytes;

function getDevices() {
  $.getJSON('/api/devices_info', function(data) {
      var devicesListData = '';
      $.each(data, function(key, value) {
          devicesListData += "<tr>";
          devicesListData += '<td>'+value.mac+'</td>';
          devicesListData += '<td>'+value.channel+'</td>';
          devicesListData += '<td>'+value.signal+'</td>';
          devicesListData += '<td>'+value.vendor+'</td>';
          devicesListData += '<td>'+value.time+'</td>';
          devicesListData += '</tr>';     
      });
          $('#devicesList').html(devicesListData);

          var search = $("#searchDevices").val().toLowerCase();
          $("#devicesList tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(search) > -1)
          });

          $('#devicesCount').html("DEVICES: " + data.length);
  });
}

function setUpDevicesChart() {
  var ctx = document.getElementById('chartCanvasDevices').getContext('2d');
  var devices_channels = $.getJSON('/api/devices_channels');
  chartDevices = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: [1,2,3,4,5,6,7,8,9,10,11,12,13,14],
        datasets: [
                    {
                        label: 'Devices',
                        data: devices_channels.responseJSON,
                        backgroundColor: 'rgba(255, 87, 51, 0.6)',
                        borderColor: 'rgba(255, 87, 51, 1)',
                        borderWidth: 1
                    }        
                  ]
      },
      options: {
        plugins: {
          legend: {
            display: false
          }
        },
        scales: {
          y: {
            title: {
              display: true,
              text: "Number of devices",
            },
            beginAtZero: true,
            max: 5
          },
          x: {
            title: {
              display: true,
              text: "Channel",
            },
          }
        }
      }
      });
}

function setUpBytesChart() {
  var ctx = document.getElementById('chartCanvasBytes').getContext('2d');
  var devices_bytes = $.getJSON('/api/devices_bytes');
  chartBytes = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: [1,2,3,4,5,6,7,8,9,10,11,12,13,14],
        datasets: [
                    {
                      label: 'Bytes',
                      data: devices_bytes.responseJSON,
                      backgroundColor: 'rgba(61, 144, 203, 0.6)',
                      borderColor: 'rgba(61, 144, 203, 1)',
                      borderWidth: 1
                  }           
                  ]
      },
      options: {
        plugins: {
          legend: {
            display: false
          }
        },
        scales: {
          y: {
            title: {
              display: true,
              text: "Bytes",
            },
            beginAtZero: true,
            max: 5000
          },
          x: {
            title: {
              display: true,
              text: "Channel",
            },
          }
        }
      }
      });
}

function updateDevicesChart() {
  $.getJSON('/api/devices_channels', function(data) {
    chartDevices.data.datasets[0].data = data;
    chartDevices.options.scales.y.max = Math.ceil((Math.max.apply(null, data)+3)/5) * 5;
    chartDevices.update();
  });
}

function updateBytesChart() {
  $.getJSON('/api/devices_bytes', function(data) {
    chartBytes.data.datasets[0].data = data;
    chartBytes.options.scales.y.max = Math.ceil((Math.max.apply(null, data)+3000)/5000) * 5000;
    chartBytes.update();
  });
}

function scanStatus(element){
  $.getJSON('/api/scan', function(data) {
    if(data.running==true){
      element.className = "mx-1 btn btn-danger";
      element.innerHTML = "Stop";
    } else {
      element.className = "mx-1 btn btn-success";
      element.innerHTML = "Start";
    }
  });
}

function scanControl(element){
  if(element.className=="mx-1 btn btn-danger"){
    $.ajax({url : '/api/disable_scan', type : 'POST'});
    element.className = "mx-1 btn btn-success";
    element.innerHTML = "Start";
    sessionStorage.setItem("lastTime",null);
  } else {
    $.ajax({url : '/api/enable_scan', type : 'POST'});
    element.className = "mx-1 btn btn-danger";
    element.innerHTML = "Stop";
    sessionStorage.setItem("lastTime",new Date().getTime());
  }
}

function eraseDB(){
  $.ajax({
    url : '/api/erase_data',
    type : 'POST',
  });
  getDevices();
  updateDevicesChart();
  updateBytesChart();
}

function controlStatus(){
  $.getJSON('/api/channel', function(data) {
    $('#currentChannel').html(data.channel);
  });
  $.getJSON('/api/optimal_channel', function(data) {
    $('#bestChannel').html(data.channel);
  });
}

function hopStatus(){
  var element = document.getElementById('channelHopper');
  $.getJSON('/api/hop', function(data) {
    if(data.hop==true){
      element.className = "mx-1 btn btn-danger btn-lg";
      element.innerHTML = "Disable";
    } else {
      element.className = "mx-1 btn btn-success btn-lg";
      element.innerHTML = "Enable";
    }
  });
}

function hopControl(){
  var element = document.getElementById('channelHopper')
  if(element.className=="mx-1 btn btn-danger btn-lg"){
    $.ajax({url : '/api/disable_channel_hopper', type : 'POST'});
    element.className = "mx-1 btn btn-success btn-lg";
    element.innerHTML = "Enable";
  } else {
    $.ajax({url : '/api/enable_channel_hopper', type : 'POST'});
    element.className = "mx-1 btn btn-danger btn-lg";
    element.innerHTML = "Disable";
  }
}

function changeChannel(element){
  if(element.innerHTML == ''){
    $.ajax({
      type: "POST",
      url: "/api/change_channel",
      data: {"channel" : element.value}
    });
  } else {
    $.ajax({
      type: "POST",
      url: "/api/change_channel",
      data: {"channel" : element.innerHTML}
    });
  }
}

function stopScanTime() {
  if(sessionStorage.getItem("lastTime")){
    if((new Date().getTime() - sessionStorage.getItem("lastTime")) / 1000 > 30){
      scanControl(document.getElementById('scanBtn'));
    }
  }
}

function saveData() {
  $.ajax({
    url : '/api/save_data',
    type : 'POST',
  });
}

$(document).ready(function() {

  setInterval( function () {
    stopScanTime();
    scanStatus(document.getElementById('scanBtn'));
  }, 2000);

  $.each ($("[onload]"), function (index, item) {
    $(item).prop ("onload").call (item);
    return false;
  });

  if (window.location.pathname == '/control') {
    controlStatus();
    hopStatus();
    setInterval(function(){
      controlStatus();
      hopStatus();
    }, 2000);
    $(document).on('submit', '#manualChannel', function() {
      changeChannel(document.getElementById('channel'))
      return false;
    });
  }

  if (window.location.pathname == '/devices') {
      getDevices();
      setUpBytesChart();
      setUpDevicesChart();
      // Fetch every 2 seconds
      setInterval(function () {
        getDevices();
        updateDevicesChart();
        updateBytesChart();
      }, 2000);

      $("#searchDevices").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#devicesList tr").filter(function() {
          $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
      });
  }

});