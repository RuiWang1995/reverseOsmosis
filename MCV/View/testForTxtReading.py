# @Author: Rui
# @Date: 12/27/20 3:17 PM
# @Description: 
# @File: testForTxtReading.py

feedSpacer = open("../Model/feedSpacer.txt")
membrane = open("../Model/membrane.txt")
content = feedSpacer.read()
strList = []
newStrList = []
str1 = ''
count = 0
for i in content:
    if i == '\n':
        strList.append(newStrList)
        newStrList = []
        str1 = ''
    else:
        if i == ' ':
            newStrList.append(str1)
            str1 = ''
        else:
            str1 = str1 + i
feedSpacer.close()
