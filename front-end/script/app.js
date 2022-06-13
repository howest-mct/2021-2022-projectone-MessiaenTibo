'use strict';

const lanIP = `${window.location.hostname}:5000`; // ip van de webserver
const socketio = io(lanIP);
let dailyGoal;
let TotalGoal;
let TodaysWaterUsage;



//**** get_ ****
const get_RoomTemperature = function(){
    //const url = "http://192.168.168.169:5000/api/v1/history/RoomTemp/" 
    const url = `http://${lanIP}/api/v1/history/RoomTemp/`
    handleData(url, show_RoomTemperature)
  }

const get_Humidity = function(){
  //const url = "http://192.168.168.169:5000/api/v1/history/Humidity/"
  const url = `http://${lanIP}/api/v1/history/Humidity/`
  handleData(url, show_humidity)
}

const get_WaterFlow = function(){
  //const url = "http://192.168.168.169:5000/api/v1/history/Waterflow/"
  const url = `http://${lanIP}/api/v1/history/Waterflow/`
  handleData(url, show_WaterFlow)
}

const get_WaterTemperature = function(){
  //const url = "http://192.168.168.169:5000/api/v1/history/WaterTemp/"
  const url = `http://${lanIP}/api/v1/history/WaterTemp/`
  handleData(url, show_WaterTemperature)
}

const getData = function () {
  //const url = "http://192.168.168.169:5000/api/v1/history/WaterUsage/"
  const url = `http://${lanIP}/api/v1/history/WaterUsage/`
  handleData(url, showData);
};

const getTotalGoal = function () {
  //const url = "http://192.168.168.169:5000/api/v1/TotalGoal/"
  const url = `http://${lanIP}/api/v1/TotalGoal/`
  handleData(url, showTotalGoal);
};

const getTodaysWaterUsage = function () {
  //const url = "http://192.168.168.169:5000/api/v1/history/TodaysWaterUsage/"
  const url = `http://${lanIP}/api/v1/history/TodaysWaterUsage/`
  handleData(url, showTodaysWaterUsage);
};

const getGoal = function ()
{
  loadDailyGoal()
}


//**** show_ ****
const show_WaterTemperature = function(jsonObject){
    const temp = document.querySelector('.watertempValue');
    const waarde = parseFloat(jsonObject.Waarde).toFixed(1)
    temp.innerHTML = waarde + "°C";
}

const show_humidity = function(jsonObject){
  const humidity = document.querySelector('.humidityValue');
  humidity.innerHTML = jsonObject.Waarde + "%";
}

const show_WaterFlow = function(jsonObject){
  const humidity = document.querySelector('.waterflowValue');
  humidity.innerHTML = jsonObject.Waarde + " ml/sec";
}

const show_RoomTemperature = function(jsonObject){
  const humidity = document.querySelector('.roomtempValue');
  const waarde = parseFloat(jsonObject.Waarde).toFixed(1)
  humidity.innerHTML = waarde + " °C";
}

// const showData = function (jsonObject) {
//   console.log(jsonObject);
//   let converted_labels = [];
//   let converted_data = [];
//   for (let iphone of jsonObject) {
//     converted_labels.push(iphone.unit);
//     converted_data.push(iphone.price);
//   }
//   drawChart(converted_labels, converted_data);
// };

const showData = function (jsonObject) {
  console.log(jsonObject);
  let converted_labels = [];
  let converted_data = [];
  for (let dag of jsonObject) {
    converted_labels.push(dag.ActieDatum);
    converted_data.push(dag.Totaal);
  }
  drawChart(converted_labels, converted_data);
};

const showTotalGoal = function (jsonObject) {
  TotalGoal = jsonObject.TotalGoal
  getTodaysWaterUsage()
}

const showTodaysWaterUsage = function (jsonObject) {
  TodaysWaterUsage = jsonObject.Totaal
  getGoal()
}


//**** listenTo ****
const listenToUI = function(){
}



// **** socketio ****
const listenToSocket = function(){
    socketio.on("connect", function(){
        console.log("Verbonden met socket webserver");
        socketio.emit("F2B_new_connection")
    });
    socketio.on("B2F_new_data", function(){
        console.log("Verbonden met socket webserver");
        get_RoomTemperature()
        get_WaterTemperature()
        get_Humidity()

        //get goal
        getTotalGoal()
    });
};


// **** methods ****
const loadDailyGoal = function(){
    let percent = parseFloat(TodaysWaterUsage) / parseFloat(TotalGoal) * 100;
    console.log(percent);
    let secondcircle = dailyGoal.querySelector(".js-second-circle");
    console.log(secondcircle);
    secondcircle.style['stroke-dashoffset'] = 440 - (440 * percent) / 100;
    let number = dailyGoal.querySelector(".number");
    number.innerHTML = `<h4>${parseFloat(percent).toFixed(0)}<span>%</span></h4>`
}

const toggleNav = function() {
  let toggleTrigger = document.querySelectorAll(".js-toggle-nav");
  for (let i = 0; i < toggleTrigger.length; i++) {
      toggleTrigger[i].addEventListener("click", function () {
          document.querySelector("body").classList.toggle("has-mobile-nav");
      })
  }
}

const drawChart=function(labels,data){
  var options = {
    chart: {
      height: "78%",
      id: 'myChart',
      type: 'line',
    },
    stroke: {
      curve: 'stepline',
    },
    dataLabels: {
      enabled: false,
    },
    series: [
      {
        name: labels,
        data: data,
      },
    ],
    labels: labels,
    noData: {
      text: 'Loading...',
    },
    tooltip:{
      enabled: false
    },
    hover:{
      mode:null
    },
  };
let chart=new ApexCharts(document.querySelector('.js-chart'),options)
chart.render()
}

//**** init ****
const init = function(){
    console.log("LanIP");
    console.log(lanIP);
    console.log("Front-end loaded");
    dailyGoal = document.querySelector(".js-daily-goal")
    //console.log(dailyGoal)
    listenToUI();
    //loadDailyGoal();
    listenToSocket();
    toggleNav();
    getData();
}



//**** DOMContentLoaded ****
document.addEventListener('DOMContentLoaded', init);