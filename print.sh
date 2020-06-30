#!/bin/bash
echo "" > /dev/ttyUSB0
echo -en "\x1B\x21\x00---[[[ Dein Logout-Token lautet: ]]]---" > /dev/ttyUSB0
echo "" > /dev/ttyUSB0
echo "" > /dev/ttyUSB0
echo "" > /dev/ttyUSB0
echo -en '\x1B\x21\x39' > /dev/ttyUSB0
echo $1 > /dev/ttyUSB0
echo "" > /dev/ttyUSB0
echo "" > /dev/ttyUSB0
echo "" > /dev/ttyUSB0
echo "" > /dev/ttyUSB0
echo -en "\x1B\x21\x00 -  - Danke dass du da warst! <3 -  - -" > /dev/ttyUSB0
#schneiden
echo "" > /dev/ttyUSB0
echo "" > /dev/ttyUSB0
echo "" > /dev/ttyUSB0
echo "" > /dev/ttyUSB0
echo "" > /dev/ttyUSB0
echo -en '\x1D\x56\x30' > /dev/ttyUSB0

