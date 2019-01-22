#coding:utf-8

import os
import os.path

rootdir = 'res\\' 									# 指明被遍历的文件夹
fileList = []

def getFileList():
	for parent,dirnames,filenames in os.walk(rootdir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
		for filename in filenames:                      #输出文件信息
			print "filename is:" + filename
			fileFullPath = os.path.join(parent,filename);
			print "the full name of the file is:" + fileFullPath #输出文件路径信息 #windows下为：d:\data\query_text\EL_00154
			fileList.append(fileFullPath)

resource = 'src\\resource.js'


def writeFile(allStr):

	file_object = open(resource,'w')
	try:
	     all_the_text = file_object.write(allStr)
	finally:
	     file_object.close( )

def makeFileStr(pathList):
	pathStr = 'g_resources = ' +  str(pathList);	

	allStr = pathStr;

	allStr = allStr.replace("\\\\","/");
	writeFile(allStr);

getFileList();
makeFileStr(fileList);
