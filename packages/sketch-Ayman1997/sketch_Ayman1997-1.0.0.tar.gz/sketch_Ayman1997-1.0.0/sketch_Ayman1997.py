import os
os.getcwd()
os.chdir('C:\\Users\\Ayman\\AppData\\Local\\Programs\\Python\\Builds\\HeadFirstPython\\Chapter3')
data = open('sketch.txt')
print(data.readline(), end='') 		 
data.seek(0) 		 
for each_line in data: 
	print(each_line, end='')
data.close()
