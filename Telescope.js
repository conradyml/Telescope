var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http, {allowEIO3: true});
var exec = require('child_process').exec, child;
var port = process.env.PORT || 3500;

//var ads1x15 = require('node-ads1x15');
//var adc = new ads1x15(0); // set to 0 for ads1015

var Gpio = require('pigpio').Gpio;
  LED = new Gpio(23, {mode: Gpio.OUTPUT});

var AzimuthSteps = 0;
var ElevationSteps = 0;
var AzStepsPerDegree=68.2666;
var ElStepsPerDegree=68.2666;

// Configure Motors.
let spec = {
    address: 0x60,
    steppers: [{W1:'M1', W2: 'M2'},{W1:'M3', W2:'M4'}],
    dcs: [],
    servos: [0,14]
};

var motorHat = require('motor-hat')(spec);
motorHat.init();
motorHat.steppers[0].setSteps(516);
motorHat.steppers[0].setSpeed({sps:40});
motorHat.steppers[0].setStyle('single');
motorHat.steppers[1].setSteps(516);
motorHat.steppers[1].setSpeed({sps:40});
motorHat.steppers[1].setStyle('interleaved');

app.get('/', function(req, res){
  res.sendFile('Telescope.html', { root: __dirname });
  console.log('HTML sent to client');
});

//child = exec("sudo bash start_stream.sh", function(error, stdout, stderr){});
motorHat.servos[0].calibrate(50, 1, 2);
motorHat.servos[0].moveTo(40);

//Whenever someone connects this gets executed
io.on('connection', function(socket){
  console.log('A user connected');

  
  socket.on('cam', function(toggle) {
    var numPics = 0;
    console.log('Taking a picture..');
    //Count jpg files in directory to prevent overwriting
    child = exec("find -type f -name '*.jpg' | wc -l", function(error, stdout, stderr){
      numPics = parseInt(stdout)+1;
      // Turn off streamer, take photo, restart streamer
      var command = 'sudo killall mjpg_streamer ; raspistill -o cam' + numPics + '.jpg -n && sudo bash start_stream.sh';
        //console.log("command: ", command);
        child = exec(command, function(error, stdout, stderr){
        io.emit('cam', 1);
      });
    });
    
  });

  // handle elevation change
  socket.on('elevation',function(degrees, minutes){
	 console.log("Received Elevation change: "+ degrees + " degrees, "+minutes+" minutes") 
	 console.log((degrees*60)+parseInt(minutes));
	 
	  var eChange = Math.round(((degrees*60) + parseInt(minutes))*ElStepsPerDegree/60); //
	  console.log('Changing Elevation by: '+ eChange)
	  var direction = 'fwd'
	  if (eChange<0){
		  direction = 'back'
	  }
	  motorHat.steppers[0].step(direction, Math.abs(eChange), function(err, result) {
		if (err) {
			console.log('Oh no, there was an error');
		} else {
			console.log('Did '+result.steps+' steps '+result.dir+' in '+result.duration/1000 +' seconds. I had to retry '+result.retried+' steps because you set me up quicker than your poor board can handle.');
			if (result.dir =='back'){
				ElevationSteps = ElevationSteps - result.steps;
			}else{
				ElevationSteps = ElevationSteps + result.steps;				
			}
			io.emit('elevation',ElevationSteps);
			console.log('New Elevation Angle: '+ElevationSteps);
			
		}
		motorHat.steppers[0].releaseSync();
	  });
	})

	//handle azimuth change
  socket.on('azimuth',function(degrees, minutes){
	  var aChange = Math.round(((degrees*60) + parseInt(minutes))*AzStepsPerDegree/60); //
	  console.log('Changing Azimuth by: '+ aChange)
	  var direction = 'fwd'
	  if (aChange<0){
		  direction = 'back'
	  }
	  motorHat.steppers[1].step(direction, Math.abs(aChange), function(err, result) {
		if (err) {
			console.log('Oh no, there was an error');
		} else {
			console.log('Did '+result.steps+' steps '+result.dir+' in '+result.duration/1000 +' seconds. I had to retry '+result.retried+' steps because you set me up quicker than your poor board can handle.');
			if (result.dir == 'back'){
				AzimuthSteps = AzimuthSteps - result.steps;
			}else{
				AzimuthSteps = AzimuthSteps + result.steps;				
			}
			io.emit('azimuth',AzimuthSteps);
			console.log('New Azimuth Angle: '+AzimuthSteps);
			
		}
		motorHat.steppers[1].releaseSync();
	  });
	})
  
  socket.on('focus', function(angle) {
	
	console.log('Focus:' + angle);
	var focusVal = Math.min(Math.max(parseInt(angle), 0), 100)
	motorHat.servos[0].moveTo(focusVal)

  });
  
  //Whenever someone disconnects this piece of code is executed
  socket.on('disconnect', function () {
    console.log('A user disconnected');
  });


  setInterval(function(){ 
 /* // send temperature every 5 sec
    child = exec("cat /sys/class/thermal/thermal_zone0/temp", function(error, stdout, stderr){
      if(error !== null){
         console.log('exec error: ' + error);
      } else {
         var temp = parseFloat(stdout)/1000;
         io.emit('temp', temp);
//         console.log('temp', temp);
      }
    });*/
	child = exec("sudo iwconfig wlan0 | grep -i --color signal", function(error, stdout, stderr){
      if(error !== null){
         console.log('exec error: ' + error);
      } else {
		 // console.log('Signal:', stdout);
		  var values = stdout.match(/Link Quality=(\d\d\/\d\d)\s\sSignal level=(-\d+ dBm)/);
          if(values.length > 1){
			  var wifi_status = values[1] +' | '+ values[2]
			  io.emit('wifi',wifi_status)
//			  console.log('wifi: ', wifi_status);
		  }
      }
    });
	
  /*  if(!adc.busy){
      adc.readADCSingleEnded(0, '4096', '250', function(err, data){ //channel, gain, samples
        if(!err){          
          voltage = 2*parseFloat(data)/1000;
          console.log("ADC: ", voltage);
          io.emit('volt', voltage);
        }
      });
    } 

	trigger.trigger(10, 1); // Set trigger high for 10 microseconds
	*/
  }, 5000);

});

http.listen(port, function(){
  console.log('listening on *:' + port);
});

function convertToDMS(dd){
	var dir = dd < 0
	
	var absDD = Math.abs(dd);
	var deg = absDD | 0;
	var frac = absDD - deg;
	var min = (frac * 60) | 0;
	var sec = frac*3600 - min * 60;
	sec = Math.round(sec*100) /100;
	var DMS = new Array();
	deg = (dir ? -deg : deg);
	DMS['deg']=deg;
	DMS['min']=min;
	DMS['sec']=sec;
    return DMS;
}
