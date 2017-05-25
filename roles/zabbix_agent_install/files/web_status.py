#!/usr/bin/env python
#coding:utf-8
import json
import os, sys, commands
def getportinfo():
    url = []
    p = os.popen("""netstat -tlpn |grep java|grep 0.0.0.0|awk '{print $4}'|awk -F: '{print $2}'| awk '/^80/'""") #类型是list
    uu = 'healthCheck'
    for port in p.readlines():   #字符
        t = os.path.basename(port.strip())   #字符
        if t == '8081':
            ppp = os.popen("""find /data/tomcat1/webapps/*.war | awk -F '/' '{print $5}' |awk -F '.' '{print $1}'""")
            pa = ppp.readlines()
            aa = t+'/'+os.path.basename(pa[0].strip())+'/'+uu  #list转 字符
            url += [{'{#WEBURL}':aa}]
        elif t == '8082':
            ppp = os.popen("""find /data/tomcat2/webapps/*.war | awk -F '/' '{print $5}' |awk -F '.' '{print $1}'""")
            pa = ppp.readlines()
            aa = t+'/'+os.path.basename(pa[0].strip())+'/'+uu  #list转 字符
            url += [{'{#WEBURL}':aa}]
            # print json.dumps({'data':url},sort_keys=True,indent=4,separators=(',',':'))
        elif t == '8083':
            ppp = os.popen("""find /data/tomcat3/webapps/*.war | awk -F '/' '{print $5}' |awk -F '.' '{print $1}'""")
            pa = ppp.readlines()
            aa = t+'/'+os.path.basename(pa[0].strip())+'/'+uu  #list转 字符
            url += [{'{#WEBURL}':aa}]
        elif t == '8084':
            ppp = os.popen("""find /data/tomcat4/webapps/*.war | awk -F '/' '{print $5}' |awk -F '.' '{print $1}'""")
            pa = ppp.readlines()
            aa = t+'/'+os.path.basename(pa[0].strip())+'/'+uu
            url += [{'{#WEBURL}':aa}]
            #return json.dumps({'data':url},sort_keys=True,indent=4,separators=(',',':'))
        else:
            print "ERROR: portinfo error"
    return json.dumps({'data':url},sort_keys=True,indent=4,separators=(',',':'))
def getwebstatus(ports):
    cmds = "curl -I -s 127.0.0.1:"+ports+" |head -1| awk '{print $2}'"
    print commands.getoutput(cmds)
if __name__ == '__main__':
    if sys.argv[1] == 'discovery':
        print getportinfo()
    elif sys.argv[1] == 'status':
        getwebstatus(sys.argv[2])
    else:
        print "ERROR: argument error"
