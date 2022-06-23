'use strict';

const lanIP = `${window.location.hostname}:5000`; // ip van de webserver
const socketio = io(lanIP);
let dailyGoal;
let TotalGoal;
let TodaysWaterUsage;
let TodaysWaterUsageUser1 = 0;
let TodaysWaterUsageUser2 = 0;
let TodaysWaterUsageUser3 = 0;
let TodaysWaterUsageUser4 = 0;
let activeUser;



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
  // grafiek legen
  if(document.querySelector('.js-chart') != null)
  {
    document.querySelector('.js-chart').innerHTML = ""
    const url = `http://${lanIP}/api/v1/history/WaterUsage/`
    handleData(url, showData);
  }
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

const getMagneticContactUser = function (id){
  console.log('2😢')
  const url = `http://${lanIP}/api/v1/MagneticContactUser/${id}`
  handleData(url, showMagneticContactUser);
};

const getUserInfoById = function (id){
  console.log("2🤞")
  const url = `http://${lanIP}/api/v1/UserInfo/${id}`
  handleData(url, loadUserInfo);
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
  humidity.innerHTML = waarde + "°C";
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
    converted_data.push(parseFloat(dag.Totaal/1000).toFixed(0));
  }
  drawChart(converted_labels, converted_data);
};

const showTotalGoal = function (jsonObject) {
  TotalGoal = jsonObject.TotalGoal
  getTodaysWaterUsage()
}

const showTodaysWaterUsage = function (jsonObject) {
  TodaysWaterUsage = 0
  for (let dag of jsonObject) {
    if(dag.GebruikerId == 1){
      TodaysWaterUsageUser1 = parseInt(dag.Totaal/1000)
    }
    if(dag.GebruikerId == 2){
      TodaysWaterUsageUser2 = parseInt(dag.Totaal/1000)
    }
    if(dag.GebruikerId == 3){
      TodaysWaterUsageUser3 = parseInt(dag.Totaal/1000)
    }
    if(dag.GebruikerId == 4){
      TodaysWaterUsageUser4 = parseInt(dag.Totaal/1000)
    }
  }
  TodaysWaterUsage = TodaysWaterUsageUser1 + TodaysWaterUsageUser2 + TodaysWaterUsageUser3 + TodaysWaterUsageUser4
  getGoal()
}

const showActiveUser = function (userId, firstname, lastname, goal){
  console.log('4😢')
  let TodaysWaterUsageActiveUser = 0
  if(userId == 1){
    TodaysWaterUsageActiveUser = TodaysWaterUsageUser1
  }
  if(userId == 2){
    TodaysWaterUsageActiveUser = TodaysWaterUsageUser2
  }
  if(userId == 3){
    TodaysWaterUsageActiveUser = TodaysWaterUsageUser3
  }
  if(userId == 4){
    TodaysWaterUsageActiveUser = TodaysWaterUsageUser4
  }
  socketio.emit("F2B_active_user_usage", TodaysWaterUsageActiveUser)
  socketio.emit("F2B_active_user_goal", goal)
  activeUser.innerHTML = `<h2>Active user</h2>
  <img class="c-profile-pictures" src="/pictures/Profile picture ${userId}.png" alt="Profile picture ${userId}">
  <h4>${firstname} ${lastname}: ${TodaysWaterUsageActiveUser} liter</h4>`
}

const showMagneticContactUser = function (jsonObject){
  console.log('3😢')
  let firstname = jsonObject.Naam
  let lastname = jsonObject.Voornaam
  let magneetcontact = jsonObject.Magneetcontact
  let goal = jsonObject.Goal
  console.log(firstname)
  console.log(lastname)
  showActiveUser(magneetcontact, firstname, lastname, goal);
}

