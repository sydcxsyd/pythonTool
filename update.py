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
gTempDir = "updateDir/"

gOldVersion = "106"
gNewVersion = "108"

# outOldVersion = "51"


gSvnUrl = "https://172.16.40.20/svn/MJJ-Client-jxmj/trunk/jxmj/"
gAndroidManifestFileName = "updateDir/android/project.manifest"
gIosManifestFileName = "updateDir/ios/project.manifest"
gTestManifestFileName = "updateDir/test/project.manifest"
gTestOutManifestFileName = "updateDir/testout/project.manifest"

gAndroidVersionFileName = "updateDir/android/version.manifest"
gIosVersionFileName = "updateDir/ios/version.manifest"
gTestVersionFileName = "updateDir/test/version.manifest"
gTestOutVersionFileName = "updateDir/testout/version.manifest"
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
	print "path " + path
	path = path + '/src'
	tempSrcDir = gTempDir + '/src'
	cmdStr = 'python ' + cocosPath + '\\cocos.py jscompile -s ' + path + ' -d ' + tempSrcDir
	os.system(cmdStr)
	shutil.rmtree(path)	
	shutil.move(tempSrcDir,path)

def removeFileRead(path):
	shutil.rmtree(path + "/src/.svn/")
	shutil.rmtree(path + "/res/.svn/")

#--------------------- end ------------------------------
newDir = gTempDir + gNewVersion + "/" 
oldDir = gTempDir + gOldVersion + "/"
def checkFileList(fileList,list,expend):
	for i in fileList:
		isOld = checkMd5(i)
		if isOld == False:
			if(i.find(".manifest") == -1):			 			
	  			fileName = i + expend
	  			print "addFile : " + fileName
				list.append(fileName)

def checkMd5(path):
	newFilePath = newDir + path
	oldFilePath = oldDir + path

	newFileMd5 = getMd5(newFilePath);
	oldFileMd5 = getMd5(oldFilePath);
	# print "newFilePath:" + newFilePath
	# print "oldFilePath:" + oldFilePath
	# print "newFileMd5:" + newFileMd5
	# print "oldFileMd5:" + oldFileMd5
	if newFileMd5 and newFileMd5 == oldFileMd5:
		return True
	else:
		return False

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
	os.chdir(gTempDir + gNewVersion)
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
	tVer = ""
	while 1:
		index = version.rfind(".")	
		num = int(version[index + 1:len(version)])
		version = version[0 : index + 1]
		num = num + 1
		if num >= 10:
			tVer = tVer + ".0"
			version = version[0 : index]
		else :
			tVer = str(num) + tVer
			break
	
	newVersion = version + tVer
	j["version"] = newVersion

def buildMainfest(fileNameList,manifestPath):
	j = loadJson(manifestPath)		
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

	saveJson(manifestPath,j)	

def buildVersion(versionPath):
	j = loadJson(versionPath)	
	addVersion(j)
	saveJson(versionPath,j)

#---------------------start check out-------------------------------
print "start check out"
if int(gOldVersion) > int(gNewVersion):
	print "oldversion must smaller than new!!!!"
	os._exit(0);
checkOutByVesion(gOldVersion)
checkOutByVesion(gNewVersion)

print "end check out"
#---------------------check-------------------------------
print "start check"
cmd = "attrib -R -H -S -A " + gTempDir + "/*" + " /s /d"	
os.system(cmd)

removeFileRead(gTempDir + gOldVersion)
removeFileRead(gTempDir + gNewVersion)


# shutil.rmtree(gTempDir + gOldVersion + "/src/.svn/")
# shutil.rmtree(gTempDir + gOldVersion + "/res/.svn/")

# shutil.rmtree(gTempDir + gNewVersion + "/src/.svn/")
# shutil.rmtree(gTempDir + gNewVersion + "/res/.svn/")

# ZipSrcFileName = vesionStr + "_src.zip"
# ZipResFileName = vesionStr + "_res.zip"
ZipFileName = vesionStr + "_update.zip"

codeList = get_recursive_file_list(gTempDir + gNewVersion + "/src/")
resList = get_recursive_file_list(gTempDir + gNewVersion + "/res/")
try:
	srcFileList = []
	resFileList = []
	checkFileList(codeList,srcFileList,"c")
	checkFileList(resList,resFileList,"")	

	buildJsc(gTempDir + gOldVersion)
	buildJsc(gTempDir + gNewVersion)

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

buildMainfest(fileNameList,gAndroidManifestFileName)
buildVersion(gAndroidVersionFileName)

buildMainfest(fileNameList,gIosManifestFileName)
buildVersion(gIosVersionFileName)

buildMainfest(fileNameList,gTestManifestFileName)
buildVersion(gTestVersionFileName)

# buildMainfest(fileNameList,gTestOutManifestFileName)
# buildVersion(gTestOutVersionFileName)
print "buildJson finish"
#---------------------clean-------------------------------
print "clean start"
shutil.rmtree(gTempDir + gNewVersion);
shutil.rmtree(gTempDir + gOldVersion);
print "clean finish"
#---------------------end-------------------------------
