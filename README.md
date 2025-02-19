Mesa Configuration Tool II

The Mesa Configuration Tool works with most Debian and Debian based Operating
Systems that meet the Python and PyQt5 minimum versions including the Raspberry
Pi with the exception of Raspbian 10. If you use a special version like from
Rod W on the forum you may encounter problems because he does not provide a
standard Python liberary kit.

Requirements:
Debian 11 OS or newer (might work on Ubuntu but not supported)
Python Version 3.6 or newer (formatted string literals)\
PyQt5 Version 5.15.0 or newer (QTabWidget.setTabVisible() Debian 11 or up)

Installation Instructions are [here](https://gnipsel.com/linuxcnc/mesact/index.html)

To run from a terminal you need to install some depenencies:\
sudo apt install python3-pyqt5\
sudo apt install python3-distro\
sudo apt install python3-requests\
sudo apt install zip

Then in the /mesact/src directory open a terminal and run with ./mesact

The old Mesa Configuration Tool is located at https://github.com/jethornton/mesact1

