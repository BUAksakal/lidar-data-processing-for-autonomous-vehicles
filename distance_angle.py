#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author:Berke Uğur Aksakal

import rospy
from sensor_msgs.msg import LaserScan
import os

def lidar_data(veri):

    angle_min = veri.angle_min
    angle_max = veri.angle_max
    angle_increment = veri.angle_increment

    relevant_ranges = veri.ranges[0:120]  # İlk 120 lazer ışını

    for i, distance in enumerate(relevant_ranges): #  i  = index of value , x  = value --> enumerate()
        if distance < 3.5:
            
            # Gelen açı sayısına bağlı olarak açıyı hesapla
            num_angles = len(relevant_ranges)
            total_angle = angle_max - angle_min
            angle_per_measurement = total_angle / num_angles

            # İndex ile açıyı hesapla
            angle_of_measurement = angle_min + (i * angle_per_measurement)

            # Cismin kapladığı açıyı hesapla
            covered_angle = 120 - angle_of_measurement

            print("Mesafe: {:.2f}, Açı: {:.2f} derece, Kapladığı Açı: {:.2f} derece".format( distance, angle_of_measurement, covered_angle))
            save_to_file(i, distance, angle_of_measurement, covered_angle)
        else:
            print("Uyarı: Gelen veri 0 ile 120 derece arasında değil.")

def save_to_file(index, distance, angle, covered_angle):
    file_name = "lidar_distances.csv"
    with open(file_name, "a") as file:

        # Her 120 ölçüm sonrasında boşluk bırakarak değerleri yaz 
        file.write("index: {}, distance: {:.2f}, angle: {:.2f}, covered angle: {:.2f}\n".format(index, distance, angle, covered_angle))

        if (index + 1) % 120 == 0:
            file.write("\n")

if __name__ == '__main__':
    rospy.init_node('tb3_lidar', anonymous=True)
    
    file_name = "lidar_distances.csv"
    with open(file_name, "w") as file:
        file.write("Mesafe, Açı, Kapladığı Açı\n")
    
    rospy.Subscriber('/scan', LaserScan, lidar_data) # subscriber to /scan 
    rospy.spin()