'use strict';

const lanIP = `${window.location.hostname}:5000`; // ip van de webserver
// const socketio = io(lanIP);
let dailyGoal


//**** listenTo ****
const listenToUI = function(){
    listenToClickReadTemp()

}

const listenToClickReadTemp = function(){
    const buttons = document.querySelectorAll('.temp');
    for(const b of buttons){
      b.addEventListener('click', function(){
          const temp = document.querySelector('.tempValue');
          temp.innerHTML = "30°C";
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