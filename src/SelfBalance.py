#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 18:08:40 2017

@author: sezan92
"""
import sys,time
import pidcontrol as pid
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu
Kp =1000
Ki =0.1
Kd =0.1


pubx = pid.PID_Controller(Kp,Ki,Kd)
cmd_vel = "/cmd_vel"
Imu_topic = "/imu"
class SelfBalance:
    def __init__(self):
        self.pub = rospy.Publisher(cmd_vel,Twist,queue_size =1)
        self.subscriber = rospy.Subscriber(Imu_topic,Imu,self.callback)
    def callback(self,data):
        setPoint = 0
        y = data.orientation.y
        vel = Twist()
        vel.linear.x = -pubx.getCorrection(setPoint,y)
        vel.linear.y = 0
        vel.linear.z = 0
        vel.angular.x =0
        vel.angular.y = 0
        vel.angular.z = 0
        self.pub.publish(vel)
        print " Error " + str(y)+ " Radian"
        
        

def main(args):
    '''Initializes and cleanup ros node'''
    rospy.init_node('SelfBalance', anonymous=True)
    ic = SelfBalance()
    
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down ROS "
    

if __name__ == '__main__':
    main(sys.argv)