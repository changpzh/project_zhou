##nodejs
###Installation:
####1st. install compiling tools
```
- $ sudo apt-get install g++ curl libssl-dev apache2-utils
- $ sudo apt-get install python
- $ sudo apt-get install build-essential
- $ sudo apt-get install gcc
- $ sudo apt-get install g++
- $ sudo apt-get install libkrb5-dev
```
####2nd. download node source files and install Nodejs
```
wget https://nodejs.org/dist/v6.10.3/node-v6.10.3.tar.gz
- $ tar -zxf node-v6.10.3.tar.gz
- $ cd node-v6.10.3
- $ ./configure
- $ make
- $ sudo make install
```
###Usage:
- $node --version
- $npm --version
- $npm init		--will create file of package.json file
- $npm install	--will install all package in package.json file.
- d. Config proxy for npm, and check conifg:
    - $ npm config set proxy http://10.144.1.10:8080
    - $ npm config set https-proxy http://10.144.1.10:8080
    - $ npm config list
	
##grunt
###Installation:
```
- $sudo npm install grunt --save-dev	---must install it as --save-dev will add grunt as a dev-dependency to your package.json.
- $sudo npm install -g grunt-cli
- $npm install grunt-contrib-uglify --save-dev  ------»ìÏý´úÂë
- $npm install grunt-contrib-qunit --save-dev
- $npm install grunt-contrib-concat --save-dev  
- $npm install grunt-contrib-jshint --save-dev
- $npm install grunt-contrib-watch --save-dev   
- $npm install connect --save-dev
```
###Config:

###Usage:
- $grunt
- $grunt watch
	
		

##karma & jasmine
###install karma
- $ npm install karma --save-dev
- $ npm install karma-coverage --save-dev
- $ npm install karma-jasmine karma-chrome-launcher jasmine-core --save-dev
- $ sudo npm install -g karma-cli
- $ npm install jasmine --save-dev
###Config:
1:use "$karma init" to generate karma.conf.js
2: edit this file.
###Usage:	
$ karma start		--start karma test in project dir by
###reference
-link: http://karma-runner.github.io/1.0/intro/installation.html

##http-sever
### what is it? ---http-server is a simple, zero-configuration command-line http server
###Installation:
$npm install http-server -g

###Usage:
$http-server [path] [options]
[path] defaults to ./public if the folder exists, and ./ otherwise.
Now you can visit http://localhost:8080 to view your server

Available Options:
-p Port to use (defaults to 8080)
-a Address to use (defaults to 0.0.0.0)

###reference
-link: https://github.com/indexzero/http-server


##bower
###Installation:
$npm install -g bower
###Usage:
$bower install [package]  
-will install it to ./bower_components/    

==========================================
###xclip will copy content
```
$ xclip -sel clip < ~/.ssh/id_rsa.pub
```
