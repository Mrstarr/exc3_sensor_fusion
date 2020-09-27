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
<br>
You can check if they are close. Also, one improvement can be done by changing the both orientation vector into quaternion
for it's the original data output.However, there is some uncertainty there so I tend to leave it as a question. 


#Report