const showUserInfo = function(magneetcontact, firstname, lastname, goal, email){
  console.log("4🤞")
  console.log(magneetcontact)
  let urlParams = new URLSearchParams(window.location.search);
  let id = parseInt(urlParams.get('id'));
  document.querySelector('.js-profile-picture-placeholder').innerHTML = `<img class="c-profile-picture-detail u-inline" src="/pictures/Profile picture ${id}.png" alt="Profile picture ${id}"></img>`
  if(magneetcontact == '')
  {
    document.querySelector('.js-magnetic-contact-placeholder').innerHTML = `<option value="1">Magnetic Contact 1</option> <option value="2">Magnetic Contact 2</option> <option value="3">Magnetic Contact 3</option><option value="4">Magnetic Contact 4</option><option value="" selected>No Magnetic Contact</option>`
  }
  else if(magneetcontact == 1){
    document.querySelector('.js-magnetic-contact-placeholder').innerHTML = `<option value="1" selected>Magnetic Contact 1</option> <option value="2">Magnetic Contact 2</option> <option value="3">Magnetic Contact 3</option><option value="4">Magnetic Contact 4</option><option value="">No Magnetic Contact</option>`
  }
  else if(magneetcontact == 2){
    document.querySelector('.js-magnetic-contact-placeholder').innerHTML = `<option value="1">Magnetic Contact 1</option> <option value="2" selected>Magnetic Contact 2</option> <option value="3">Magnetic Contact 3</option><option value="4">Magnetic Contact 4</option><option value="">No Magnetic Contact</option>`
  }
  else if(magneetcontact == 3){
    document.querySelector('.js-magnetic-contact-placeholder').innerHTML = `<option value="1">Magnetic Contact 1</option> <option value="2">Magnetic Contact 2</option> <option value="3" selected>Magnetic Contact 3</option><option value="4">Magnetic Contact 4</option><option value="">No Magnetic Contact</option>`
  }
  else if(magneetcontact == 4){
    document.querySelector('.js-magnetic-contact-placeholder').innerHTML = `<option value="1">Magnetic Contact 1</option> <option value="2">Magnetic Contact 2</option> <option value="3">Magnetic Contact 3</option><option value="4" selected>Magnetic Contact 4</option><option value="">No Magnetic Contact</option>`
  }
  document.querySelector('.js-first-name-placeholder').value = firstname
  document.querySelector('.js-last-name-placeholder').value = lastname
  document.querySelector('.js-goal-placeholder').value = goal
  document.querySelector('.js-email-placeholder').value = email
}

//**** listenTo ****
const listenToUI = function(){
  listenToclickProfile()
  if(document.querySelector(".js-profiledetail-page")){
    listenToClickSave()
  }
}

const listenToclickProfile = function(){
  const buttons = document.querySelectorAll('.js-profile-click')
  for (let button of buttons) {
    button.addEventListener('click', function () {
      const id = this.getAttribute('data-gebruiker-id')
      window.location.href = `ProfileDetail.html?id=${id}`;
    })
  }
}

const listenToClickSave = function(){
  document.querySelector('.js-btn-save').addEventListener('click', function() {
    // get gebruikerid
    let urlParams = new URLSearchParams(window.location.search);
    let id = parseInt(urlParams.get('id'));
    // get magneticContact
    let magneetcontact = document.querySelector('.js-magnetic-contact-placeholder');
    let magneetcontactid
    if(magneetcontact.value != ''){
      magneetcontactid = magneetcontact.value;
    }
    else{
      magneetcontactid = null
    }
    //
    const jsonObject = {
      Email: document.querySelector('.js-email-placeholder').value,
      Magneetcontact: magneetcontactid,
      Naam: document.querySelector('.js-last-name-placeholder').value,
      Voornaam: document.querySelector('.js-first-name-placeholder').value,
      Goal: document.querySelector('.js-goal-placeholder').value,
      GebruikerId: id,
    };
    console.log(jsonObject)
    handleData(`http://${lanIP}/api/v1/Users/`,
    callbackSave,
    null,
    'PUT',
    JSON.stringify(jsonObject))
  });
}

// call_backs
const callbackSave = function (data) {
  console.log(data.status);
  // htmlMelding.classList.remove('u-hide');
  // htmlMelding.innerHTML = data.status;
  document.querySelector('.js-btn-save').innerHTML = `${data.status}`
  let delay = 1500;
  setTimeout(function () {
    document.querySelector('.js-btn-save').innerHTML = "Save"
  }, delay);
};

