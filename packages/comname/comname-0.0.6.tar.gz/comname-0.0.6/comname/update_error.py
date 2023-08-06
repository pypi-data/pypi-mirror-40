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

etypes_json  = jsonfiler.load("error.json")

error_keys = list(etypes_json.keys())

jsonfiler.dump(error_keys,"error_names.json",indent=4)

