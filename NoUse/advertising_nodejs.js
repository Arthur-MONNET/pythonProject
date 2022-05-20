/*
NRF.setAdvertising({},{manufacturer: 0x0590, manufacturerData:[0]});

setWatch(function() {
  LED1.set()
  NRF.setAdvertising({},{manufacturer: 0x0590, manufacturerData:[1]});
}, BTN, {edge:"rising", repeat:1, debounce:20})
setWatch(function() {
  LED1.reset()
  NRF.setAdvertising({},{manufacturer: 0x0590, manufacturerData:[0]});
}, BTN, {edge:"falling", repeat:1, debounce:20})
*/

var noble = require('@abandonware/noble');
var WebSocket = require('ws')
var socket = new WebSocket("ws://localhost:8000")
socket.send('connection:' + 'puckjs' + '.' + 'list');




// List of allowed devices
const devices = [
  "d3:a2:fb:dc:17:0f", // <- puck.js 170f 
  "c8:e6:c2:7b:ea:0b", // <- Puck.js ea0b
]; 
// last advertising data received
var lastAdvertising = {
};

function onDeviceChanged(addr, data) {
  socket.send('puckjs.'+addr+':push>'+(data.data[0]==1?'True':'False'));
	console.log("Device ",addr,"changed data",JSON.stringify(data));
}

function onDiscovery(peripheral) {
  // do we know this device?
  if (devices.indexOf(peripheral.address)<0) return;
  // does it have manufacturer data with Espruino/Puck.js's UUID
  if (!peripheral.advertisement.manufacturerData ||
      peripheral.advertisement.manufacturerData[0]!=0x90 ||
      peripheral.advertisement.manufacturerData[1]!=0x05) return;
  // get just our data
  var data = peripheral.advertisement.manufacturerData.slice(2);
  // check for changed services
  if (lastAdvertising[peripheral.address] != data.toString())
    onDeviceChanged(peripheral.address, data);
  lastAdvertising[peripheral.address] = data;
}

noble.on('stateChange',  function(state) {
  if (state!="poweredOn") return;
  console.log("Starting scan...");
  noble.startScanning([], true);
});
noble.on('discover', onDiscovery);
noble.on('scanStart', function() { console.log("Scanning started."); });
noble.on('scanStop', function() { console.log("Scanning stopped.");});
