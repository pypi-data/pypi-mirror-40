    def docut2(self,name_segs):
        """
        根据公司名字的分词列表，把公司的各个属性字段提取出来

        :param name_segs: 公司名字的分词列表
        :return com_name_items:
                ok: 返回的状态
                segs:分词的结果,这个字段只在调试的时候使用，调试结束需要删除(不需要返回该字段)
                com_loc:城市信息
                com_feature:企业特色命名
                com_etype:企业公司模板
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
            elif name_segs[i] in self.ETYPES:
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
        com_etype = ""
        if type_start > -1:
            for item in range(type_start, type_end+1):
                com_etype += name_segs[item]
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
            "com_etype":com_etype.replace("（", "").replace("）", "").replace("(", "").replace(")", ""), 
            "com_tail":com_tail.replace("（", "").replace("）", "").replace("(", "").replace(")", ""), 
            "com_sub":com_sub.replace("（", "").replace("）", "").replace("(", "").replace(")", ""), 
            "com_subtail":com_sub_tail.replace("（", "").replace("）", "").replace("(", "").replace(")", "")
        }
        #print(type_end > )
        if tail_start - type_end > 1:
            print(com_name_items)
        return com_name_items


