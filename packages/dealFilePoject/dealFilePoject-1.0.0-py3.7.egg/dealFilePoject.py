# 打印数据到屏幕或者文件
# the_list-数据集合； indent-是否需要缩进； level_flag-缩进几个制表符； file_dir-写入到哪个文件
import sys
def printLol(the_list,indent=False,level_flag=0,file_dir=sys.stdout):
    #we will call myself to find next list
    for eachLol in the_list:
    	if isinstance(eachLol,list):
    		printLol(eachLol,indent,level_flag+1,file_dir)
    	else:
    		if indent:
    			for tab_stop in range(level_flag):
    				print("\t",end='',file=file_dir)
    		print(eachLol,file=file_dir)

# 处理文件数据并写入到文件中
import os
os.chdir('E:\\WORK_SPACE\\workspace_for_python\\DataInfo\\firstFile')
man = []
other = []
# 处理文件数据
try:
	data = open('sketch.txt')
	# 逐行处理
	for each_line in data:
		try:
			# 把字符串按":"拆分为两部分，若含有多个":"则可设置第二个参数限制split('',maxsplit)
			(person,spoken)=each_line.split(':',1)
			# 去掉字符串收尾空白字符
			spoken = spoken.strip()
			if person == 'Man':
				man.append(spoken)
			elif person == 'Other Man':
				other.append(spoken)
			#print(person,end='')
			#print('	said:',end='')
			#print(spoken)
		except ValueError:
			pass
	data.close()
# 为异常定义数据对象，然后通过数据对象输出异常详细信息
except IOError as fileErr:
	# 异常类型可能为字符型，强制转换为字符型再进行打印
	print('Open file error: ' + str(fileErr))
# 写入数据到文件
try:
	# 如果我们使用with处理文件，则可删除finally模块，你不用考虑关闭文件的问题
	#man_out = open('man_data.txt','w')
	#with open('man_data.txt','w') as man_out:
	#	print(man,file=man_out)
	#other_out = open('other_data.txt','w')
	#with open('other_data.txt','w') as other_out:
	#	print(other,file=other_out)
	# With模块也可以多个放到同一行，用","分割，最后一个添加":"
	with open('man_data.txt','w') as man_out, open('other_data.txt','w') as other_out:
		# 直接把集合写入到文件中
		#print(man,file=man_out)
		# 集合格式化后写入到文件中
		printLol(man,True,1,man_out)
		#print(other,file=other_out)
		printLol(other,True,1,other_out)
except IOError as err:
	print('Write file error: ' + str(err))
#finally:
	# 关闭数据对象前先判断数据对象是否在本地创建
	#if 'man_out' in locals():
	#	man_out.close()
	#if 'other_out' in locals():
	#	other_out.close()
