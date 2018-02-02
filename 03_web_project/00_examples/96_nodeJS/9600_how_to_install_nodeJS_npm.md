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
