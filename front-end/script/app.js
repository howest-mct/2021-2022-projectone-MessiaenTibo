'use strict';

const lanIP = `${window.location.hostname}:5000`; // ip van de webserver
// const socketio = io(lanIP);
let dailyGoal



//**** get_ ****
const get_Temperature = function(){
    const url = "http://192.168.168.169:5000/api/v1/history/"
    handleData(url, show_Temperature)
  }

const get_humidity = function(){
  const url = "http://192.168.168.169:5000/api/v1/history/humidity/"
  handleData(url, show_humidity)
}



//**** show_ ****
const show_Temperature = function(jsonObject){
    const temp = document.querySelector('.tempValue');
    temp.innerHTML = jsonObject.Waarde + "°C";
}

const show_humidity = function(jsonObject){
  const humidity = document.querySelector('.humidityValue');
  humidity.innerHTML = jsonObject.Waarde + "%";
}



//**** listenTo ****
const listenToUI = function(){
    listenToClickReadTemp()
    listenToClickReadHumidity()
}

const listenToClickReadTemp = function(){
    const buttons = document.querySelectorAll('.temp');
    for(const b of buttons){
      b.addEventListener('click', function(){
        console.log("klik temp")
        get_Temperature()
      })
    }
  }


const listenToClickReadHumidity = function(){
    const buttons = document.querySelectorAll('.humidity');
    for(const b of buttons){
      b.addEventListener('click', function(){
        console.log("klik humidity")
        get_humidity()
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


//**** init ****
const init = function(){
    console.log("Front-end loaded");
    //dailyGoal = document.querySelector(".js-daily-goal")
    //console.log(dailyGoal)
    listenToUI();
    //loadDailyGoal();
    // listenToSocket();
}



//**** DOMContentLoaded ****
document.addEventListener('DOMContentLoaded', init);