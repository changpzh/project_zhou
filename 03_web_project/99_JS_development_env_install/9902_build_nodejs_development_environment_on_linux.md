## How to build development environment on Linux?


Step 1. Download Oracle VirtualBox for Windows hosts from https://www.virtualbox.org/wiki/Downloads, and install it  
Step 2. Download Ubuntu 14.04.2 LTS 64-bit ISO from http://www.ubuntu.com/download/desktop, Long Term Support (LTS) version is preferred  
Step 3. Enable VT-x/AMD-V virtualization support in your PC BIOS (Otherwise you can't install 64-bit linux)  

Step 4. Start VirtualBox Manager (reference: http://www.crifan.com/crifan_recommend_virtual_machine_soft_virtualbox/)  


Click New - >select linux -> Ubuntu 64 bit -> Next  
Input virtual Momory size (I assign 3096)  
Create virtual disk. At least 20G. (I create 30G size disk)  
Config your Virtual computer:  


a.Add Ubuntu 14.04.2 ISO into CDROM.  
b.Enable copy/paste.  
c.Set Graph memory size.  
d.Set CPU count  
e.Enable network  


#### Start the virtual computer your just created and install Ubuntu.
Make sure network is workable. If you're doing this in office network, select "Try Ubuntu" on install start page, set proxy in "System Settings", then click Install Ubuntu on desktop.  
Install VirtualBox Guest Additions on Virtualbox manager menu to enable cliboard/folder sharing and get better screen resolution.  
Enable root user and set password for root  

sudo passwd -u root  
sudo passwd root  


#### Switch to root user and add proxy settings in ~/.bashrc:

export http_proxy=http://10.144.1.10:8080  
export https_proxy=http://10.144.1.10:8080  


#### Configure proxy for apt (Advanced Package Tool) with 'root@ubuntu:~# vim /etc/apt/apt.conf':  

Acquire::http::proxy "http://10.144.1.10:8080";  
Acquire::ftp::proxy "ftp://10.144.1.10:8080";  
Acquire::https::proxy "https://10.144.1.10:8080";  


#### Restart your Virtual computer to continue



### Step 5. application install


a. Install git by command : sudo apt-get install git  
b. Install Nodejs  

1. firstly，install compiling tools  
$ sudo apt-get install g++ curl libssl-dev apache2-utils  
$ sudo apt-get install python  
$ sudo apt-get install build-essential  
$ sudo apt-get install gcc  
$ sudo apt-get install g++  
$ sudo apt-get install libkrb5-dev  
2. download node source files and install Nodejs  
wget https://nodejs.org/dist/v6.12.2/node-v6.12.2.tar.gz  
- $ tar -zxf node-v6.12.2.tar.gz  
- $ cd node-v6.12.2  
- $ ./configure  
- $ make  
- $ sudo make install  


c. Clone 5g Source code by command:  

$ git clone git@baltig.nsn-net.net:5g/nodeoam.git  
(Need add your SSH key(find it ~/.ssh/id_rsa.pub) into Gitlab profile first)  


d. Config proxy for npm, and check conifg:  

$ npm config set proxy http://10.144.1.10:8080  
$ npm config set https-proxy http://10.144.1.10:8080  
$ npm config list


e. Switch to ./nodeoam folder and run command npm install, this will install all dependencies listed in package.json  
g. npm start  

### install webstorm
download linux version of webstorm from offical location

create a new dircetory of webstorm in /usr/share as root user  
`# mkdir /usr/share/webstorm`  
then umcompress it your dir previous created.  
`# tar zxvf WebStorm-11.0.3.tar.gz -C /usr/share/webstorm`

create a symbol link of webstorm.sh in your /usr/share/webstorm/.*/bin/webstorm.sh
