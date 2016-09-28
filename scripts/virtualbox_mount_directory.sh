#!/bin/bash

docker-machine.exe stop

"C:/Program Files/Oracle/VirtualBox/VBoxManage" sharedfolder add default -name win_share -hostpath $PWD

docker-machine.exe restart

docker-machine ssh default "sudo mkdir /VM_share; sudo mount -t vboxsf win_share /VM_share"