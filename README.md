# Readme
This is the third training exercise from KTH formula team in topic of sensor fusion and Kalman filter<br>
## To run the code : 
download the file and open two terminals in file repository<br>
in first one :<br>
```
~ roscore
```
in second one : <br>
```
~ python main.py
```
## Output
- the estimation of state (Position vector(x,y,z),Orientation vector(x,y,z))<br>
- the measurement of state from gnss (Position vector(x,y,z),Orientation vector(x,y,z))<br>
- You can check if they are close<br>
- An improvement should change the both orientation vector into quaternion,<br>
- But I am a little bit not sure about this and questions remains<br>
