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

## About coding
The coding itself is 100 % self-written. I take the website https://kthfs-dv.gitbook.io/slam/sensor-fusion mainly as my reference and apply simple Kalman filter to do the estimation. The total amount of time I spent is close to 6(Saturday)+ 2(Sunday)=8 hours excluding time to reading the stuff.<br>
The five steps of the filter are represented by five functions. I also write three function to transform /gnss,/imu,/odom data to seperately, measurement and state vector. More details could be seen inside my code. Besides, I also added some thinking during the coding which might be true or wrong.<br>
The date comes from gnss,imu and odom is more difficult to work on than the filter itself, in my opinion.<br>
<br>
## Answers to questions in sensor fusion
#### 1.What are the main differences between Kalman Filter and Extended Kalman Filter?<br>
The equation to calculate mean and covariance is linear in Kalman Filter. While in EKF, the equation is nonlinear,for example, m_t = h(m_t-1,ut)<br>
#### 2.How to take into account several sensors using Kalman filtering?
One way is to do update or estimation several times, if the information from sensors is not overlapped. By overlap, I mean the data is complementary and does not conflict with each other, which is the case in our task. 
Another way could use the idea of particle filter. We build several models with different measurement and estimation method, and give them each a value of importance factor.<br>
#### 3.How can we tune the behaviour of such filters?
Not quite sure about the meaning of 'behaviour'. Generally, pick the most fit filters, build good models from the dynamics and environment, avoid overdrifting by good planning work. My idea of this question is based on the Kalman filter in the task, which doesn't really have some parameters to adjust. Maybe we can discuss it later in the interview.

## Quiz
#### Which category is the most important in the Business Plan Presentation?
In terms of score, **Content**.
#### The driver must be able to leave the car quickly in an emergency. What does the regulations state about driver egress time?
Egress is considered complete when the driver stands next to the car both feet on the ground.
#### Is it okay to adjust the angle of the winglets after technical inspection?
Yes
#### How many lateral g's are simulated during the tilt test?
sqrt(3)/2 g
#### How should the DV log data during the race?
#### What level of wireless communication with the vehicle (exclusing Remote Emergency System) is allowed during the race?
