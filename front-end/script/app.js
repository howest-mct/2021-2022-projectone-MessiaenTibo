'use strict';

const lanIP = `${window.location.hostname}:5000`; // ip van de webserver
const socketio = io(lanIP);



//**** listenTo ****
const listenToUI = function(){

}


//**** socketio ****
const listenToSocket = function(){
    socketio.on("connect", function(){
        console.log("Verbonden met socket webserver");
    });
};



//**** init ****
const init = function(){
    console.log("Front-end loaded");

    listenToUI();
    listenToSocket();
}



//**** DOMContentLoaded ****
document.addEventListener('DOMContentLoaded', init);