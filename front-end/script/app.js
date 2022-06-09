'use strict';

const lanIP = `${window.location.hostname}:5000`; // ip van de webserver
// const socketio = io(lanIP);
let dailyGoal



//**** get_ ****
const get_RoomTemperature = function(){
    const url = "http://192.168.168.169:5000/api/v1/history/RoomTemp/"
    handleData(url, show_RoomTemperature)
  }

const get_Humidity = function(){
  const url = "http://192.168.168.169:5000/api/v1/history/Humidity/"
  handleData(url, show_humidity)
}

const get_WaterFlow = function(){
  const url = "http://192.168.168.169:5000/api/v1/history/Waterflow/"
  handleData(url, show_WaterFlow)
}

const get_WaterTemperature = function(){
  const url = "http://192.168.168.169:5000/api/v1/history/WaterTemp/"
  handleData(url, show_WaterTemperature)
}



//**** show_ ****
const show_WaterTemperature = function(jsonObject){
    const temp = document.querySelector('.watertempValue');
    temp.innerHTML = jsonObject.Waarde + "°C";
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
  humidity.innerHTML = jsonObject.Waarde + " °C";
}



//**** listenTo ****
const listenToUI = function(){
    listenToClickReadRoomTemp()
    listenToClickReadHumidity()
    listenToClickReadWaterFlow()
    listenToClickReadWaterTemp()
}

const listenToClickReadRoomTemp = function(){
    const buttons = document.querySelectorAll('.roomtemp');
    for(const b of buttons){
      b.addEventListener('click', function(){
        console.log("klik temp")
        get_RoomTemperature()
      })
    }
  }


const listenToClickReadHumidity = function(){
    const buttons = document.querySelectorAll('.humidity');
    for(const b of buttons){
      b.addEventListener('click', function(){
        console.log("klik humidity")
        get_Humidity()
      })
    }
  }


  const listenToClickReadWaterFlow = function(){
    const buttons = document.querySelectorAll('.waterflow');
    for(const b of buttons){
      b.addEventListener('click', function(){
        console.log("klik waterflow")
        get_WaterFlow()
      })
    }
  }

  const listenToClickReadWaterTemp = function(){
    const buttons = document.querySelectorAll('.watertemp');
    for(const b of buttons){
      b.addEventListener('click', function(){
        console.log("klik temp")
        get_WaterTemperature()
      })
    }
  }


// **** socketio ****
const listenToSocket = function(){
    socketio.on("connect", function(){
        console.log("Verbonden met socket webserver");
    });
};


// **** methods ****
const loadDailyGoal = function(){
    let percent = dailyGoal.getAttribute("percent");
    console.log(percent);
    let secondcircle = dailyGoal.querySelector(".js-second-circle");
    console.log(secondcircle);
    secondcircle.style['stroke-dashoffset'] = 440 - (440 * percent) / 100;
}

const toggleNav = function() {
  let toggleTrigger = document.querySelectorAll(".js-toggle-nav");
  for (let i = 0; i < toggleTrigger.length; i++) {
      toggleTrigger[i].addEventListener("click", function () {
          document.querySelector("body").classList.toggle("has-mobile-nav");
      })
  }
}


//**** init ****
const init = function(){
    console.log("Front-end loaded");
    //dailyGoal = document.querySelector(".js-daily-goal")
    //console.log(dailyGoal)
    listenToUI();
    //loadDailyGoal();
    // listenToSocket();
    toggleNav();
}



//**** DOMContentLoaded ****
document.addEventListener('DOMContentLoaded', init);