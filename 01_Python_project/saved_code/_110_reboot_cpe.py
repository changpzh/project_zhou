#!/usr/bin/env python
# -*- coding: utf-8 -*-

def reboot(self):
        """ue reboot
        """
        if not self._connected:
            self._connect()
        self._conn.send_data("ATREBOOT" + os.linesep) #reboot command
        reboot_succeed = False
        start_time = time.time()
        while time.time() - start_time < 10 :
            if os.system('ping %s -n 1' % self._host) == 0: #是否还可以ping通
                continue
            else:
                log.info("ue '%s' is shutdown" % self._host)
                curtime_tmp = time.time()
                while time.time() - curtime_tmp < self._reboot_max_duration: #是否在给定时间内起来。
                    if os.system("ping %s -n 1" % self._host) == 0:
                        reboot_succeed = True
                        break
                break
        if reboot_succeed is True:
            self._connected = False
            log.info("ue '%s'reboot succeed!" % self._host)
            time.sleep(10)
            return True
        raise Exception("ue '%s'reboot failed!" % self._host)
