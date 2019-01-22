import sys;
import hashlib;
import os;
import zipfile;
import time;
import shutil;
import subprocess;
import json;


gYear = str(time.localtime().tm_year)
gMonth = ( "0" + str(time.localtime().tm_mon) if time.localtime().tm_mon < 10 else str(time.localtime().tm_mon))
gDay = ("0" + str(time.localtime().tm_mday)  if time.localtime().tm_mday  < 10 else str(time.localtime().tm_mday))
gHour = ("0" + str(time.localtime().tm_hour)  if time.localtime().tm_hour < 10 else str(time.localtime().tm_hour))
gMin = ("0" + str(time.localtime().tm_min) if time.localtime().tm_min < 10 else str(time.localtime().tm_min))

vesionStr = gYear+ "_"+ gMonth + "_"+gDay + "_" + gHour+ "_"+ gMin
gTempDir = "updateDir/test/"
gManifestFileName = gTempDir + "project.manifest"
gVersionFileName = gTempDir + "version.manifest"
#--------------------------check out-------------------------------
def checkOutByVesion(vesion):	
	srcDir = gTempDir + vesion + "/src"
	resDir = gTempDir + vesion + "/res"
	commondSrc = "svn checkout " + gSvnUrl + "src/ " + srcDir + " -r " + vesion
	os.system(commondSrc)
	commondRes = "svn checkout " + gSvnUrl + "res/ " + resDir + " -r " + vesion
	os.system(commondRes)

#---------------------build jsc------------------------------
cocosPath = os.environ["COCOS_CONSOLE_ROOT"]

def buildJsc(path):
	path = 'src'
	tempSrcDir = gTempDir + "src"
	cmdStr = 'python ' + cocosPath + '\\cocos.py jscompile -s ' + path + ' -d ' + tempSrcDir
	os.system(cmdStr)	

def removeFileRead(path):	
	cmd = "attrib -R -H -S " + gTempDir + "/*" + " /s /d"	
	os.system(cmd)
	
#--------------------- end ------------------------------
def checkFileList(fileList,list,expend):
	for i in fileList:
		fileName = i + expend
		print "addFile : " + fileName
		list.append(fileName)	

def getMd5(filePath):
	#print("filepath :" + filePath)
	leMd5 = "null"
	#filePath = filePath.encode('gb18030')
	if os.path.exists(filePath):
		filePtr = open(filePath,'rb')
		leMd5 = hashlib.md5(filePtr.read()).hexdigest()
		filePtr.close();

	return leMd5

def zip_dir(filelist,fileName):
	zip = zipfile.ZipFile(gTempDir + fileName, 'a',zipfile.ZIP_DEFLATED)
	_curpath = os.getcwd()
	os.chdir(gTempDir)
	for x in filelist:		
		path = x				
		savePath = path.replace(path + os.path.sep, '')
		savePath = path.replace("/", "\\")
		print "savePath:" + savePath
		# path = gTempDir + gNewVersion + "/" + path
		dirPath = savePath[0 : savePath.rindex("\\")];		
		print "dirPath:" + dirPath
		zip.write(dirPath)
		zip.write(savePath)		
	zip.close()	
	os.chdir(_curpath)
	# zip.printdir()

def get_recursive_file_list(path):
	current_files = os.listdir(path)
	all_files = []
	for file_name in current_files:
		full_file_name = os.path.join(path, file_name)

		if os.path.isdir(full_file_name):
			next_level_files = get_recursive_file_list(full_file_name)
			all_files.extend(next_level_files)
		else:
			#fisrt = full_file_name.find("\\")
			#fileName = full_file_name[fisrt + 1:]
			index = full_file_name.find("/")
			index = full_file_name.find("/",index + 1)
			savePath = full_file_name[index + 1:len(full_file_name)]
			all_files.append(savePath)
			# print "fileName:" + savePath
	return all_files

#---------------------check-------------------------------

#---------------------buildJson-------------------------------

def loadJson(fileName):
	f = open(fileName)
	j = json.load(f)
	f.close()
	return j

def saveJson(fileName,j):
	f = open(fileName,"w")
	json.dump(j, f,indent=1) 
	f.close()

def addVersion(j):
	version = j["version"]
	index = version.rfind(".")
	num = int(version[index + 1:len(version)])
	num = num + 1
	newVersion = version[0 : index + 1] + str(num)
	j["version"] = newVersion

def buildMainfest(fileNameList):
	j = loadJson(gManifestFileName)		
	addVersion(j)
	# -------------for test-------------
	# j["assets"] = {}
	# -------------for test-------------
	for fileName in fileNameList : 
		md5 = getMd5(gTempDir + fileName)		
		newPackage = {
	        "path" : fileName,
	        "md5" : md5,
	        "compressed" : True,            
	    }
		j["assets"][fileName] = newPackage

	saveJson(gManifestFileName,j)	

def buildVersion():
	j = loadJson(gVersionFileName)	
	addVersion(j)
	saveJson(gVersionFileName,j)


#---------------------check-------------------------------
codeList = ["src/Common/Const.js"]
resList = []

ZipFileName = vesionStr + "_update.zip"
try:
	srcFileList = []
	resFileList = []
	checkFileList(codeList,srcFileList,"c")
	checkFileList(resList,resFileList,"")	
	buildJsc("")
	zip_dir(srcFileList,ZipFileName)
	zip_dir(resFileList,ZipFileName)
except Exception, e:
	print e
	print "check error!!!!!"
	os._exit(0);
	raise
print "check finish"
#---------------------buildJson start-------------------------------
print "buildJson start"
fileNameList = [ZipFileName]
buildMainfest(fileNameList)
buildVersion()
print "buildJson finish"
#---------------------end-------------------------------