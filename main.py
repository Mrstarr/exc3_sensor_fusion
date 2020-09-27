from rosbag import * 
from geometry_msgs.msg import Pose,Twist
from nav_msgs.msg import Odometry 
import numpy as np
import tf
import math


def gnss_to_statewithcovariance(gnss):
    """
    From pose data to model state (x,y,z,angle_x,angle_y,angle_z)
    * From GNSS we have orientation_x = oritentation_y = 0 which means rotation vector is (0,0,theta) * 
    * Strange. Position z is changing, which means car doesn't move in a plane * 
    """
    pose = gnss.pose.pose
    p_x = pose.position.x
    p_y = pose.position.y
    p_z = pose.position.z
    o_x = pose.orientation.x
    o_y = pose.orientation.y
    o_z = pose.orientation.z
    o_w = pose.orientation.w
    r =o_x**2 + o_y**2 + o_z**2
    if o_w == 0:
        return None,None
    theta = math.atan2(o_z,o_w)
    state = np.array([p_x,p_y,p_z,0,0,2 * theta])
    # from 1 * 6 matrix to 6 * 1 matrix
    measure_error = np.reshape(gnss.pose.covariance,(6,6))
    return np.transpose(state),measure_error

def odom_to_motionwithcovariance(odom):
    """
    from odom data to control input (vx,vy,vz,ax,ay,az)
    typically from Odometry, we have vy = vz = ax = ay = az =0
    * This is possibly because only linear x is measured *
    * So based on odometry data, angle_z , i.e., theta is never changed *
    * So we need find another to calculate theta *

    *** THE WAY I THINK IS ***
    *** incorporate IMU ? ***
    """
    twist = odom.twist.twist
    lx = twist.linear.x
    ly = twist.linear.y
    lz = twist.linear.z
    ax = twist.angular.x
    ay = twist.angular.y
    az = twist.angular.z
    u = np.array([lx,ly,lz,ax,ay,az])
    motion_error = np.reshape(odom.twist.covariance,(6,6))
    return np.transpose(u),motion_error


def imu_to_motionwithcovariance(imu):
    """
    from imu data to control input (0,0,0,ax,ay,az)
    For now, linear acceleration is not used
    """
    ax = imu.angular_velocity.x
    ay = imu.angular_velocity.y
    az = imu.angular_velocity.z
    motion_error = np.zeros((6,6))
    error = np.reshape(imu.angular_velocity_covariance,(3,3))
    motion_error[3:6,3:6] = error
    u = np.array([0,0,0,ax,ay,az])
    return u,motion_error



class Kalman:
    """
    Classic Kalman Filter
    """
    def __init__(self,bagname):
        self.bagname = bagname         
        self.mean = None
        self.cov = None
        

    def kalm(self):
        #run bag
        bag = Bag(self.bagname)
        it = 0 
        # judge whether initialized or not
        init = False
        for topic, msg, t in bag.read_messages():
            it = it + 1
            # initalize mean and covariance
            if self.mean is None:
                if topic =='/gnss':
                    self.mean,self.cov = gnss_to_statewithcovariance(msg)
            else:
                # if one odom control signal comes
                if topic == '/odom':
                    # from odom data to motion and motion_error
                    ut,motion_error = odom_to_motionwithcovariance(msg)
                    # estimate mean
                    self.mean = self.est_mean(self.mean,ut,0.25)
                    # estimate covariance
                    self.cov = self.est_cov(self.cov,motion_error,0.25) 
                # if one imu control signal comes
                
                if topic == '/imu':
                    ut,motion_error = imu_to_motionwithcovariance(msg)
                    self.mean = self.est_mean(self.mean,ut,0.01)
                    self.cov = self.est_cov(self.cov,motion_error,0.01)
                
                # if one measurement comes
                if topic =='/gnss':
                    # from gnss data to measurement and measurement_error
                    measure,measure_error = gnss_to_statewithcovariance(msg)
                    # calculate kalman gain
                    kalman_gain = self.gain(self.cov,measure_error)
                    #print(kalman_gain)
                    print('estimate positon=')
                    print(self.mean)
                    print('measurement=')
                    print(measure)
                    # update mean and covariance
                    self.mean = self.update_mean(kalman_gain,measure,self.mean)
                    self.cov = self.update_cov(kalman_gain,self.cov)


    def est_mean(self,mt,ut,t):
        """
        estimate the mean pose from mean_t-1 , u_t and time 
        what's B_t in equation ?
        """  
        theta = mt[5]
        ut[0]= math.cos(theta) * ut[0]
        ut[1]= math.sin(theta) * ut[0]
        # Step 1: mu_t = A_t * mu_(t-1) + B_t * u_t 
        # B_t in our case should be ([cos(theta),0...0], [sin(theta),0...0], [0...0], [0...0], [0...0], [0...0])
        # IS THAT TRUE?
        m = mt + t * ut
        return m
    

    def est_cov(self,cov,motion_error,t):
        """
        I think motion error should be t* twist_covariance
        """
        # Step 2: cov_t = A * cov_(t-1) * A_trans + R_t
        cov = cov + t * motion_error
        return cov

    
    def gain(self,cov,measure_error):
        # Step 3: K_t = cov_t * C_t.trans * (C_t * cov_t * C_t.trans + Q_t).inv
        # inv = (C_t * cov_t * C_t.trans + Q_t).inv
        """
        I am not sure if it 's OK I use pseudo-inverse here
        """
        inv = np.linalg.pinv(cov + measure_error)
        # K_t = cov_t * C_t.trans * inv
        gain = cov.dot(inv)
        return gain
    

    def update_mean(self,gain,measure,m):
        # Step 4 mu_t_update = mu_t + K_t * (z_t - C_t * mu_t)
        m_update = m + gain.dot(measure - m)
        # a BRUTAL way to incorporate the change of theta
        # m_update[5] = measure[5]
        return m_update


    def update_cov(self,gain,cov):
        # Step 5 cov_update =(I - K_t) * cov 
        I = np.identity(6)
        cov_update = (I - gain).dot(cov)
        return cov_update

est = Kalman('data.bag')
est.kalm()
