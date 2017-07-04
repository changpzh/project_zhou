# README

* [1. Overview](#link_1 "Overview about COOP")
* [2. Files Tree](#link_2 "Coop source code structure")
* [3. Understand the metrics definition and relevant data model](#link_3)
* [4. Post data for coop](#link_4)
* [5. Raw data in MongoDB](#link_5)
* [6. An example of API development](#link_6)
* [7. Installation And Deployment](#link_7 "Installation And Deployment")
* [8. Testing and deployment](#link_8)
* [9. Maintenance](#link_9)
* [10. Learning Resources](#link_10)
* [11. About Glossary](#link_11)
* [12. PCI interface](#link_12)
* [A.1 How to Build Coop develop environment on Win7 ?](#link_a1 "setup coop develp environment")
* [A.3 Collection's Index](#link_a3 "List index for each collection")
* [A.4-1 How to get CRT trigger?](#link_a41 "How to get CRT trigger?")
* [A.4-2 How to get PCI promotion trigger?](#link_a42 "How to get PCI promotion trigger?")
* [A.5 How to get builds?](#link_a5 "How to get builds?")
* [A.6 How to get SCCI data?](#link_a6 "How to get SCCI data")
* [A.7 How to get PCI build data?](#link_a7 "How to get build data")
* [A.8 SC contacts](#link_a8 "SC contacts")
* [A.9 How to restart MongoDB on coop/testcoop?](#link_a9 "restart mongodb")
* [A.10 How to create merge request?](#link_a10 "merge request")

<a name="link_1" id="link_1"></a>
### 1. Overview
COOP is developing for the Synergistic Continuous Integration data visualization purpose. As we know, during software continuous integration process, there are a lot of data will be generated, but the data is distributed in too many places, it's hard to provide continuous integration healthy insights. Actually, we can gather such data, and making the whole continuous integration situation visibility. Identify the metrics and statistics, offer the insight opportunities to R&D management.

This project is sponsored by TD-LTE CPD team, its implementation is [MEAN](http://mean.io/#!/ "meanio")-based. You can access [http://coop.china.nsn-net.net](http://coop.china.nsn-net.net "falcon") to see the live falcon project demo.

#### 1.1 Application architecture

The application architecture is illustrated as below:

![Alt text](frontend/img/COOP.Design.png "COOP architecture")

- 1. data provider: it can be a target SC SCM or product CI's any stage's owner, for example, it can be TDD_CPRI_HANDLER software component SCM, QT testing team's portal.
- 2. Receiver: it's a Express application which is running on the application server, to handle the data provider POST data, for example, `EventStore` once receive the POST data from data provider, it will store the raw data into `Events` database.
- 3. Events database: it's a mongoDB database, it's used to store all the raw data from data provider for further processing.
- 4. Status Report Database: this database stored the data which has been proccessed, this part of data will be used for the CI status chart render (note: status does not equals metrics)
- 5. Metrics Report Database: this database store the data which has been proccessed as well as status report database. As we mentioned above the raw data is stored in the `Events` database, there are relevant scripts will process the data to apply we defined statistics metrics
- 6. Front-End: as its name meaning, this part about the chart drawing, and html interaction.
- 7. Under developing
- 8. Under developing

<a name="link_2" id="link_2"></a>
### 2. Files Tree

```
`-- atest
 -- documents
 -- frontend
    |-- css
    |-- html
    |-- img
    |-- js
    |-- lib
    |-- index.html
 -- img
 -- producer
    |-- routes
        |-- api
        |-- index.js
    |-- scripts
    |-- test
    |-- app.js
    |-- eventstore.js
 `-- readme.md
```

* `readme.md` is the project introduction
* folder `producer` keeps the source code of the backend, which is used to provide the REST_API for the frontend web usage. It's the [Express](http://expressjs.com/ "expressjs")-based application which is working under <code>port:3000</code>. It's falcon project main application.
* folder `frontend` keeps web site front end source code, such as `*.html`, `*.js` and `*.css`. The data visualization codes are located here, and they are implemented by [d3js](http://d3js.org/ "d3js").

<a name="link_3" id="link_3"></a>
### 3. Understand the metrics definition and relevant data model

#### 3.1. Pipeline section (deprecated)

* Area A: The builds pipeline rough information, each cell to identify the status of specific build and specific stage.
* Area B: Illustrating the stages details of selected build.
* Area C: Illustrating the different stage time costing for specific build.
* Area D: Illustrating the cycle time of the builds which already listed in Area A.
![Alt text](frontend/img/pipeline_overview.png "pipeline")


#### 3.2. WIP (Working In Progress) section (TODO)

#### 3.3 PCI pipeline

The product level CI pipeline is illustrate as below, each row is a specfic build, there are several different stages for one build, the cell indicates the build and stage, and the color means the stage is successful or not. The number float above the cell, to indicate how many problems in this stage. User can click the cell to zoom in the stage's details.

![Alt text](frontend/img/PCI.Pipeline.png "PCI pipeline")


<a name="link_4" id="link_4"></a>
### 4. Post data for coop

#### 4.1. Enable Time Synchronization using NTP

* Pls enable NTP time synchronization for your CI server before posting data for coop.(ref: https://help.ubuntu.com/community/UbuntuTime#Time%20Synchronization%20using%20NTP)

#### 4.2. Post data for coop
* [Integrate SCCI data for coop](http://becrtt01.china.nsn-net.net/cpd/falcon/tree/master/documents/software.component.ci.data.integration.md 'SCCI data integration')
* [Integrate PCI data for coop](http://becrtt01.china.nsn-net.net/cpd/falcon/tree/master/documents/api.pci.common.md 'PCI data integration')

<a name="link_5" id="link_5"></a>
### 5. Raw data in MongoDB
- [Raw data in MongoDB](http://becrtt01.china.nsn-net.net/cpd/falcon/tree/master/documents/raw.data.in.mongodb.md 'raw data')

<a name="link_6" id="link_6"></a>
### 6. An example of API development
- [An Example of API Development](http://becrtt01.china.nsn-net.net/cpd/falcon/tree/master/documents/an.example.of.api.development.md 'api development')

<a name="link_7" id="link_7"></a>
### 7. Installation And Deployment

#### 7.1. Required Components (Assuming on Linux hosts)
* Nodejs: *producer* servers as a nodejs app.
* Mongodb: a NoSQL database
* Nginx: provide web server for contents within *frontend*
* [PM2](https://github.com/Unitech/PM2) (optional): for automatic deployment and run-forever (auto restart on crash), but it's not fully configured, now, a Jenkins/Gitlab CI configuration is needed to build a completed CD system.


#### 7.2. Installation
1. Install components:(You can get the more details information from:  [How to build Coop development environment on Win7?](#link_a1 "How to build Coop development environment on Win7"))
  * Nodejs: https://github.com/joyent/node/wiki/Installing-Node.js-via-package-manager
  * Mongodb: http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/
  * Nginx: `sudo apt-get install nginx`
  * Arangodb: https://www.arangodb.com/download/ (prefer to install by package manage)
  * redis: `sudo apt-add-repository ppa:chris-lea/redis-server; sudo apt-get update; sudo apt-get install redis-server`
  * PM2 (optional): https://github.com/Unitech/pm2
  
        #install pm2 with 'npm install pm2 -g'  
        #stop and delete all pm2 processes(pm2 delete all)  
        #pm2 start pm2.json
        # or 
        #start falcon using 1 instance(pm2 start ./bin/www --name "falcon" --max-memory-restart 4096M --node-args="--max_old_space_size=4096")  
        #start falconReader using 1 instance(pm2 start reader.js --name "falconReader" --max-memory-restart 4096M --node-args="--max_old_space_size=4096")  
1. Check out the code:
  * Generate your ssh key within your development environment by http://gitlab.china.nsn-net.net/help/ssh/README
  * and set it into gitlab http://gitlab.china.nsn-net.net/profile/keys
  * in your working folding, 'git clone http://gitlab.china.nsn-net.net/cpd/falcon.git'
  * install node modules: `cd falcon/producer; npm install`

1. Add a site config (based at folder `falcon/frontend`) to `/etc/nginx/sites-available`, and make a soft link in `/etc/nginx/sites-enabled`, then restart nginx. Example:

        # /etc/nginx/sites-available/falcon.conf
        # Falcon

        server {
          listen *:80 default_server;         # e.g., listen 192.168.1.1:80; In most cases *:80 is a good idea
          server_name coop.china.nsn-net.net;     # e.g., server_name source.example.com;
          server_tokens off;     # don't show the version number, a security best practice
          proxy_redirect off;
          proxy_set_header Host             $host;
          proxy_set_header   X-Real-IP        $remote_addr;
          proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
          proxy_connect_timeout 600;
          proxy_read_timeout 600;
          proxy_send_timeout 600;

          # CHANGE it to the folder in which source code located
          root /path/to/falcon/frontend;

          # individual nginx logs for this gitlab vhost
          access_log  /var/log/nginx/falcon_access.log;
          error_log   /var/log/nginx/falcon_error.log;

          # you can add other service under the same port, distiguish by url path
          #location /ci/ {
          #  proxy_pass http://localhost:8081/ci/;
          #}

          location / {
            # serve static files from defined root folder;.
             index index.html;
          }

          # tell IE to use edge document mode, IE is always the most stupid one
          add_header "X-UA-Compatible" "IE=Edge,chrome=1";
        }
1. Under `falcon/producer`, type `npm start` to run the app. Or, if you use PM2, create an app by PM2 with command `pm2 start`, `pm2 reload`, more instructions please refer to its manual.
1. How to upgrade node:
  * npm cache clean -f
  * npm install -g n
  * n stable
  * node -v  
  and then  
  * rm -rf node_modules
  * npm cache clean
  * npm install
1. How to upgrade pm2(http://pm2.keymetrics.io/docs/usage/update-pm2/):
  * pm2 save
  * npm install pm2 -g
  * pm2 update

<a name="link_8" id="link_8"></a>
### 8. Testing and deployment

#### 1.1 COOP has two types of testing:
```
- 1. Unit Testing with `mocha` framework(e.g. run xxx.js with mocha test/__init__.js test/integration/xxx.js)
- 2. Acceptance Testing with `RobotFramework` and `webdriver`
    - We use `selenium2` and `RobotFramework` to do the acceptance testing, you can refer to [Web Testing Based on RobotFramework and Webdriver](https://docs.google.com/presentation/d/17FyeecnUCA2awrrsovrNBDo3WI1sID9zA1t3RsW0kvw/pub?start=false&loop=false&delayms=3000).
```
#### 1.2 Continuous integration process as below:

![Continuous Integration](frontend/img/COOP.CI.png "COOP Continuous Integration")

1. Developer commit code to gitlab
1. The commit will trigger `unit testing` automatically
1. If the `unit testing` success, the commit will be deployed to `pilot` environment, and trigger `acceptance testing` automatically, `acceptance testing` will run on the `pilot` environment
1. If the `acceptance testing` success, the commit can be deployed to `product` environment manually (by promotion of `cci_falcon`)
1. if the `acceptance testing` success, the unit testing will be triggered on testcoop(`http://coop.china.nsn-net.net/ci/job/testcoop/`), and the commit will be deployed to testcoop environment automatically (you can also deploy it by promotion of `testcoop`)

<a name="link_9" id="link_9"></a>
### 9. Maintenance

- Start arangodb : `root@hztdltev02:/data/arangodb# service arangodb start`
- Start Falcon : `pm2 reload falcon; pm2 reload falconReader`
- Start CI: `root@hztdltev02:/data/ci# start_ci.sh`
- Backup Job: http://coop.china.nsn-net.net/ci/job/cron_db_backup/
- Backup Strategy: daily, and keep the latest 10 copies
- Dumped DB download FTP: ftp://hzogrvm01.china.nsn-net.net/mongo_backup/
- Restore from dumped DB (**NOTE**, it will drop your current database): `mongorestore  --drop "/home/cpd/mongo_backup/$latest_dump"`
- Coop maintenance in .bashrc
  * alias startmongo='mongod --fork --syslog --dbpath /data/db --bind_ip 127.0.0.1'; startmongo
  * alias stopmongo='mongod --shutdown'; stopmongo
  * alias mountpilot='sshfs -o nonempty -o allow_other -o kernel_cache -o auto_cache -o reconnect cpd@hzogrvm01.china.nsn-net.net:/home/cpd/mongo_backup /home/cpd/mongo_backup' ; mountpilot
- mount /home/cpd/mongo_backup on /srv/ftp/mongo_backup
  * ssh to hzogrvm01.china.nsn-net.net
  * mount --bind /home/cpd/mongo_backup /srv/ftp/mongo_backup

<a name="link_10" id="link_10"></a>
### 10. Learning Resources

* [Learning Git](http://pcottle.github.io/learnGitBranching/)
* [The Best Way to Learn JavaScript](http://code.tutsplus.com/tutorials/the-best-way-to-learn-javascript--net-21954)
* [Web Developer Skills](https://www.codecademy.com/learn)
* [MongoDB](https://docs.mongodb.org "MongoDB")
* UT
    * [Mocha](http://mochajs.org/) 
* [Lodash ~4](https://lodash.com/docs "Lodash 4.16.4")
* [d3js](http://d3js.org/ "d3js") for chart drawing, animating on browser
* [ECharts](http://echarts.baidu.com/echarts2/doc/example.html#gauge "EChart") for chart drawing
* [jquery-multiselect-plugin](http://www.jqueryrain.com/demo/jquery-multiselect-plugin/ "jquery-multiselect-plugin")
* [Calendar View](http://bl.ocks.org/mbostock/4063318 "Calendar View")
* [outdatedbrowser](http://outdatedbrowser.com/en/project, "outdatedbrowser 1.1.0")
* [debug on nodejs](https://github.com/node-inspector/node-inspector#quick-start)

<a name="link_11" id="link_11"></a>
### 11. About Glossary

- **SC** stands for Software Component
- **CI** stands for Continuous Integration
- **PCI** stands for Product Continuous Integration system
- **SCCI** stands for Software Component Continuous Integration system
- **SCM**  stands for Software Configuration Management
- **Pipeline**  is an automated manifestation of your process for getting software from version control into the ready to hands package to customer. The whole process maight be including Software Component CI, Product level SCM, Quick Test, Integration and Verification etc. phases, each phase will be called one "stage" here.
- **SCT** stands for Software Component Testing, what is located in SCCI, used to do Software Component regression testing.

<a name="link_12" id="link_12"></a>
### 11. Post Data For PCI 
- [Post Data For PCI ](http://becrtt01.china.nsn-net.net/cpd/falcon/tree/master/documents/api.pci.common.md 'PCI')

### A - Questions and Anwsers
<a name="link_a1" id="link_a1"></a>
#### A.1 How to build Coop development environment on Win7?
- Step 1. Download Oracle VirtualBox for Windows hosts from https://www.virtualbox.org/wiki/Downloads, and install it
- Step 2. Download Ubuntu 14.04.2 LTS 64-bit ISO from http://www.ubuntu.com/download/desktop, Long Term Support (LTS) version is preferred
- Step 3. Enable VT-x/AMD-V virtualization support in your PC BIOS (Otherwise you can't install 64-bit linux)
- Step 4. Start VirtualBox Manager (reference: http://www.crifan.com/crifan_recommend_virtual_machine_soft_virtualbox/)
	* Click New - >select linux -> Ubuntu 64 bit -> Next
	* Input virtual Momory size (I assign 3096)
	* Create virtual disk. At least 20G. (I create 30G size disk)
	* Config your Virtual computer:
		* a.Add Ubuntu 14.04.2 ISO into CDROM.
		* b.Enable copy/paste.
		* c.Set Graph memory size.
		* d.Set CPU count
		* e.Enable network
	* Start the virtual computer your just created and install Ubuntu.
		Make sure network is workable. If you're doing this in office network, select "Try Ubuntu" on install start page, set proxy in "System Settings", then click Install Ubuntu on desktop.
	* Install VirtualBox Guest Additions on Virtualbox manager menu to enable cliboard/folder sharing and get better screen resolution.
  * Enable root user and set password for root
  ```
    sudo passwd -u root
    sudo passwd root
  ```
	* Switch to root user and add proxy settings in ~/.bashrc:
	```
    export http_proxy=http://10.144.1.10:8080
    export https_proxy=http://10.144.1.10:8080
	```
	* Configure proxy for apt (Advanced Package Tool) with 'root@ubuntu:~# vim /etc/apt/apt.conf':
	```
	Acquire::http::proxy "http://10.144.1.10:8080";
    Acquire::ftp::proxy "ftp://10.144.1.10:8080";
    Acquire::https::proxy "https://10.144.1.10:8080";
	```
	* Restart your Virtual computer to continue

- Step 5. Coop application install
	* a. Install git by command : sudo apt-get install git
	* b. Install Nodejs
```
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
		$ make
		$ sudo make install
```
	* c. Clone Coop Source code by command:
```
    $ git clone http://gitlab.china.nsn-net.net/cpd/falcon.git ~/falcon
    (Need add your SSH key into Gitlab profile first: http://becrtt01.china.nsn-net.net/help/ssh/README)
```
	* d. Config proxy for npm, and check conifg:
```
    $ npm config set proxy http://10.144.1.10:8080
    $ npm config set https-proxy http://10.144.1.10:8080
    $ npm config list
```
	* e. Switch to ./falcon/producer folder and run command `npm install`, this will install all dependencies listed in package.json
	* g. Install MongoDB 2.6 (reference url : http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/)
		* Issue the following command to import the MongoDB public GPG Key:
			* sudo -E apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
		* Create list file for MongoDB:
			* echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list
		* Issue the following command to reload the local package database:
			* sudo apt-get update
		* Install the latest stable version of MongoDB. Issue the following command:
			* sudo apt-get install mongodb-org
		* Check Mongodb service by Command:
			* sudo service mongod status
		* Start MongoDB by Command:
			* sudo service mongod start
		* Import mongoDB from dump file
			1. Get mongoDB last dump from link: ftp://hzogrvm01.china.nsn-net.net/mongo_backup/
			2. unzip dump file by command : tar zxvf dump_2016-03-25-003500.tar.gz
			3. import mongoDB by command: mongorestore  --drop dump_2016-03-25-003500
			4. Connect mongoDB by command: mongo 127.0.0.1/pipeline
      
	* h. Install Redis
		* Get Redis by command :wget http://download.redis.io/releases/redis-3.0.1.tar.gz
		* unzip file by command : tar xvzf redis-3.0.1.tar.gz
		* cd redis-3.0.1
		* make
		* make test
		* sudo make install
		* cd utils and run command : sudo ./install_server.sh
		* check Redis service by command: sudo service redis_6379 status
		* Start Redis service by command: sudo service redis_6379 start

	* i. Install ArangoDB (see https://www.arangodb.com/download/)
		* Add the repository key to apt like this:
```		
			wget https://www.arangodb.com/repositories/arangodb2/xUbuntu_14.04/Release.key
			sudo apt-key add - < Release.key
```			
		* Create the /etc/apt/sources.list.d/arangodb.list list file using the following command:
			* echo 'deb https://www.arangodb.com/repositories/arangodb2/xUbuntu_14.04/ /' | sudo tee /etc/apt/sources.list.d/arangodb.list
            * sudo apt-get install apt-transport-https
            * sudo apt-get update
            * sudo apt-get install arangodb=2.8.7
		* Check ArangoDB service by Command:
			* sudo service arangodb status
		* Start ArangoDB by Command:
			* sudo service arangodb start
		* Import ArangoDB from dump file
			* 1. Get arangoDB last dump from link: ftp://hzogrvm01.china.nsn-net.net/arango_backup/
			* 2. unzip dump file by command : tar zxvf coop_arangodb_dump.tar.gz
			* 3. create database falcon by command : 
			* $ arangosh
			* $ db._createDatabase('falcon')
			* 4. import arangoDB by command: arangorestore --server.database=falcon --input-directory=arango_2015-06-04-135805
		* Initiation arangoDB issue following command:
			* cd falcon/producer/scripts
			* node setup_graph.js

- Step 6. Start coop develop environment
	* cd /falcon/producer/
	* node reader.js      	-- Start Coop Redis service
	* npm start				-- Start Coop Data API service:  Access http://127.0.0.1:3000/api/trunkbuilds/search/index to verify 3000 port is work able.
	* npm test              -- execute unit test
	* cd /falcon/frontend
	* python -m SimpleHTTPServer 8080  -- Start Coop web service : Access http://127.0.0.1:8080 to verify the web page.

### A.3 Collection's Index
<a name="link_a3" id="link_a3"></a>

```
#### events
* db.events.ensureIndex({type:1,time:-1})

#### test_category
* db.test_category.ensureIndex({sc:1})

#### pci
* db.pci.ensureIndex({product:1,branch:1,type:1,buildend:-1})
* db.pci.ensureIndex({bl:1,product:1,branch:1,buildid:-1})
* db.pci.ensureIndex({buildid:-1})

#### events_scci
* db.events_scci.ensureIndex({path:1,revision:1})    -- will remove
* db.events_scci.ensureIndex({cut_commitrepo:1,revision:1})
* db.events_scci.ensureIndex({time:-1,author:1})
* db.events_scci.ensureIndex({type:1,promotedrev:1})
* db.events_scci.ensureIndex({type:1,tag:1})
* db.events_scci.ensureIndex({path:1,date:-1,_id:-1})
* db.events_scci.ensureIndex({cut_commitrepo:1,date:-1,_id:-1})

#### scci_usedby
* db.scci_usedby.ensureIndex({linkid:1,buildid:1})
* db.scci_usedby.ensureIndex({linkid:1})

#### scci_promotion
* db.scci_promotion.ensureIndex({promotedrev:1,cut_repo:1})
* db.scci_promotion.ensureIndex({promotedrev:1,type:1})

#### fzmfdd_trunkbuild
* db.fzmfdd_trunkbuild.ensureIndex({timestamp:1})

#### fzmtdd_trunkbuild
* db.fzmtdd_trunkbuild.ensureIndex({timestamp:1})

#### macrotdd_trunkbuild
* db.macrotdd_trunkbuild.ensureIndex({timestamp:1})
```

### Restore single collection without dropping example:
mongodump -h 127.0.0.1:27017 --db pipeline --collection pci --out ./
mongorestore --collection pci --db pipeline ./pci.bson

### Query 'type'&'promotedrev' same but 'path' is difference from events_scci
db.events_scci.aggregate([{"$match":{"promotedrev":{$exists:true}}},{"$group":{_id:{type:"$type",promotedrev:"$promotedrev",path:"$promotedrepo"}}},{$group:{_id:{"type":"$_id.type",promotedrev:"$_id.promotedrev"},count:{"$sum":1}}},{$match:{count:{$gte:2}}}]);


### A.4-1 How to get CRT trigger?
<a name="link_a41" id="link_a41"></a>
#### common CRT trigger(each trigger just have product,branch,day fields defined)
* URL: http://coop.china.nsn-net.net:3000/api/crt_trigger/search/build?product=macrotdd&branch=trunk&day=201509232359, return: TL00_ENB_9999_150923_034529
    * product=macrotdd   //the value could  be fzmtdd, fzmfdd,macrotdd
    * branch=trunk    //the value could be trunk,fl16,fl15a,fb14.07,and the default value is 'trunk'
    * day=201507032359    //2015-07-03 23:59, day=2015070309    //2015-07-03 09:00, and the defaults day is current time 
    * CRT Interface will based on QT execution time. The following build will be CRT target:
        * Score > 5
        * DAY-0 build
        * For macrto tdd products, QT Done Time is DAY-0
        * For macro tdd products, If No CRT target is fetched, CRT team search previous day’s target with url(http://coop.china.nsn-net.net:3000/api/crt_trigger/search/build?product=macrotdd&branch=trunk&day=201509232359&begin=201509221600)

#### extended CRT trigger(each trigger have product,branch,day,qt1testline fields defined)
* URL: http://coop.china.nsn-net.net:3000/api/crt_trigger/search/build?product=fzmfdd&branch=trunk&day=201605042359&qt1testline=FZM_FW2FIWA_QT1QT2, return: FLF00_ENB_9999_160504_020614
    * product=fzmfdd    //the value could  be fzmtdd, fzmfdd,macrotdd
    * branch=trunk    //the value could be trunk,fl16,fl15a,fb14.07,and the default value is 'trunk'
    * day=201507032359    //2015-07-03 23:59, day=2015070309 //2015-07-03 09:00, and the defaults day is current time
    * CRT Interface will based on QT execution time. The following build will be CRT target:
        * DAY-0 build
        * qt1testline //FZM_FW2FIWA_QT1QT2, qt1 result on FZM_FW2FIWA_QT1QT2 should be 'PASS'
        * For macrto tdd products, QT Done Time is DAY-0

<a name="link_a42" id="link_a42"></a>
### A.4-2 How to get PCI promotion trigger?
#### common PCI promotion trigger(each trigger just have bl,product,branch,time fields defined)
* URL: http://coop.china.nsn-net.net:3000/api/promotion/get?bl=lte-n&product=tdd-macro&branch=asmi_trunk&time=20160602, return: TL00_FSM4_9999_160602_008163
    * bl=lte-n          //could be lte-n, default value is lte-n
    * product=tdd-macro   //could be tdd-fzm/tdd-macro, default value is 'tdd-macro'
    * branch=trunk    //could be trunk,fl16,fl15a,fb14.07,and the default value is 'trunk'
    * time=20160602    //2016-06-02 16:00 +0800, query start time is 16:00,which was saved in collection 'pci_hierarchy'(http://coop.china.nsn-net.net/html/other/pci_hier.html)
    * uppertest=qt          //could be qt/cit, and the default value is qt
    * promotion Interface will based on QT execution time. The following build will be promotion target:
        * build start time should in [00:00, time)
        * all qt data which done time is later than 'time' will be skipped
        * Score >= upper_score (e.g. which was saved in collection 'pci_hierarchy',default value is 5)
        * if No promotion target is fetched, search build during 'time-24hours'~'time'
        
### A.5 How to get the latest builds?
<a name="link_a5" id="link_a5"></a>
- **URL**  http://coop.china.nsn-net.net:3000/api/scm/build/dashboardpci?bl=lte-n&product=fdd-fzm&branch=trunk&begin=1479225600&end=1481903999&type=product

- **Notes**

- *bl=lte-n*  // the value could  be lte-n
- *product=tdd-macro*  // the value could  be tdd-fzm/tdd-macro
- *branch=trunk*  // the value could  be trunk,fl16,fl15a,fb14.07
- *type=product*  // the value could be product,scbuild
- *begin=1479225600* // unix timestamp
- *end=1481903999* // unix timestamp
- get builds in latest month with http://coop.china.nsn-net.net:3000/api/scm/build/dashboardpci?bl=lte-n&product=fdd-fzm&branch=trunk&type=product

### A.6 How to get scci data?
<a name="link_a6" id="link_a6"></a>
- **URL**
http://coop.china.nsn-net.net:3000/api/scci/get?sc=phy_rx_tdd&branch=trunk&revision=121936

- **Notes**

- *sc=phy_rx_tdd*  // the value could  be phy_rx_tdd/mac_ps_tdd/...
- *branch=trunk*  // the value could  be trunk/tl16/...
- *revision=121936*  // the revison could be commit revision or git revison

### A.7 How to get PCI build data?
<a name="link_a7" id="link_a7"></a>
- **URL**
```
http://coop.china.nsn-net.net:3000/api/pciinfo/get?buildid=TL00_ENB_9999_160517_045380
```
- **Notes**

- *buildid=TL00_ENB_9999_160517_045380*  // release build

### A.8 SC contacts
<a name="link_a8" id="link_a8"></a>
#### SC contacts of LTE-N
```python
[
        "PHY_RX_TDD",           //Wang, Xiao W. (Nokia - CN/Hangzhou) xiao.w.wang@nokia.com
        "PHY_TX_TDD",           //Fu, Mingjie (Nokia - CN/Hangzhou) mingjie.fu@nokia.com; Zhu, Xiaowen (Nokia - CN/Hangzhou) xiaowen.zhu@nokia.com
        "BM",  
        "MAC_PS_TDD",           //Fu, Mingjie (Nokia - CN/Hangzhou) mingjie.fu@nokia.com
        "TDDCPRI",              //Liu, Anne (Nokia - CN/Hangzhou) anne.liu@nokia.com
        "PS_CCS",
        "CCS SCM",
        "TRS",
        "FZM_BM",
        "PHY_PS_TDD",
        "PS_MCUHWAPI",
        "PS_UPHWAPI",
        "FZM_OAM",
        "PHY_PROXY",
        "DSP_COMMON",               //Jost, Martin (Nokia - DE/Ulm) / I_EXT_LTE_DSP_COMMON_GMS
        "Codec",
        "FZM_LFS",
        "LOM_FDD",
        "TCOM",
        "TUP_R2",
        "TUP_R3",
        "LOM",                      //Ferenc, Jacek (Nokia - PL/Wroclaw)
        "MAC_PS",                   //Ferenc, Jacek (Nokia - PL/Wroclaw)
        "PHY_RX",                   //Ferenc, Jacek (Nokia - PL/Wroclaw)
        "C-PLANE",                  //Jaeger, Dominik (Nokia - DE/Ulm) / I_MBB_LTE_CP_CI_CORE_GMS
        "OAM",                      //I_EXT_MBB_BTS_SCM_LTE_OAM_WRO@internal.nsn.com
        "LRC-DCM-UM",
        "rakereceiver",
        "pic",
        "tupu",
        "LocalTelecom",
        "Rake",
        "Pic",
        "TupU",
        "Decoder",
        "w1plrx",
        "codec",
        "CodecRM",
        "W1plTX",
        "PIC",
        "PHY_TX",                   //I_EXT_MBB_LTE_UP_DL_PHY_SCM@internal.nsn.com
        "EncBcpHsdpa",
        "BSTAT",
        "MCTRL",
        "DCS",
        "SYSADAPT",
        "FARECO",
        "FJCPRI",
        "IM_PORT",
        "FP",
        "DecoderLibrary",
        "Measurements",
        "LTE L2",                   //Kivimaki, Tommi (Nokia - FI/Oulu)
        "LocalOam",
        "OAM_FSM3_TDD",
        "OAM_FSM4_WMP",
        "OAM_FSM4_TDD",
        "OAM_FSM3_WMP",
        "EncBcpDch",
        "OAM_COMMON_TDD",
        "OAM_COMMON_WMP",
        "W1plRx",
        "CommonDsp",
        "CodecCommon"
]
```

### A.9 How to restart MongoDB on coop/testcoop?
<a name="link_a9" id="link_a9"></a>
#### COOP
* restart mongodb
    - add startmongo and stopmongo in .bashrc
        * alias startmongo='mongod --fork --syslog --dbpath /data/db --bind_ip 127.0.0.1'
        * alias stopmongo='mongod --shutdown'
    - run 'startmongo' to start mongodb
    
#### TESTCOOP
* restart mongodb
    - service mongod restart
* stop mongodb
    - service mongod stop

### A.10 How to create merge request?
<a name="link_a10" id="link_a10"></a>  
* create merge request:
*   firstly creat branch
     - Step1 :‘Git pull’ (make suer your wokring on master, you can get your weather working on master usre by comand "git branch")
     - Step2:'git checkout –b feature/xxxxxx'
*   Add/Modify your Script
    - Step1: git add xxxxx.js
    - Step2: git commit –a –m “your message"
    - Step3: 'git fetch origin develop && git rebase develop' (or git pull origin develop   -- Merge code from origin develop. If conflict need fix it manually on local before you pust)
    - Step4: git push origin feature/xxxxxx
  - check the job status : http://coop.china.nsn-net.net/ci/job/1.%20verify_merge_into_develop/
