import logging
import json
import re
import datetime
import json
import re
import string
import jsonfiler
import copy
import os
import numpy
import traceback
import jieba
from enum import Enum

class Lookingfor(Enum):
    LOC = 1
    FEATURE = 2
    TYPE = 3
    TAIL = 4
    SUB = 5
    SUBTAIL = 6
    ENDLESS = 7

class cutter():
    #构造函数
    def __init__(self):
        #关键词列表要单独提取出来做分析
        self.module_path = os.path.dirname(__file__)
        # com_loc的库
        path_citys = os.path.join(self.module_path,"user_dict","user_dict_com_citys.dat")
        with open(path_citys, "r", encoding="utf-8") as f:
            LOCS = f.readlines()
        self.LOCS = [x.strip() for x in LOCS]
        
        # com_type的库
        path_types = os.path.join(self.module_path,"user_dict","user_dict_com_types.dat")
        with open(path_types, "r", encoding="utf8") as f:
            TYPES = f.readlines()
        self.TYPES = [x.strip() for x in TYPES]
        self.TYPES_SET = set(self.TYPES)
        # com_tail的库
        path_tails = os.path.join(self.module_path,"user_dict","user_dict_com_tails.dat")
        with open(path_tails, "r", encoding = "utf-8") as f:
            TAILS = f.readlines()
        self.TAILS = [x.strip() for x in TAILS]
       
        # TYEPS要extendTAILS
        self.TYPES.extend(self.TAILS)

        # com_subs的库跟city的库是同一个
        self.SUBS = LOCS
        
        # com_sub_tail的库跟tail的库是同一个
        path_types = os.path.join(self.module_path,"user_dict","user_dict_com_sub_tails.dat")
        with open(path_types, "r", encoding="utf8") as f:
            SUBTAILS = f.readlines()
        self.SUBTAILS = [x.strip() for x in SUBTAILS]
        
        #对公司名进行分词
        jieba.load_userdict(os.path.join(self.module_path,"user_dict","user_dict_com_types.dat"))
        jieba.load_userdict(os.path.join(self.module_path,"user_dict","user_dict_com_types_extra01.dat"))
        jieba.load_userdict(os.path.join(self.module_path,"user_dict","user_dict_com_types_extra02.dat"))
        jieba.load_userdict(os.path.join(self.module_path,"user_dict","user_dict_com_types_extra03.dat"))
        jieba.load_userdict(os.path.join(self.module_path,"user_dict","user_dict_com_types_extra04.dat"))
        jieba.load_userdict(os.path.join(self.module_path,"user_dict","user_dict_com_tails.dat"))
        jieba.load_userdict(os.path.join(self.module_path,"user_dict","user_dict_com_citys.dat"))
        self.jieba = jieba        
        #对公司名片段进行映射的映射表
        name_rmap = {}
        name_rmap0 = jsonfiler.load(os.path.join(self.module_path,"user_dict","user_dict_com_types.json"))   
        name_rmap1 = jsonfiler.load(os.path.join(self.module_path,"user_dict","user_dict_com_types_extra01.json"))   
        name_rmap2 = jsonfiler.load(os.path.join(self.module_path,"user_dict","user_dict_com_types_extra02.json"))   
        name_rmap3 = jsonfiler.load(os.path.join(self.module_path,"user_dict","user_dict_com_types_extra03.json"))
        name_rmap4 = jsonfiler.load(os.path.join(self.module_path,"user_dict","user_dict_com_types_extra04.json"))
        name_rmap1.update(name_rmap0)
        name_rmap1.update(name_rmap2)
        name_rmap1.update(name_rmap3)
        name_rmap1.update(name_rmap4)
        name_rmap = name_rmap1
        for k,v in name_rmap.items():
            name_rmap[k] = v.split("+")
        self.name_rmap = name_rmap
    
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

    def cut(self,com_name,method="FSM"):
        #以下是要获取的企业Logo信息所需要的元素,企业Logo名应该由,
        #1. 企业所在的省, com_province
        #2. 企业所在的市, com_city
        #2. 企业所在的县, com_city
        #3. 企业特色命名, com_feature
        #4. 企业公司模板, com_type
        #5. 企业名字后缀, com_tail
        #5. 企业名字后缀, com_sub
        #5. 企业名字后缀, com_sub_tail
        #   根据一定原则生成最好的logo名字，如果四个字更好
        #   企业的全名一定是:
        #   企业省 + 企业市 + 企业特色 + 企业模板 + 企名后缀 
        com_name = self.reform(com_name)
        if not self.validate(com_name):
            return None

        rep = re.compile("\((.*)\)")
        braced_strs = re.findall(rep, com_name)
        m_strs = list(map(lambda x:"(" + str(x) + ")", braced_strs))
        for i in m_strs:
            com_name = com_name.replace(i, "")
        #我们大致估计括号里的都是地名 所以把括号里的拿出来 放到开头

        com_province        = ""
        com_city            = ""
        com_loc             = ""
        com_feature         = ""
        com_type            = ""
        com_type_s1         = ""
        com_type_s2         = ""
        com_type_s3         = ""
        com_tail            = ""
        com_sub            = ""
        com_subtail       = ""
        com_tail_s1         = ""
        com_tail_s2         = ""
        com_tail_s3         = ""
        com_logo            = ""
        
        #把公司的()里面的内容提取出来,当做地名放到name_segs的最前面
        cut_segs = jieba.cut(com_name)
        name_segs = list(cut_segs)
        braced_strs.extend(name_segs)
        name_segs = braced_strs
       
        #如果企业名字里有"",要替换掉
        if "" in name_segs:
            name_segs.remove("")
        if method == "FSM":
            com_name_cuts = self.docut1(name_segs) 
        else:
            com_name_cuts = self.docut2(name_segs) 
        if com_name_cuts is None:
            com_name_cuts = {"ok":False}
        com_name_cuts["name"] = com_name
        return com_name_cuts

    def docut1(self,name_segs):
        
        #切分之后看types是否存在,如果不存在直接返回
        if set(name_segs) & self.TYPES_SET == ():
            return None
        
        com_province        = ""
        com_city            = ""
        com_loc             = ""
        com_feature         = ""
        com_type            = ""
        com_type_s1         = ""
        com_type_s2         = ""
        com_type_s3         = ""
        com_tail            = ""
        com_sub            = ""
        com_subtail       = ""
        com_tail_s1         = ""
        com_tail_s2         = ""
        com_tail_s3         = ""

        #状态机逆序搜索，确认企业名字的最后一个短语
        #江西添福养老服务有限公司大码头社区居家养老服务中心
        name_end = ""
        for seg in reversed(name_segs):
            if seg in self.TAILS or seg in self.SUBTAILS or seg in self.TYPES:
                name_end = seg+name_end
            else:
                break

        #状态机正序搜索
        ok_flag = True
        cur_state = Lookingfor.LOC
        for seg in name_segs:
            if cur_state is Lookingfor.LOC:
                if seg in self.LOCS:
                    com_loc +=seg
                elif seg in ["中国","省","市","区","县","村","乡","镇","堡"]:
                    com_loc +=seg
                elif seg in self.TYPES:
                    com_type = seg
                    cur_state = Lookingfor.TYPE
                else:
                    com_feature +=seg
                    cur_state = Lookingfor.FEATURE
                continue

            elif cur_state is  Lookingfor.FEATURE:
                if seg in self.TYPES:
                    com_type = seg
                    cur_state = Lookingfor.TYPE
                else:
                    com_feature +=seg
                continue
            #能进这个状态,说明实现已经找到type了
            elif cur_state is  Lookingfor.TYPE:
                if seg in self.SUBS:
                    com_sub += seg
                    cur_state = Lookingfor.SUB
                elif seg in self.SUBTAILS:
                    com_subtail = seg
                    com_state = Lookingfor.SUBTAIL
                elif seg in self.TYPES:
                    com_type += seg
                    com_state = Lookingfor.TYPE
                elif seg in self.TAILS:
                    com_tail += seg
                    com_state = Lookingfor.TAIL
                else:
                    com_sub += seg
                    cur_state = Lookingfor.SUB
                continue 

            #能进这个状态,说明实现已经找到tail了
            elif cur_state is  Lookingfor.TAIL:
                if seg in self.SUBS:
                    com_sub += seg
                    cur_state = Lookingfor.SUB
                elif seg in self.SUBTAILS:
                    com_subtail = seg
                    com_state = Lookingfor.SUBTAIL
                elif seg in self.TAILS:
                    com_tail += seg
                    com_state = Lookingfor.TAIL
                else:
                    com_sub += seg
                    cur_state = Lookingfor.SUB
                continue 


            #江西添福养老服务有限公司,大,码头,社区居家养老,服务中心 
            #在sub状态,如果还没有发现name_end词,那么就一直sub
            elif cur_state is  Lookingfor.SUB:
                if seg != name_end:
                    com_sub += seg
                else:
                    #如果在subtails能找到多个tail:如 广场,店 = 广场店
                    com_subtail = name_end
                    cur_state = Lookingfor.SUBTAIL
                continue 
            
            elif cur_state is  Lookingfor.SUBTAIL:
                if seg in self.SUBTAILS:
                    com_subtail += seg
                else:
                    cur_state = Lookingfor.ENDLESS
                continue

            elif cur_state is  Lookingfor.ENDLESS:
                ok_flag = False
                break
        name_segs_full = []
        for name_seg in name_segs:
            if name_seg not in self.name_rmap:
                name_segs_full.append(name_seg)
            else:
                name_segs_full.extend(self.name_rmap[name_seg])

        com_name_items = {
            "ok":ok_flag,
            "com_segs":name_segs,
            "com_segs_full":name_segs_full,
            "com_loc:":com_loc,
            "com_feature":com_feature,  
            "com_type":com_type, 
            "com_tail":com_tail, 
            "com_sub":com_sub, 
            "com_subtail":com_subtail
        }
        return com_name_items


    def docut2(self,name_segs):
        """
        根据公司名字的分词列表，把公司的各个属性字段提取出来

        :param name_segs: 公司名字的分词列表
        :return com_name_items:
                ok: 返回的状态
                segs:分词的结果,这个字段只在调试的时候使用，调试结束需要删除(不需要返回该字段)
                com_loc:城市信息
                com_feature:企业特色命名
                com_type:企业公司模板
                com_tail:企业名字结尾(如"有限公司"等)
                com_sub:企业名字附加模板(如"烟台"等)
                com_subtail:企业名字附加结尾(如"分公司"等)
        """
        # 以 "广西航通石油贸易有限公司海南分公司" 为例
        # 该公司的分词结果为 ["广西", "航通", "石油贸易", "有限公司", "海南", "分公司"]
        loc_start = -1   # 标记loc字段的位置，本例中该值最终应该为0，即标记"广西"
        loc_end = -1     # 标记loc字段的终止位置, 本例中该值最终应该为0,即标记"广西"
        feture_start = -1  # 标记feture字段的起始位置
        feture_end = -1    # 标记feture字段的终止位置
        type_start = -1    # 标记type字段的起始位置
        type_end = -1      # 标记type字段的终止位置
        tail_start = -1    # 标记tail字段的起始位置
        tail_end = -1      # 标记tail字段的终止位置
        sub_start = -1     # 标记sub字段的起始位置
        sub_end = -1       # 标记sub字段的终止位置
        sub_tail_start = -1  # 标记sub_tail字段的起始位置
        sub_tail_end = -1    # 标记sub_tail字段的终止位置
        length = len(name_segs)
        # 先找到两个公司结尾部分, 即com_tail, com_sub_tail这两个字段的值
        # 遍历整个分词结果来找
        for i in range(0, length):
            # 先找到第一个公司尾缀，在本例中应该是"有限公司",下标为3，那么tail_start和tail_end应该同为3
            if name_segs[i] in self.TAILS:
                if tail_start == -1:
                    tail_start = i
                    tail_end = i
                    continue
            # 找到第一个公司尾缀之后才能再找第二个
            if tail_start != -1:
                if name_segs[i] in self.SUBTAILS:
                    if sub_tail_start == -1:
                        sub_tail_start = i
                        sub_tail_end = i
        # 拿到下标索引之后，从name_segs(分词结果列表)中将数据取出
        com_tail = name_segs[tail_start] if tail_start>-1 else ""
        com_sub_tail = name_segs[sub_tail_start] if sub_tail_start>-1 else ""
        # 我认为公司应该总存在尾缀，如果没有找到尾缀，那么就先把分词结果的最后一个做为尾缀
        if tail_start==-1 and sub_tail_start==-1:
            tail_start = length-1
        # 获取城市字段, com_loc, com_sub
        # 公司的城市字段可能有两个，比如本例中的"广西"和"海南"
        # 这里使用公司尾缀来划分，"海南"这个城市必然在公司第一个尾缀的后面
        # 那么找第一个城市，只需要在公司尾缀的前面找就行了
        for i in range(0, tail_start+1):
            if name_segs[i] in self.LOCS:
                if loc_start == -1:
                    loc_start = i
                    loc_end = i
                # 公司的城市不一定只有一个分词字段，可能需要拼接
                # 拼接的原则是,如果若干个城市字段相邻,那么就把这些城市拼接起来
                elif i-loc_end == 1:
                    loc_end = i
            # type和城市一样，都在公司尾缀的前面，随意在遍历寻找城市字段的时候，可以顺带把type也找到
            elif name_segs[i] in self.TYPES:
                type_start = i
                type_end = i
        # 找到城市字段之后再找第二个城市字段，这个城市字段应该在公司的第一个尾缀和第二个尾缀之间
        if sub_tail_start > tail_start:
            for i in range(tail_start, sub_tail_start+1):
                if name_segs[i] in self.LOCS:
                    if sub_start == -1:
                        sub_start = i
                        sub_end = i
                    # 同样，这个城市也可能需要拼接
                    elif i - sub_end == 1:
                        sub_end = i
        # 城市字段提取完成后，loc_start到loc_end的全部加起来就是com_loc的结果
        com_loc = ""
        if loc_start > -1:
            for item in range(loc_start, loc_end+1):
                com_loc += name_segs[item]
        # 同上
        com_sub = ""
        if sub_start > -1:
            for item in range(sub_start, sub_end+1):
                com_sub += name_segs[item]
        # 同上
        com_type = ""
        if type_start > -1:
            for item in range(type_start, type_end+1):
                com_type += name_segs[item]
        # 获得com_feature字段
        # 这个字段比较难准确获取,以下为各种需要处理的情况
        # 比如 "[] type 地点 ..." 表示 com_feature字段的后面是type，再后面是地点，再后面是其他
        # "[] 地名 ..." 则表示 com_feature字段的后面是地名，再后面是其它
        com_feature = ""
        if loc_start>-1:
            # [] type 地点 ...
            if type_start>-1 and type_start<loc_start:
                for i in range(0, type_start):
                    com_feature += name_segs[i]
            if not com_feature:
                # [] 地名 ...
                for i in range(0, loc_start):
                    com_feature += name_segs[i]
                if not com_feature:
                    # 地名 [] type
                    if type_start > loc_end:
                        for i in range(loc_end+1, type_start):
                            com_feature += name_segs[i]
                    # 地名 [] tail
                    else:
                        for i in range(loc_end+1, type_start):
                            com_feature += name_segs[i]
        elif type_start>0:
            # [] type ...
            for i in range(0, type_start):
                com_feature += name_segs[i]
        else:
            # [] tail ...
            for i in range(0, tail_start):
                com_feature += name_segs[i]
        # com_sub并不总是城市，如果是其它的东西，就全部拼接起来
        if not com_sub:
            if sub_tail_start>-1 and tail_end>-1:
                for i in range(tail_end+1, sub_tail_start):
                    com_sub += name_segs[i]
        com_name_items = {
            "ok":True,
            "segs":name_segs,
            "com_loc":com_loc.replace("（", "").replace("）", "").replace("(", "").replace(")", ""),
            "com_feature":com_feature.replace("（", "").replace("）", "").replace("(", "").replace(")", ""), 
            "com_type":com_type.replace("（", "").replace("）", "").replace("(", "").replace(")", ""), 
            "com_tail":com_tail.replace("（", "").replace("）", "").replace("(", "").replace(")", ""), 
            "com_sub":com_sub.replace("（", "").replace("）", "").replace("(", "").replace(")", ""), 
            "com_subtail":com_sub_tail.replace("（", "").replace("）", "").replace("(", "").replace(")", "")
        }
        #print(type_end > )
        if tail_start - type_end > 1:
            print(com_name_items)
        return com_name_items

