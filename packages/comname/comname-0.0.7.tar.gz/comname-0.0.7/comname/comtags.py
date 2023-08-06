import logging
import json
import re
import datetime
import string
import jsonfiler
import copy
import os
import numpy
import traceback
import jieba
from enum import Enum
from tqdm import tqdm
from collections import Counter



#给公司名字打经营范围标签的标签器
class comname_tagger():
    #构造函数
    def __init__(self):
        self.module_path = os.path.dirname(__file__)
        path_remap = os.path.join(self.module_path,"user_dict","com_name_industry_tags_remap.json")
        REMAP_DICT = jsonfiler.load(path_remap)
        self.tags_remap_dict = REMAP_DICT
        
        path_user_dict = os.path.join(self.module_path,"user_dict","com_name_industry_tags_user_dict.dat")
        jieba.load_userdict(path_user_dict)
        self.jieba = jieba

        path_tags = os.path.join(self.module_path,"user_dict","com_name_industry.dat")   # 最终的Tag列表
        with open(path_tags, "r", encoding="utf8") as f:
            Tags = f.readlines()
        self.Tags = [x.strip() for x in Tags]


    
    def validate(self,com_name):
        #必须全是汉字,只有中文和(),最长39个字符
        re_comp = re.compile(u'^[\(\)\u4e00-\u9fa5]{1,39}$')
        is_valid_com_name = re_comp.search(com_name)
        if not is_valid_com_name:
            return False
        return True

    def reform(self,com_name):
        #把公司名里的(),[],等去掉,虽然企业名字应该是中文,不应该有这些乱字符，但这个地方还是做筛选处理
        com_name = com_name.replace("\t","")
        com_name = com_name.replace("\r","")
        com_name = com_name.replace("\n","")
        com_name = com_name.replace(" ","")
        com_name = com_name.replace("）",")")
        com_name = com_name.replace("（","(")
        com_name = com_name.replace("【","[")
        com_name = com_name.replace("】","]")
        com_name = com_name.replace("〔","(")
        com_name = com_name.replace("〕",")")
        com_name = com_name.replace("[","(")
        com_name = com_name.replace("]",")")
        com_name = com_name.replace(" ","")
        return com_name


    def tag(self,com_name):
        tags_remap_dict = self.tags_remap_dict
        keys = tags_remap_dict.keys()
        keys = list(keys)

        temp = com_name
        cut = self.jieba.cut(temp,cut_all= True)
        cut = list(cut)

        com_name_tags = ""
        for word in cut:
            if word in keys:          # 分词后存在remap中的短语
                if  com_name_tags == "":
                    com_name_tags = tags_remap_dict[word]
                elif tags_remap_dict[word] not in com_name_tags:
                    com_name_tags = com_name_tags + "|" + tags_remap_dict[word]
        
        return com_name_tags

# 输入：企业名称
# 需要文件： com_name_industry.dat ;  最终的Tag列表
#            user_dict.dat ;          用户字典
#            remap.json               映射表
# return: 企业经营范围的Tag向量 ( 按照com_name_industry.dat列表的顺序 )
    def tagvec(self,com_name):
        vector = [0] * 128                               # 预留到512

        tags_remap_dict = self.tags_remap_dict
        keys = tags_remap_dict.keys()
        keys = list(keys)

        temp = com_name
        cut = self.jieba.cut(temp,cut_all= True)
        cut = list(cut)
        for word in cut:
            if word in keys:          # 分词后存在remap中的短语
                if tags_remap_dict[word] in self.Tags:   # 短语在映射表中对应的tag也在最终的Tag列表里
                    vector[self.Tags.index(tags_remap_dict[word])]=1
        
        new_vector = [str(v) for v in vector]
        new_vector_str = "".join(new_vector)
        return new_vector_str


def main():
    mytagger = comname_tagger()
    print(mytagger.tag("北京通信设备公司"))
    print(mytagger.tagvec("北京通信设备公司")[:111])
    print(mytagger.tag("上海红堤坊茶饮有限公司"))
    print(mytagger.tagvec("上海红堤坊茶饮有限公司")[:111])
    print(mytagger.tag("上海君为中草药种植专业合作社"))
    print(mytagger.tagvec("上海君为中草药种植专业合作社")[:111])
    print(mytagger.tag("南京荣氏商贸有限公司第八十二分公司"))
    print(mytagger.tagvec("南京荣氏商贸有限公司第八十二分公司")[:111])
    print(mytagger.tag("西宁市城中区赏延斋书画社"))
    print(mytagger.tagvec("西宁市城中区赏延斋书画社")[:111])
    





if __name__ == '__main__':
    main()
