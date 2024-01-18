#!/bin/bash

echo ""
echo "Preparing Spin to use parallel executions..."
echo ""
sudo /sbin/sysctl kernel.shmmax=6442450944
sudo /sbin/sysctl kernel.shmall=1572864
echo ""
echo "Done!"
echo ""