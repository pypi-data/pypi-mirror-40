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
from tqdm import tqdm
from collections import Counter

#参考:http://baijiahao.baidu.com/s?id=1604832028977288918&wfr=spider&for=pc
"""
公司起名看似简单，实则有很多门道。 
公司名字由四个部分组成，地域+字号+行业特点+类型。
有些公司名字没有地域，是因为在局核名。 
首先，你要确定公司的类型，比如要确定公司的类型。是有限责任公司、股份有限公司、合伙企业、个人独资企业等。 
然后，你要选择哪个行业特点。投资公司，科技公司，商贸公司等等。 最后就是公司的字号。 举个例子：律晓宇（北京）投资管理有限公司， 律晓宇是字号，北京是地域，投资管理是行业，有限公司是类型。
"""
#https://zhidao.baidu.com/question/918547007801744099.html
"""
个人独资企业的名称可以叫厂、店、部、中心、工作室等。
根据《个人独资企业登记管理办法》第六条 个人独资企业的名称应当符合名称登记管理有关规定，并与其责任形式及从事的营业相符合。
个人独资企业的名称中不得使用“有限”、“有限责任”或者“公司”字样

"""
#https://zhidao.baidu.com/question/271939034.html
"""
合伙企业名称中的组织形式后应当标明“普通合伙”“特殊普通合伙”或者“有限合伙”字样。

"""
#https://zhidao.baidu.com/question/552821234.html
"""
经营者姓名可作字号，不得用“中国”等字词：个体工商户名称由行政区划、字号、行业、组织形式依次组成。经营者姓名可以作为个体工商户名称中的字号使用。个体工商户名称中的行业应当反映其主要经营活动内容或者经营特点，名称中的组织形式可以用“厂”、“店”、“馆”、“部”、“行”、“中心”等字样，但不得使用“企业”、“公司”和“农民专业合作社”字样。
"""
#https://baike.baidu.com/item/%E4%BC%81%E4%B8%9A%E5%90%8D%E7%A7%B0%E7%99%BB%E8%AE%B0%E7%AE%A1%E7%90%86%E8%A7%84%E5%AE%9A/7954344?fr=aladdin
"""
企业名称管理制度
"""
class Lookingfor(Enum):
    LOC     = 1
    FEATURE = 2
    INDUSTRY= 4
    TYPE    = 5
    TAIL    = 6
    SUB     = 7
    SUBTAIL = 8
    ENDLESS = 9

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
        
        # com_etypes的库
        path_etypes = os.path.join(self.module_path,"user_dict","user_dict_com_etypes.json")
        ETYPES_DICT = jsonfiler.load(path_etypes)
        self.ETYPES_DICT = ETYPES_DICT
        self.ETYPES = [x.strip() for x in ETYPES_DICT.keys()]
        self.ETYPES_SET = set(self.ETYPES)

        # com_etypes_weight库
        path_etypes = os.path.join(self.module_path,"user_dict","user_dict_com_etypes_weight.json")
        self.ETYPEW = jsonfiler.load(path_etypes)
        

        # com_industries的库
        path_types = os.path.join(self.module_path,"user_dict","user_dict_com_industries.dat")
        with open(path_types, "r", encoding="utf8") as f:
            INDUSTRIES = f.readlines()
        self.INDUSTRIES = [x.strip() for x in INDUSTRIES]
 
        # com_type的库
        path_types = os.path.join(self.module_path,"user_dict","user_dict_com_types.dat")
        with open(path_types, "r", encoding="utf8") as f:
            TYPES = f.readlines()
        self.TYPES = [x.strip() for x in TYPES]

        # com_tail的库
        path_tails = os.path.join(self.module_path,"user_dict","user_dict_com_tails.dat")
        with open(path_tails, "r", encoding = "utf-8") as f:
            TAILS = f.readlines()
        self.TAILS = [x.strip() for x in TAILS]
       
        # TYEPS要extendTAILS
        self.ETYPES.extend(self.TAILS)

        # com_subs的库跟city的库是同一个
        self.SUBS = LOCS
        
        # com_sub_tail的库跟tail的库是同一个
        path_types = os.path.join(self.module_path,"user_dict","user_dict_com_sub_tails.dat")
        with open(path_types, "r", encoding="utf8") as f:
            SUBTAILS = f.readlines()
        self.SUBTAILS = [x.strip() for x in SUBTAILS]
        
        #对公司名进行分词
        jieba.load_userdict(os.path.join(self.module_path,"user_dict","user_dict_com_etypes.dat"))
        jieba.load_userdict(os.path.join(self.module_path,"user_dict","user_dict_com_types.dat"))
        jieba.load_userdict(os.path.join(self.module_path,"user_dict","user_dict_com_industries.dat"))
        jieba.load_userdict(os.path.join(self.module_path,"user_dict","user_dict_com_sub_tails.dat"))
        jieba.load_userdict(os.path.join(self.module_path,"user_dict","user_dict_com_tails.dat"))
        jieba.load_userdict(os.path.join(self.module_path,"user_dict","user_dict_com_citys.dat"))
        self.jieba = jieba        
        #对公司名片段进行映射的映射表
        name_rmap = jsonfiler.load(os.path.join(self.module_path,"user_dict","user_dict_com_etypes.json"))   
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

    def extend_name_segs(self,name_segs):
        name_segs_extended = []
        for name_seg in name_segs:
            if len(name_seg) <=3:
                name_segs_extended.append(name_seg)
                continue

            if name_seg not in self.name_rmap:
                name_segs_extended.append(name_seg)
            elif len(self.name_rmap[name_seg])>=2:
                name_segs_extended.extend(self.name_rmap[name_seg])
            else:
                name_segs_extended.append(name_seg)
        return name_segs_extended



    #这里是选择最好的公司type而不是公司etype,所以要先把name_segs给分隔开
    def decide_best_type(self,name_segs):
        com_name  = "".join(name_segs)
        name_segs = self.extend_name_segs(name_segs)
        best_type = ""
        
        popular_com_types = [
            "有限责任公司",
            "股份有限公司",
            "有限公司",
            "股份公司",
            "集团公司"
        ]
        
        #如果企业名中含有流行的模式,应该立即返回.
        for  k in popular_com_types:
            if k in com_name:
                best_type = k
                return best_type
        
        
        possible_types = list(set(name_segs) & set(self.TYPES))
        if possible_types ==[] :
            return ""
        #从name_segs和types里的交集选择一个最长的作为潜在的最好的type,如果
        #遇到"商城"和"商行"这两个选择,需要借助如下原则
        #只有industry后面的seg才能算best_type
        #'临沂', '商城', '王家', '瑶', '劳保服装', '商行'
        #如果不判断industry很容易把商城当作type
        best_type = possible_types[0]
        possible_types_dict = {}

        for k in possible_types:
            possible_types_dict[k] = self.ETYPEW[k] if k in self.ETYPEW else 0

        top_types_list = sorted(possible_types_dict,reverse=True)
        best_type = top_types_list[0]
        """        
        get_industry = False
        for seg in name_segs:
            if seg not in segs_shared:
                continue
            if len(seg) > len(best_type):
                best_type = seg
            if seg in self.INDUSTRIES:
                get_industry = True
            if get_industry and seg in possible_types:
                best_type = seg
        """
        return best_type



    def cut(self,com_name):
        #以下是要获取的企业Logo信息所需要的元素,企业Logo名应该由,
        #1. 企业所在的省, com_province
        #2. 企业所在的市, com_city
        #2. 企业所在的县, com_district
        #3. 企业特色命名, com_feature
        #4. 企业公司行业, com_industry
        #4. 企业公司类型, com_type
        #5. 企业名字后缀, com_tail
        #5. 企业名字后缀, com_sub
        #5. 企业名字后缀, com_sub_tail
        #   根据一定原则生成最好的logo名字，如果四个字更好
        #   企业的全名一定是:
        #   企业省 + 企业市 + 企业特色 + 企业模板 + 企名后缀 
        com_province        = ""
        com_city            = ""
        com_loc             = ""
        com_feature         = ""
        com_tail            = ""
        com_sub             = ""
        com_subtail         = ""
        com_logo            = ""
        com_braced          = ""
        com_type_best       = ""
        com_industry        = ""
        com_type            = ""

        com_name = self.reform(com_name)
        if not self.validate(com_name):
            return None

        rep = re.compile("\((.*)\)")
        braced_strs = re.findall(rep, com_name)
        m_strs = list(map(lambda x:"(" + str(x) + ")", braced_strs))
        for i in m_strs:
            com_name = com_name.replace(i, "")
        com_braced = ",".join(braced_strs)
        #我们大致估计括号里的都是地名 所以把括号里的拿出来 放到开头

        #把公司的()里面的内容提取出来,当做地名放到name_segs的最前面
        cut_segs = jieba.cut(com_name)
        name_segs = list(cut_segs)
       
        #如果企业名字里有"",要替换掉
        if "" in name_segs:
            name_segs.remove("")

        if len(com_name) <=3:
            return {"ok":False,"com_segs":name_segs}
        
        #状态机逆序搜索，确认企业名字的最后一个短语
        #江西添福养老服务有限公司大码头社区居家养老服务中心
        name_end = ""
        for seg in reversed(name_segs):
            if seg in self.TAILS or seg in self.SUBTAILS or seg in self.ETYPES or seg in self.TYPES:
                name_end = seg+name_end
            else:
                break
        #把etype的完整词汇再模拟分词效果分回去
        """
        ['北京', '光明', '健康乳业', '销售有限公司', '天津', '第一分', '公司']
        ['北京', '光明', '健康乳业', '销售', '有限公司', '天津', '第一分', '公司']
        """
        #print(name_segs_extended)
        #确认企业名字的type字段,把企业的segs和types求交集
        best_type = self.decide_best_type(name_segs)
        #状态机正序搜索
        ok_flag = True
        cur_state = Lookingfor.LOC
        for seg in name_segs:
            if cur_state is Lookingfor.LOC:
                if seg in self.LOCS:
                    com_loc +=seg
                elif seg in ["中国","省","市","区","县","村","乡","镇","堡"]:
                    com_loc +=seg
                elif seg in self.ETYPES_DICT and best_type in seg:
                    com_etype = seg
                    com_etype_extend = self.ETYPES_DICT[seg]
                    if "+" in com_etype_extend:
                        com_etype_list = com_etype_extend.split("+")
                        com_industry = com_etype_list[0]
                        com_type = com_etype_list[1]
                        cur_state =  Lookingfor.TYPE
                    else:
                        com_type = com_etype
                        cur_state = Lookingfor.TYPE
                elif seg in self.INDUSTRIES:
                    com_industry += seg
                    cur_state = Lookingfor.INDUSTRY
                elif seg == best_type:
                    com_type += seg
                    cur_state = Lookingfor.TYPE
                else:
                    com_feature +=seg
                    cur_state = Lookingfor.FEATURE
                continue

            elif cur_state is  Lookingfor.FEATURE:
                if seg in self.ETYPES_DICT and best_type in seg:
                    com_etype = seg
                    com_etype_extend = self.ETYPES_DICT[com_etype]
                    if "+" in com_etype_extend:
                        com_etype_list = com_etype_extend.split("+")
                        com_industry = com_etype_list[0]
                        com_type = com_etype_list[1]
                        cur_state =  Lookingfor.TYPE
                    else:
                        com_type = com_etype
                        cur_state = Lookingfor.TYPE
                elif seg == best_type:
                    com_type += seg
                    cur_state = Lookingfor.TYPE
                elif seg in self.INDUSTRIES:
                    com_industry += seg
                    cur_state = Lookingfor.INDUSTRY
                else:
                    com_feature +=seg
                continue
            #能进这个状态,说明实现已经找到industries了
            elif cur_state is  Lookingfor.INDUSTRY:
                if seg == best_type:
                    com_type += seg
                    cur_state = Lookingfor.TYPE
                else:
                    #如果在Industry，那一定要继续找type,在找到type之前,所有的都算industry
                    com_industry += seg
                continue 
            
            #能进这个状态,说明实现已经找到industry了
            elif cur_state is  Lookingfor.TYPE:
                if seg in self.TAILS:
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
            

        name_segs_full = self.extend_name_segs(name_segs)

        com_name_items = {
            "ok":ok_flag,
            "com_segs":name_segs,
            "com_segs_full":name_segs_full,
            "com_type_best":best_type,
            "com_loc:":com_loc,
            "com_feature":com_feature,  
            "com_industry":com_industry,
            "com_type":com_type,
            "com_tail":com_tail, 
            "com_sub":com_sub, 
            "com_subtail":com_subtail,
            "com_braced":com_braced
        }
        
       
        if com_name_items["com_industry"] == "" and com_name_items["com_type"] == "":
            com_name_items["ok"] = False
        if com_name_items["com_industry"] == "":
            com_name_items["ok"] = False
        
        com_name_items["name"] = com_name
        return com_name_items

    def docut(self,name_segs):
        return com_name_items


