# auto_rotation_hdaps

## What it accomplishes

This application adds auto-rotation functionality to tablet/laptop devices with Linux that have HDAPS accelerometers such as the X201 tablet Thinkpad. 
It does this by reading data exposed by the HDAPS driver, from the accelerometer, to determine the correct orientation to rotate the screen and touch matrix. 

## Compatability

Currently, it is only for certain that this application works with the x201 Tablet Thinkpad. I suspect that it will work with any HDAPS-using device(a quick 
google search of your device can determine whether it uses the HDAPS drivers); however, this is not gauranteed. 

## Installing

1. First, you need to make sure you have the hdaps driver installed. Your particular linux distribution may have it as a package. If not, you will need to install from source. [tp_smapi](https://github.com/linux-thinkpad/tp_smapi) is the driver package for Thinkpads.
2. Clone repository onto your machine
3. Move both `auto_rotate.py` and `tablet_mode_detection.py` into your `/usr/bin`
4. Add the HDAPS driver kernal module by executing command `echo hdaps > /etc/modules-load.d/hdaps.conf`
5. Restart your machine and test the application out by running `auto_rotate.py` in a terminal
6. If all seems to be working as it should, add `auto_rotate.py` to your desktop environment's autostart section, or add `auto_rotate.py &` to your `~/.xinitrc` file. This will ensure that auto rotation works upon startup. 
7. Enjoy. 

## Arch Linux

If you're using arch, you can download the [PKGBUILD here](https://aur.archlinux.org/packages/auto-rotation-hdaps-git)


