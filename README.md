<h1 align="center">ROV Raspberry Pi Camera script</h1> 

### What is it
scripts that utilizes the ***Gstreamer*** API to send and recieve video streams from the Rov camera system to the topside computers over an IP network with ID 192.168.2.X

The ROV camera system is comprised of the raspberry PI and some USB cams connected to said PI, which the sender scripts detects and streams data from to the broadcast IP of subnet 192.168.2.X

On the other end we have laptops setup with a reciever script that recieves streams from the appropriate port

### Usage
To use the sender script make sure you installed python3 and gstreamer for your linux system and that's as far as setting your environment goes.

 - make sure your cameras are connected to the PI
 - make sure you are runnning the appropriate reciever script on the recieving devices
 - Some of the code here requires a custom compiled Opencv that has gstreamer enabled for the backend use

### TODO:

 - [X] write the damned thing
 - [X] test it
 - [X] exception handling for camera errors
 - [ ] run script on Pi startup 
 - [X] support for multi-device broadcasting
 - [ ] better optimized pipline for H.264 encoding
 - [ ] write a reciever script using opencv not gstreamer
 - [ ] remove uneeded print statements and debug info


 ### Notes:

 note to self : if we use a half decent router as the switch for this home network it probably won't work as the switch will instantly block the streams coming in from the broadcast IP