def main():
    test_names = [
        #"兰州中力商情信息咨询有限公司",
        #"成都千寻文化传媒有限公司",
        #"绍兴市洁达工程渣土运输有限公司",
        #"芜湖凯电表面处理科技有限公司",
        #"南京荣氏商贸有限公司第八十二分公司",
        #"长立商贸（宜昌）有限公司",
        #"中国物资国际招商投资开发公司大连公司",
        #"宝鸡有一群怀揣着梦想的少年相信在牛大叔的带领下会创造生命的奇迹网络科技有限公司",
        #"北京光明健康乳业销售有限公司天津第一分公司",
        #"临沂商城王家瑶劳保服装商行",
        #"西宁市城中区赏延斋书画社",
        #"上海君为中草药种植专业合作社"
        #"兰州中力商情信息咨询有限公司",
        #"南京荣氏商贸有限公司第八十二分公司"
        #这个里面的物资是type字典里的:物资,招商投资
    ]
    
    with open("user_dict/solo_types.dat", "r", encoding="utf8") as f:
        solo_types = f.readlines()
        solo_types = [x.strip() for x in solo_types]
    
    #test_names = jsonfiler.load("json/com_names_combasic_107w.json")
    #test_names = jsonfiler.load("json/com_error_names.json")
    test_names = jsonfiler.load("json/com_names_5w.json")[:1000]
    mycutter = cutter()
    error_count = 0
    all_count = len(test_names)
    name_cuts_error = {}
    new_types = {}
    bad_segs  = []
    for test_name in tqdm(test_names):
        name_cuts = mycutter.cut(test_name)
        if not name_cuts:
            error_count +=1
            name_cuts_error[test_name] = name_cuts
            continue 
        
        if not name_cuts["ok"]:
            error_count +=1
            name_cuts_error[test_name] = name_cuts
            bad_segs.extend(name_cuts["com_segs"])
            pass
    
    print("错误数:"+str(error_count)+"/"+str(all_count))    
    jsonfiler.dump(name_cuts_error, "error.json", indent=4)
    jsonfiler.dump(list(name_cuts_error.keys()), "error_names.json", indent=4)
    name_list = Counter(bad_segs).most_common()
    namestr_list = []
    min_freq = 0
    new_types = []
    for name in tqdm(name_list):
        if int(name[1]) > min_freq:
            com_name = name[0]+":"+str(name[1])
            for solo_type in solo_types:
                if name[0].endswith(solo_type):
                    namestr_list.append(com_name)
   
    jsonfiler.dump(namestr_list, "bad_segs.json", indent=4)


if __name__ == '__main__':
    main()