def main():
    test_names = [
       #"兰州中力商情信息咨询有限公司",
       #"成都千寻文化传媒有限公司",
       #"绍兴市洁达工程渣土运输有限公司",
       #"芜湖凯电表面处理科技有限公司",
       #"南京荣氏商贸有限公司第八十二分公司",
        "长立商贸（宜昌）有限公司",
        "中国物资国际招商投资开发公司大连公司",
        "宝鸡有一群怀揣着梦想的少年相信在牛大叔的带领下会创造生命的奇迹网络科技有限公司---",
        "宝鸡有一群怀揣着梦想的少年相信在牛大叔的带领下会创造生命的奇迹网络科技有限公司"
        #这个里面的物资是type字典里的:物资,招商投资
    ]
    mycutter = cutter()
    error_count = 0
    all_count = len(test_names)
    name_cuts_error = {}
    new_types = {}
    for test_name in test_names:
        name_cuts = mycutter.cut(test_name)
        if not name_cuts:
            error_count +=1
            name_cuts_error[test_name] = name_cuts
            continue 
        print(name_cuts)
        if name_cuts["ok"]:
            full_type = name_cuts["com_type"] + name_cuts["com_tail"]
            new_types[full_type] = {
                "cato":name_cuts["com_type"],
                "tail":name_cuts["com_tail"]
            }
        else:
            error_count +=1
            name_cuts_error[test_name] = name_cuts
            pass
    print("错误数:"+str(error_count)+"/"+str(all_count))    
    jsonfiler.dump(name_cuts_error, "error.json", indent=4)
    jsonfiler.dump(new_types, "new_types.json", indent=4)


if __name__ == '__main__':
    main()
