# Welcome to Chalens!

This is a wireless ecosystem analysis app to help find the most suitable channel for each moment. It was part of a final year degree thesis but I am still working on it whenever I have some free time. Any fork or use of the app is welcome, feel free to do with it as you please. But take into account, it uses a modification I made to Trackerjacker to run so maybe some kind of reference may be needed. 


## Current state

Currently, the app works correctly within a Raspberry Pi 4. However, any Linux based device should be fine.


## Set up
**IMPORTANT!** The app modifies the device's configuration, everything must be executed as root, so take care ;) Also, it is required to have a network card compatible with monitor mode (YOU will need to change the interface specified within the code. It is easy, do it in the scan.py and selector.py files)
With the help of the bash files: runChalens.sh and installChalens.sh you should be on the go pretty fast. 
