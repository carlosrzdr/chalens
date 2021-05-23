var chartDevices;

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

          var search = $("#searchDevices").val().toLowerCase();
          $("#devicesList tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(search) > -1)
          });

          $('#devicesCount').html("DEVICES: " + data.length);
          updateDevicesChart();
  });
}

function setUpChart() {
  var ctx = document.getElementById('chartCanvasDevices').getContext('2d');
  var devices = $.getJSON('/api/devices_channels');
  chartDevices = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: [1,2,3,4,5,6,7,8,9,10,11,12,13,14],
        datasets: [
                    {
                        label: 'Devices',
                        data: devices.responseJSON
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
            max: 10
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

function scanStatus(element){
  $.getJSON('/api/scan', function(data) {
    if(data.running==true){
      element.className = "mx-1 btn btn-danger";
      element.innerHTML = "Apagar";
    } else {
      element.className = "mx-1 btn btn-success";
      element.innerHTML = "Encender";
    }
  });
}

function scanControl(element){
  $.getJSON('/api/scan', function(data) {
    if(data.running==true){
      $.ajax({url : '/api/disable_scan', type : 'POST'});
      element.className = "mx-1 btn btn-success";
      element.innerHTML = "Encender";
    } else {
      $.ajax({url : '/api/enable_scan', type : 'POST'});
      element.className = "mx-1 btn btn-danger";
      element.innerHTML = "Apagar";
    }
  });
}

function eraseDB(){
  $.ajax({
    url : '/erase_data',
    type : 'POST',
  });
  getDevices();
  updateDevicesChart();
}

$(document).ready(function() {

  setInterval(scanStatus(document.getElementById('scanBtn')), 2000)

  $.each ($("[onload]"), function (index, item) {
    $(item).prop ("onload").call (item);
    return false;
  });

  if (window.location.pathname == '/devices') {
      getDevices();
      setUpChart();
      // Fetch every 2 seconds
      setInterval(function () {
        getDevices();
        updateDevicesChart();
      }, 2000);

      $("#searchDevices").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#devicesList tr").filter(function() {
          $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
      });
  }

});