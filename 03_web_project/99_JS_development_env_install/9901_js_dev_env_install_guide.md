## nodejs
### Installation:
#### 1st. install compiling tools
```
- $ sudo apt-get install g++ curl libssl-dev apache2-utils
- $ sudo apt-get install python
- $ sudo apt-get install build-essential
- $ sudo apt-get install gcc
- $ sudo apt-get install g++
- $ sudo apt-get install libkrb5-dev
```
#### 2nd. download node source files and install Nodejs
```
wget https://nodejs.org/dist/v6.10.3/node-v6.10.3.tar.gz
- $ tar -zxf node-v6.10.3.tar.gz
- $ cd node-v6.10.3
- $ ./configure
- $ make
- $ sudo make install
```
### Usage:
- $node --version
- $npm --version
- $npm init		--will create file of package.json file
- $npm install	--will install all package in package.json file.
- d. Config proxy for npm, and check conifg:
    - $ npm config set proxy http://10.144.1.10:8080
    - $ npm config set https-proxy http://10.144.1.10:8080
    - $ npm config list

## grunt
### Installation:
```
- $sudo npm install grunt --save-dev	---must install it as --save-dev will add grunt as a dev-dependency to your package.json.
- $sudo npm install -g grunt-cli
- $npm install grunt-contrib-uglify --save-dev
- $npm install grunt-contrib-qunit --save-dev
- $npm install grunt-contrib-concat --save-dev
- $npm install grunt-contrib-jshint --save-dev
- $npm install grunt-contrib-watch --save-dev
- $npm install connect --save-dev
```
### Config:

### Usage:
- $grunt
- $grunt watch

## karma & jasmine
### install karma
- $ npm install karma --save-dev
- $ npm install karma-coverage --save-dev
- $ npm install karma-jasmine karma-chrome-launcher jasmine-core --save-dev
- $ sudo npm install -g karma-cli
- $ npm install jasmine --save-dev
### Config:
1:use "$karma init" to generate karma.conf.js
2: edit this file.
### Usage:
$ karma start		--start karma test in project dir by
### reference
-link: http://karma-runner.github.io/1.0/intro/installation.html

## http-sever
### what is it? ---http-server is a simple, zero-configuration command-line http server
###Installation:
$npm install http-server -g

### Usage:
$http-server [path] [options]

[path] defaults to ./public if the folder exists, and ./ otherwise.
Now you can visit http://localhost:8080 to view your server

Available Options:
-p Port to use (defaults to 8080)
-a Address to use (defaults to 0.0.0.0)

### reference
-link: https://github.com/indexzero/http-server


## bower
### Installation:
$npm install -g bower
### Usage:
$bower install [package]
-will install it to ./bower_components/

==========================================
### xclip will copy content
```
$ xclip -sel clip < ~/.ssh/id_rsa.pub
```
## Windows OS:
### How to install nodeJS

- 1: download nodejs.msi in https://nodejs.org
- 2: install it by regular package installation, npm will auto install while nodejs - installation.
- 3: check version by using node -v and npm -v.
- 4: excute file though "node file.js"

## Linux OS:
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
### OR
you can see information of ubuntu nodejs installation from offical [link](www.nodejs.org)

## node version control
`
$ npm install -g n
`
### Installing Binaries
Install a few nodes ("v" is optional), the version given becomes the active node binary once installation is complete.
`
$ n 0.2.6
$ n v0.3.3
`
https://www.npmjs.com/package/n2

##NPM usage
### How to use npm

- 1: use "`npm init`" in one project dir, to create a project, one more file "package.jason" will created.
- 2: use "`npm install XXX --save-dev`" in that project to install third package.
- 3: 全局安装用 `-g` 参数， 比如：`npm install -g learnyounode`
- 4: npm 安装指定版本可在模块后面加`@version_numer`, 比如`npm install -g mocha@2.5.3`


**Notes**

* `--save` : 表示把模块安装后同时写到package.json的dependencies里面
* `--save-dev`: 表示把模块安装后同时写到package.json的**dev**Dependencies里面

### [Fixing npm permissions](https://docs.npmjs.com/getting-started/fixing-npm-permissions)
Change the permission to npm's default directory

- Find the path to npm's directory:

	`$ npm config get prefix`  

For many systems, this will be **/usr/local**

**WARNING: If the displayed path is just /usr, switch to Option 2 or you will mess up your permissions.**

- See what is current user:

	`$ whoami`

- Change the owner of npm's directories to the name of the current user (your username!):

	`$ sudo chown -R $(whoami) $(npm config get prefix)/{lib/node_modules,bin,share}`
