/* On Linux, BLE normally needs admin right to be able to access BLE
 *
 * sudo setcap cap_net_raw+eip $(eval readlink -f `which node`)
 */
 

//sudo node puck.js image1 170f

var noble = require('@abandonware/noble');
var process = require('process');
var WebSocketClient = require('websocket').client
var client = new WebSocketClient()
client.on('connectFailed', function(error) {
    console.log('Connect Error: ' + error.toString());
});

var data1 = process.argv[2]
var data2 = process.argv[3]
var NAME = "Puck.js "+data2;
var COMMAND = '\x03\x10var id = "A";'+
'\n\x10function press(){LED1.write(1),print("true")};'+
'\n\x10function released(){LED1.write(0),print("false")};'+
'\n\x10setWatch(press, BTN1, {repeat:true, edge:"rising"});\n\x10setWatch(released, BTN1, {repeat:true, edge:"falling"})\n';

var btDevice;
var txCharacteristic;
var rxCharacteristic;
var foundDevice = false;
var recievedTrue = true, recievedFalse = true;

client.on('connect',connection=>{
    console.log('webSocket connected !');
    noble.on('stateChange', function(state) {
     console.log("Noble: stateChange -> "+state);
      if (state=="poweredOn")
        noble.startScanning([], true);
    });



    noble.on('discover', function(dev) {
      
      if (foundDevice) return;
      if(dev.advertisement.localName)console.log("Found device: ",dev.advertisement.localName);
      if (dev.advertisement.localName != NAME) return;
      noble.stopScanning();
      // noble doesn't stop right after stopScanning is called,
      // so we have to use foundDevice to ensure we onloy connect once
      foundDevice = true;
      // Now connect!
      connect(dev, connection, function() {
        // Connected!
        write(COMMAND, function() {
          console.log("all set")
        });
      });
    });
})


function connect(dev, socketCo, callback) {
  btDevice = dev;
  console.log("BT> Connecting");
  btDevice.on('disconnect', function() {
    console.log("Disconnected");
    foundDevice = false;
    noble.startScanning([], true);
  });
  btDevice.connect(function (error) {
    if (error) {
      console.log("BT> ERROR Connecting",error);
      btDevice = undefined;
      return;
    }
    console.log("BT> Connected");
    btDevice.discoverAllServicesAndCharacteristics(function(error, services, characteristics) {
      function findByUUID(list, uuid) {
        for (var i=0;i<list.length;i++)
          if (list[i].uuid==uuid) return list[i];
        return undefined;
      }

      var btUARTService = findByUUID(services, "6e400001b5a3f393e0a9e50e24dcca9e");
      txCharacteristic = findByUUID(characteristics, "6e400002b5a3f393e0a9e50e24dcca9e");
      rxCharacteristic = findByUUID(characteristics, "6e400003b5a3f393e0a9e50e24dcca9e");
      if (error || !btUARTService || !txCharacteristic || !rxCharacteristic) {
        console.log("BT> ERROR getting services/characteristics");
        console.log("Service "+btUARTService);
        console.log("TX "+txCharacteristic);
        console.log("RX "+rxCharacteristic);
        btDevice.disconnect();
        txCharacteristic = undefined;
        rxCharacteristic = undefined;
        btDevice = undefined;
        return openCallback();
      }

      rxCharacteristic.on('data', function (data) {
        var s = "";
        for (var i=0;i<data.length;i++) s+=String.fromCharCode(data[i]);
        if(s.includes("true") && recievedTrue){
          console.log("press");
          if(socketCo.connected)socketCo.send('puckjs.'+data1+':push>True;id>'+data2)
          recievedTrue = false
          setTimeout(()=>{recievedTrue=true},200)
        }else if(s.includes("false") && recievedFalse){
          console.log("released");
          if(socketCo.connected)socketCo.send('puckjs.'+data1+':push>False;id>'+data2)
          recievedFalse = false
          setTimeout(()=>{recievedFalse=true},200)
        }
      });
      rxCharacteristic.subscribe(function() {
        callback();
      });
    });
    console.log("after discover all")
  });
};

function write(data, callback) {  
  function writeAgain() {
    if (!data.length) return callback();
    var d = data.substr(0,20);
    data = data.substr(20);
    var buf = Buffer.alloc(d.length);
    for (var i = 0; i < buf.length; i++){
      buf.writeUInt8(d.charCodeAt(i), i);
    }
    txCharacteristic.write(buf, false, writeAgain);
  }
  writeAgain();
  console.log("Analysing data")
}

function disconnect() {
  btDevice.disconnect();
}
client.connect('ws://localhost:8000/')
//'\x03\x10var id = "A"\x10\nconsole.log("lol")\x10\nfunction press(){LED1.write(1)}\x10\nfunction released(){LED1.write(0)}\x10\nsetWatch(press, BTN1, {repeat:true, edge:"rising"})\x10\nsetWatch(released, BTN1, {repeat:true, edge:"falling"})\n'
//\x03\x10clearInterval()\n\x10setInterval(function() {LED.toggle()}, 500);\n\x10print('Hello World')\n
/*var id = "A";

var verifLedOn = true;
// keep track of the ID, see later
var timeout_ID;
function press() {
  LED1.write(1);
}
function released() {
  LED1.write(0);
}

setWatch(press, BTN1, {repeat:true, edge:"rising"});
setWatch(released, BTN1, {repeat:true, edge:"falling"});*/
