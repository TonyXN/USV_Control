# USV_Control

## Getting started

Build:

```
catkin_make

source devel/setup.bash
```

Run(For LinkTrack):

```
rosrun nlink linktrack_publisher /dev/ttyUSB0 921600

```

Notice: please use port name and baud rate of your device instead.

Known issue

- Run failed, show "Unhandled Exception: IO Exception (13): Permission denied, file ... ", permission needs to be changed.

Edit file

```
sudo gedit /etc/udev/rules.d/70-ttyusb.rules
```

append

```
KERNEL=="ttyUSB[0-9]*",MODE="0666"
```

Then replug the device, try again.