// **** socketio ****
const listenToSocket = function(){
    socketio.on("connect", function(){
        console.log("Verbonden met socket webserver");
        socketio.emit("F2B_new_connection")
    });
    socketio.on("B2F_new_data", function(){
        console.log("Verbonden met socket webserver");
        get_RoomTemperature()
        // get_WaterTemperature()
        get_Humidity()
        //get goal
        // getTotalGoal()
    });
    socketio.on("B2F_new_data_id", function(id){
      console.log("Verbonden met socket webserver");
      get_RoomTemperature()
      get_WaterTemperature()
      get_Humidity()
      //get goal
      getTotalGoal()
      //Active user
      getMagneticContactUser(id)
  });
    socketio.on("B2F_new_active_user", function(userId){
      getMagneticContactUser(userId)
      getData()
    });
    socketio.on("B2F_no_active_user", function(){
      RemoveActiveUser();
      getData()
    });
};


// **** methods ****
const loadDailyGoal = function(){
    let percent = parseFloat(TodaysWaterUsage) / parseFloat(TotalGoal) * 100;
    let percent1 = parseFloat(TodaysWaterUsageUser1) / parseFloat(TotalGoal) * 100
    let percent2 = parseFloat(TodaysWaterUsageUser1 + TodaysWaterUsageUser2) / parseFloat(TotalGoal) * 100
    let percent3 = parseFloat(TodaysWaterUsageUser1 + TodaysWaterUsageUser2 + TodaysWaterUsageUser3) / parseFloat(TotalGoal) * 100
    let percent4 = parseFloat(TodaysWaterUsageUser1 + TodaysWaterUsageUser2 + TodaysWaterUsageUser3 + TodaysWaterUsageUser4) / parseFloat(TotalGoal) * 100

    let secondcircle = dailyGoal.querySelector(".js-second-circle");
    let thirdcircle = dailyGoal.querySelector(".js-third-circle");
    let fourthcircle = dailyGoal.querySelector(".js-fourth-circle");
    let fifthcircle = dailyGoal.querySelector(".js-fifth-circle");

    secondcircle.style['stroke-dashoffset'] = 440 - (440 * percent4) / 100;
    thirdcircle.style['stroke-dashoffset'] = 440 - (440 * percent3) / 100;
    fourthcircle.style['stroke-dashoffset'] = 440 - (440 * percent2) / 100;
    fifthcircle.style['stroke-dashoffset'] = 440 - (440 * percent1) / 100;

    let number = dailyGoal.querySelector(".number");
    number.innerHTML = `<h4>${parseFloat(percent).toFixed(0)}<span>%</span></h4>`
}

const loadUserInfo = function(jsonObject){
  console.log(jsonObject)
  console.log("3🤞")
  let firstname = jsonObject.Voornaam
  let lastname = jsonObject.Naam
  let magneetcontact
  let goal = jsonObject.Goal
  if(jsonObject.Magneetcontact != null){
    magneetcontact = jsonObject.Magneetcontact
  }
  else{
    magneetcontact = ''
  }
  let email = jsonObject.Email
  showUserInfo(magneetcontact, firstname, lastname, goal, email);
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

const RemoveActiveUser = function(){
  activeUser.innerHTML = `<h1>No active user</h1>`
}

//**** init ****
const init = function(){
    console.log("Front-end loaded");
    activeUser = document.querySelector(".acive-user")
    dailyGoal = document.querySelector(".js-daily-goal")
    //console.log(dailyGoal)
    listenToUI();
    //loadDailyGoal();
    listenToSocket();
    toggleNav();
    getData();
    getTotalGoal()
    get_WaterTemperature()
    if(document.querySelector(".js-profiledetail-page")){
      let urlParams = new URLSearchParams(window.location.search);
      let id = urlParams.get('id');
      console.log("1🤞")
      getUserInfoById(id);
    }
}



//**** DOMContentLoaded ****
document.addEventListener('DOMContentLoaded', init);