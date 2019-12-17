# coding=utf-8
# -*- coding: utf-8 -*-
import os
import re

# file = open("C:\\Users\\liuwei\\Desktop\\location1.txt","r",encoding='UTF-8')
# lines = file.readlines()
# file.close()
# aaa = {}
# for line in lines:
#     line = re.sub(u'(\"+)', u',', line)[1:-2]
#     ls = line.split(",")
#     if(aaa.get(ls[1].strip() if len(ls) > 3 else ls[0].strip() ) != None):
#         aaa[ls[1].strip() if len(ls) > 3 else ls[0].strip()] += 1
#     else:
#         aaa[ls[1].strip() if len(ls) > 3 else ls[0].strip()] = 1 
# test_data_3=sorted(aaa.items(),key=lambda x:x[1],reverse=True)

# with open("C:\\Users\\liuwei\\Desktop\\location.txt",'w',encoding='utf-8') as file_obj:
#     i = 1
#     file_obj.write("排名\t国家名\t\t\t\t\t\t\t出现次数\n")
#     for wline in test_data_3:
#         file_obj.write(str(i) + "\t" + str(wline[0]) + "\t\t\t\t\t\t\t" + str(wline[1]) + "\n")
#         i +=1
