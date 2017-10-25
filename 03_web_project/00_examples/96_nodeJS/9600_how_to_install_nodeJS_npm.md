Windows OS:
How to install nodeJS
1: download nodejs.msi in https://nodejs.org
2: install it by regular package installation, npm will auto install while nodejs installation.
3: check version by using node -v and npm -v.
4: excute file though "node file.js"
How to use npm

1: use "npm init" in one project dir, to create a project, one more file "package.jason" will created.
2: use "npm install XXX --save-dev" in that project to install third package.
	- notes: --save-dev: used to save third package to package.jason 

Linux OS:
	Install Nodejs
		1. firstly，install compiling tools
		$ sudo apt-get install g++ curl libssl-dev apache2-utils
		$ sudo apt-get install python
		$ sudo apt-get install build-essential
		$ sudo apt-get install gcc
		$ sudo apt-get install g++
		$ sudo apt-get install libkrb5-dev
		2. download node source files and install Nodejs
		wget https://nodejs.org/dist/v0.10.34/node-v0.10.34.tar.gz
		$ tar -zxf node-v0.10.34.tar.gz
		$ cd node-v0.10.34
		$ ./configure
		$ make	---it make take a long time.
		$ sudo make install
	Config proxy for npm if needed, and check conifg:
	    $ npm config set proxy http://10.144.1.10:8080
	    $ npm config set https-proxy http://10.144.1.10:8080
	    $ npm config list
	Delete proxy of npm
	    $ npm config delete proxy
	    $ npm config delete https-proxy
###OR
you can see information of ubuntu nodejs installation
http://jingyan.baidu.com/article/6181c3e080f979152ef15387.html
