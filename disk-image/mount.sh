#!/bin/bash

name=$(sudo fdisk -l  parsec| tail -1 | awk -F: '{ print $1 }' | awk -F" " '{ print $1 }')
start_sector=$(sudo fdisk -l parsec | grep $name | awk -F" " '{ print $3 }')
units=$(sudo fdisk -l parsec | grep Units | awk -F" " '{ print $9 }')

echo "name = $name"
echo "start_sector = $start_sector"
echo "unit = $units"
sudo mount -o loop,offset=$(($start_sector*$units)) parsec disk_mnt

#name=parsec-aarch64-ubuntu-trusty-headless.img
##name1=parsec-aarch64-ubuntu-trusty-headless.img1
#start_sector=$(sudo fdisk -l $name | grep $name | awk -F" " '{ print $2 }')
#units=$(sudo fdisk -l  $name  | grep ^Units | awk -F" " '{ print $8 }')
#sudo mount -o loop,offset=$(($start_sector*$units)) $name disk_mnt
