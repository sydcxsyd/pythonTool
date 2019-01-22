# -*- coding:utf-8 -*- 
import xlrd
import types
from datetime import date,datetime
import json

filePath = ""
outDir = "..\\src\\Data\\"
def read_table(table,lineNum,idLine,outFileName):
	nrows = table.nrows
	data = {}
	templateList = []
	id = 0
	for i in range(2 ,nrows):		
		colData = table.row_values(i)
		temp_rowData = {}
		for j in range(lineNum):
			value = colData[j]
			if i == 2 : #第二行配置的是字段名字
				templateList.append(str(value))
			else:							
				if isinstance(value,float) or isinstance(value,float):
					value = int(value)
					print value
				elif not isinstance(value, unicode):
					value = int(value)
					print value
				else :
					value = value.encode("utf-8")
					print value
				if j == idLine:
					id = value				
				temp_rowData[templateList[j]] = value
		if not i == 2:
			data[id] = temp_rowData
		
	outPath = outDir + outFileName + ".js"

	data_string = json.dumps(data,indent=1)
	data_string = "var " + outFileName + " = " + data_string
	print data_string
	f = open(outPath, 'w')
	f.write(data_string)
	f.close()


def read_excel(excelName,pageIndex,lineNum,idLine,outFileName):
	# 打开文件
	data = xlrd.open_workbook(filePath + excelName)
	table = data.sheets()[pageIndex]
	read_table(table,lineNum,idLine,outFileName)
	

read_excel("item.xlsx",0,4,0,"ItemData")
read_excel("arenaCfg.xlsx",0,25,0,"ArenaConfigData")
read_excel("arenaRule.xlsx",0,9,0,"ArenaRuleData")
read_excel("arenaReward.xlsx",0,4,0,"ArenaRewardData")
