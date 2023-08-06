# coding:utf-8
#功能：最后用于判断得的范围
#https://www.sohu.com/a/163372936_622516
#工商登记对于经营范围要怎么写并没有明确的规定，不要求字数也没有类别限制。但是通常来说，经营范围的填写最好规范、易懂。如果真的不知道怎么写呢。就到国家统计局上去，找到“国民经济行业分类”，在这里可以看到比较规范的描述。

import logging
import json
import re
import datetime
import json
import re
import string
import ml3
import copy
import os
import numpy
import traceback
import jsonfiler
import codecs
import time
from collections import Counter

os.system("cp user_dict/user_dict_com_types.dat user_dict/user_dict_com_types_old.dat")

with open("user_dict/user_dict_com_industries.dat", "r", encoding="utf8") as f:
    OLD_INDUSTRIES = f.readlines()
OLD_INDUSTRIES = [x.strip() for x in OLD_INDUSTRIES]

OLD_INDUSTRIES = list(set(OLD_INDUSTRIES))

#myList = ['青海省','内蒙古自治区','西藏自治区','新疆维吾尔自治区','广西壮族自治区']  
#OLD_INDUSTRIES.sort(key = lambda i:len(i),reverse=True)  
OLD_INDUSTRIES.sort(key = lambda i:len(i),reverse=False)  


new_file=codecs.open("user_dict/user_dict_com_industries.dat","wb",encoding="utf-8")
for word in OLD_INDUSTRIES:
    new_file.write(word+"\n")
new_file.close()
