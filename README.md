<h1>ROV Raspberry Pi Camera script</h1> 

### Tech
scripts that utilizes the ***Gstreamer*** API to send and recieve Stream data from the Rov camera system to the topside computers over an IP network with ID 192.168.2.X

### TODO:

 - [ ] write a reciever script using opencv not gstreamer
 - [ ] better optimized pipline for H.264 encoding
 - [ ] run script on Pi startup 
 - [ ] support for multi-broadcasting
 - [ ] **exception handling for camera errors**
    - [X] write the damned thing
    - [ ] test it
 - [ ] remove all print statements and debug info