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

os.system("cp user_dict/user_dict_com_etypes.json user_dict/user_dict_com_etypes_old.json")
os.system("cp user_dict/user_dict_com_industries.dat user_dict/user_dict_com_industries_"+time.strftime("%Y%m%d_%H_%M_%S",time.localtime())+".dat")
gbbs_rmap =  jsonfiler.load(os.path.join("user_dict","user_dict_com_etypes.json"))

path_types = os.path.join("user_dict","bad_keys.dat")
with open(path_types, "r", encoding="utf8") as f:
    BAD_KEYS = f.readlines()
BAD_KEYS = [x.strip() for x in BAD_KEYS]

path_industries = os.path.join("user_dict","a.dat")
with open(path_industries, "r", encoding="utf8") as f:
    OLD_INDUSTRIES = f.readlines()
OLD_INDUSTRIES = [x.strip() for x in OLD_INDUSTRIES]


more_industries = []
for k,v in gbbs_rmap.items():
    if v.startswith("+") or v.endswith("+"):
        gbbs_rmap[k] = ""
        continue
    new_industry = v.split("+")[0]
    if new_industry not in OLD_INDUSTRIES:
        more_industries.append(new_industry)
    if v == "" and k not in OLD_INDUSTRIES:
        more_industries.append(k)
more_industries=[x.strip() for x in more_industries]
more_industries=list(set(more_industries))
if "" in more_industries:
    more_industries.remove("")

NEW_INDUSTRIES = []
NEW_INDUSTRIES.extend(OLD_INDUSTRIES)
NEW_INDUSTRIES.extend(more_industries)
print(len(OLD_INDUSTRIES))
print(len(more_industries))
print(len(NEW_INDUSTRIES))
NEW_INDUSTRIES = list(set(NEW_INDUSTRIES))
if "" in NEW_INDUSTRIES:
    NEW_INDUSTRIES.remove("")
print(len(NEW_INDUSTRIES))


path_types = os.path.join("user_dict","user_dict_com_types.dat")
with open(path_types, "r", encoding="utf8") as f:
    OLD_TYPES = f.readlines()
OLD_TYPES = [x.strip() for x in OLD_TYPES]


more_types = []

for k,v in gbbs_rmap.items():
    new_type = v.split("+")[-1]
    if new_type in gbbs_rmap:
        v = gbbs_rmap[new_type]
        if len(v.split("+")) == 2:
            new_type = v.split("+")[-1]
            if new_type not in OLD_TYPES:
                more_types.append(new_type)
        else:
            print("错误的key:"+k)
    elif new_type not in OLD_TYPES:
        more_types.append(new_type)

new_types = list(set(OLD_TYPES + more_types))

if "" in new_types:
    new_types.remove("")

new_types = [k for k in sorted(new_types)]

gbbs_rmap_keys = [k for k in sorted(gbbs_rmap.keys())]


if "" in gbbs_rmap:
    gbbs_rmap.pop("")
for k in gbbs_rmap_keys:
    if len(k) <3:
        #print(k)
        pass
    if k in BAD_KEYS:
        gbbs_rmap.pop(k)

gbbs_rmap_keys = [k for k in sorted(gbbs_rmap.keys())]

jsonfiler.dump(gbbs_rmap,"user_dict/user_dict_com_etypes.json",indent=4)

new_file=codecs.open("user_dict/user_dict_com_etypes.dat","wb",encoding="utf-8")
for word in gbbs_rmap_keys:
    new_file.write(word+"\n")
new_file.close()

new_file=codecs.open("user_dict/user_dict_com_industries_more.dat","wb",encoding="utf-8")
for word in more_industries:
    new_file.write(word+"\n")
new_file.close()


new_file=codecs.open("user_dict/user_dict_com_industries.dat","wb",encoding="utf-8")
for word in NEW_INDUSTRIES:
    new_file.write(word+"\n")
new_file.close()

"""
确保user_dict_com_types.dat有备份再运行下面代码
new_file=codecs.open("user_dict/user_dict_com_types.dat","wb",encoding="utf-8")
for word in new_types:
    new_file.write(word+"\n")
new_file.close()
"""
