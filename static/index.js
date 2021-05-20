function getDevices() {
  $.getJSON('/api/devices_info', function(data) {
      var devicesListData = '';
      $.each(data, function(key, value) {
          devicesListData += '<tr>';
          devicesListData += '<td>'+value.mac+'</td>';
          devicesListData += '<td>'+value.channel+'</td>';
          devicesListData += '<td>'+value.signal+'</td>';
          devicesListData += '<td>'+value.vendor+'</td>';
          devicesListData += '<td>'+value.time+'</td>';
          devicesListData += '</tr>';     
      });
          $('#devicesList').html(devicesListData);
          setDevicesChart()
  });
}

function setDevicesChart() {
    var ctx = document.getElementById('chartCanvasDevices').getContext('2d');
    var devices = $.getJSON('/api/devices_channels');
    var chart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: [1,2,3,4,5,6,7,8,9,10,11,12,13,14],
          datasets: [
                      {
                          label: 'Devices per channel',
                          data: devices,
                          backgroundColor: 'blue',
                          borderColor: 'blue',
                          borderWidth: 2,
                          fill: true,
                          pointBorderWidth: 1,
                          pointHoverRadius: 5,
                          pointHoverBackgroundColor: 'blue',
                          pointHoverBorderColor: 'blue',
                          pointHoverBorderWidth: 2,
                          pointRadius: 1,
                          pointHitRadius: 10,
                      }          
                    ]
        },
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
        });
}

function scanControl(id){
  $.getJSON('/api/scan', function(data) {
    if(data.running){
      document.getElementById(id).className = "btn btn-danger";
      document.getElementById(id).innerHTML = "Apagar";
      $.ajax({url : '/api/disable_scan', type : 'POST'});
    } else {
      document.getElementById(id).className = "btn btn-success";
      document.getElementById(id).innerHTML = "Encender";
      $.ajax({url : '/api/enable_scan', type : 'POST'});
    }
  });
}

$(document).ready(function() {

  $.each ($("[onload]"), function (index, item) {
    $(item).prop ("onload").call (item);
    return false;
  });

  if (window.location.pathname == '/') {
      $('#eraseForm').click(function(event) {

          $.ajax({
              url : '/erase_data',
              type : 'POST',
          });
  
          event.preventDefault();
  
      });
    }

    if (window.location.pathname == '/devices') {
        getDevices();
        // Fetch every 5 seconds
        setInterval(getDevices, 2000);
    }

});