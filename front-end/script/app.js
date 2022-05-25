'use strict';

const lanIP = `${window.location.hostname}:5000`; // ip van de webserver
// const socketio = io(lanIP);
let dailyGoal


const getTemperatuur = function(){
    const url = "http://127.0.0.1:5000/api/v1/temperatuur/"
    handleData(url, showDestination)
  }


const showTemperatuur = function(jsonObject){
    const temp = document.querySelector('.tempValue');
    temp.innerHTML = "30°C";
}

//**** listenTo ****
const listenToUI = function(){
    listenToClickReadTemp()

}

const listenToClickReadTemp = function(){
    const buttons = document.querySelectorAll('.temp');
    for(const b of buttons){
      b.addEventListener('click', function(){
        //   showTemperatuur
      })
    }
  }

// **** socketio ****
const listenToSocket = function(){
    socketio.on("connect", function(){
        console.log("Verbonden met socket webserver");
    });
};



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