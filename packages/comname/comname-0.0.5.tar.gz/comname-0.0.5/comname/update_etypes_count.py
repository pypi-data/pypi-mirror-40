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
import comname
from tqdm import tqdm
test_names = jsonfiler.load("json/com_names_combasic_107w.json")
#test_names = jsonfiler.load("json/com_names_5w.json")
mycutter = comname.cutter()
error_count = 0
all_count = len(test_names)
name_cuts_error = {}

etypes_json  = jsonfiler.load("user_dict/user_dict_com_etypes.json")
etypes_keys  = etypes_json.keys()
etypes_count = {}
for k in etypes_keys:
    etypes_count[k] =0
for test_name in tqdm(test_names):
    name_cuts = mycutter.cut(test_name)
    if not name_cuts:
        error_count +=1
        name_cuts_error[test_name] = name_cuts
        continue 
    
    if not name_cuts["ok"]:
        error_count +=1
        name_cuts_error[test_name] = name_cuts
        continue

    name_segs = name_cuts["com_segs"]
    name_segs2 = []
    for name_seg in name_segs:
        if len(name_seg) <=3:
            name_segs2.append(name_seg)
            continue
        if name_seg not in etypes_keys:
            name_segs2.append(name_seg)
        elif len(etypes_json[name_seg])>=2:
            name_segs2.extend(etypes_json[name_seg])
        else:
            name_segs2.append(name_seg)
    name_segs = name_segs2
    for seg in name_segs:
        if seg in etypes_keys:
            etypes_count[seg]+=1

print("错误数:"+str(error_count)+"/"+str(all_count))    
jsonfiler.dump(name_cuts_error, "error.json", indent=4)
 
jsonfiler.dump(etypes_count,"user_dict_com_etypes_count.json",indent=4)
