#!/usr/bin/python
 
import sys
import socket
import re
import subprocess
from StringIO import StringIO
import os
 
 
zabbix_sender = '/data/zabbix/bin/zabbix_sender'
zabbix_conf = '/data/zabbix/etc/zabbix_agentd.conf'
send_to_zabbix = 1
zabbix_server = '10.19.192.38'
hostname = socket.getfqdn(socket.gethostname())
 
############# get zookeeper server status
class ZooKeeperServer(object):
 
    def __init__(self, host='localhost', port='2181', timeout=1):
        self._address = (host, int(port))
        self._timeout = timeout
        self._result  = {}
 
    def _create_socket(self):
        return socket.socket()
 
 
    def _send_cmd(self, cmd):
        """ Send a 4letter word command to the server """
        s = self._create_socket()
        s.settimeout(self._timeout)
 
        s.connect(self._address)
        s.send(cmd)
 
        data = s.recv(2048)
        s.close()
 
        return data
 
    def get_stats(self):
        """ Get ZooKeeper server stats as a map """
        data_mntr = self._send_cmd('mntr')
        data_ruok = self._send_cmd('ruok')
        if data_mntr:
            result_mntr = self._parse(data_mntr)
        if data_ruok:
            result_ruok = self._parse_ruok(data_ruok)
 
        self._result = dict(result_mntr.items() + result_ruok.items())
         
        if not self._result.has_key('zk_followers') and not self._result.has_key('zk_synced_followers') and not self._result.has_key('zk_pending_syncs'):
 
           ##### the tree metrics only exposed on leader role zookeeper server, we just set the followers' to 0
           leader_only = {'zk_followers':0,'zk_synced_followers':0,'zk_pending_syncs':0}    
           self._result = dict(result_mntr.items() + result_ruok.items() + leader_only.items() )
 
        return self._result  
 
 
 
    def _parse(self, data):
        """ Parse the output from the 'mntr' 4letter word command """
        h = StringIO(data)
         
        result = {}
        for line in h.readlines():
            try:
                key, value = self._parse_line(line)
                result[key] = value
            except ValueError:
                pass # ignore broken lines
 
        return result
 
    def _parse_ruok(self, data):
        """ Parse the output from the 'ruok' 4letter word command """
        
        h = StringIO(data)
        
        result = {}
        
        ruok = h.readline()
        if ruok:
           result['zk_server_ruok'] = ruok
  
        return result
  
 
 
    def _parse_line(self, line):
        try:
            key, value = map(str.strip, line.split('\t'))
        except ValueError:
            raise ValueError('Found invalid line: %s' % line)
 
        if not key:
            raise ValueError('The key is mandatory and should not be empty')
 
        try:
            value = int(value)
        except (TypeError, ValueError):
            pass
 
        return key, value
 
 
 
    def get_pid(self):
         pidarg = '''ps -ef|grep java|grep zookeeper|grep -v grep|awk '{print $2}' ''' 
         pidout = subprocess.Popen(pidarg,shell=True,stdout=subprocess.PIPE)
         pid = pidout.stdout.readline().strip('\n')
         return pid
 
 
    def send_to_zabbix(self, metric):
         key = "zookeeper.status[" +  metric + "]"
 
         if send_to_zabbix > 0:
            # print key + ":" + str(self._result[metric])
             try:
 
                subprocess.call([zabbix_sender, "-z", zabbix_server, "-s",hostname, "-k", key, "-o", str(self._result[metric]) ], stdout=FNULL, stderr=FNULL, shell=False)
             except OSError, detail:
                print "Something went wrong while exectuting zabbix_sender : ", detail
         else:
                print "Simulation: the following command would be execucted :\n", zabbix_sender, "-c", zabbix_conf, "-k", key, "-o", self._result[metric], "\n"
 
 
 
 
def usage():
        """Display program usage"""
 
        print "\nUsage : ", sys.argv[0], " alive|all"
        print "Modes : \n\talive : Return pid of running zookeeper\n\tall : Send zookeeper stats as well"
        sys.exit(1)
 
 
 
accepted_modes = ['alive', 'all']
 
if len(sys.argv) == 2 and sys.argv[1] in accepted_modes:
        mode = sys.argv[1]
else:
        usage()
 
 
 
 
zk = ZooKeeperServer()
pid = zk.get_pid()
 
if pid != "" and  mode == 'all':
   zk.get_stats()
   # print zk._result
   FNULL = open(os.devnull, 'w')
   for key in zk._result:
       zk.send_to_zabbix(key)
   FNULL.close()
   print pid
 
elif pid != "" and mode == "alive":
    print pid
else:
    print 0
