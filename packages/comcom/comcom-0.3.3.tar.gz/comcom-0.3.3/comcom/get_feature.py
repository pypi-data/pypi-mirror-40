"""
整合公司信息成6个要素，这6个要素分别是：
        com_loc:城市(例如：广东)
        com_feature:公司特色名字(例如：南海松岗宏兴)
        com_type:公司行业标识(例如：液压机械)
        com_tail:结尾(例如：有限公司)
        com_sub:附加信息的城市(例如：福建)
        com_sub_tail:附加信息的结尾(例如：分公司)
"""
import ml3

# com_loc的库
with open(r"data/citys.dat", "r", encoding="utf-8") as f:
    LOCS = f.readlines()
LOCS = [x.strip() for x in LOCS]

# com_type的库
with open("data/com_types.dat", "r", encoding="utf8") as f:
    TYPES = f.readlines()
TYPES = [x.strip() for x in TYPES]

# com_tail的库
with open(r"data/tails.dat", "r", encoding = "utf-8") as f:
    TAILS = f.readlines()
TAILS = [x.strip() for x in TAILS]

# com_subs的库跟city的库是同一个
SUBS = LOCS

# com_sub_tail的库跟tail的库是同一个
SUB_TAILS = TAILS

def get_merge():
    com_infos = ml3.tools.load_json_file("data/results.json")
    merges = {}
    for com, pro in com_infos.items():
        comname = com
        info = do_merge(com, pro)
        merges[com] = info
    ml3.tools.dump_json_file(merges, "data/merges.json", indent=4)

def do_merge(name, res):
    global LOCS
    global TYPES
    global TAILS
    global SUBS
    global SUB_TAILS
    # 标记loc字段的位置
    loc_start = -1
    loc_end = -1
    # 标记feture字段的位置
    feture_start = -1
    feture_end = -1
    # 标记type字段的位置
    type_start = -1
    type_end = -1
    # 标记tail字段的位置
    tail_start = -1
    tail_end = -1
    # 标记sub字段的位置
    sub_start = -1
    sub_end = -1
    # 标记sub_tail字段的位置
    sub_tails_start = -1
    sub_tails_end = -1
    length = len(res)
    # 先找到两个公司结尾部分, com_tail, com_sub_tail
    for i in range(0, length):
        if res[i] in TAILS:
            if tail_start == -1:
                tail_start = i
                tail_end = i
            else:
                sub_tails_start = i
                sub_tails_end = i
    com_tail = res[tail_start] if tail_start>-1 else ""
    com_sub_tail = res[sub_tails_start] if sub_tails_start>-1 else ""
    if tail_start==-1 and sub_tails_start==-1:
        tail_start = length-1
    # print("com_tail:" + com_tail)
    # print("com_sub_tail:" + com_sub_tail)
    # 获取城市字段, com_loc, com_sub， 同时获取公司行业标识com_type
    # 把公司分成 city1 公司 city2 分公司
    # 获得city1
    for i in range(0, tail_start+1):
        if res[i] in LOCS:
            if loc_start == -1:
                loc_start = i
                loc_end = i
            elif i-loc_end == 1:
                loc_end = i
        elif res[i] in TYPES:
            type_start = i
            type_end = i
    # 获得city2
    if sub_tails_start > tail_start:
        for i in range(tail_start, sub_tails_start+1):
            if res[i] in LOCS:
                if sub_start == -1:
                    sub_start = i
                    sub_end = i
                elif i - sub_end == 1:
                    sub_end = i
    com_loc = ""
    if loc_start > -1:
        for item in range(loc_start, loc_end+1):
            com_loc += res[item]
    com_sub = ""
    if sub_start > -1:
        for item in range(sub_start, sub_end+1):
            com_sub += res[item]
    com_type = ""
    if type_start > -1:
        for item in range(type_start, type_end+1):
            com_type += res[item]
    # 获得com_feature字段
    com_feature = ""
    if loc_start>-1:
        # [] 地名 ...
        for i in range(0, loc_start):
            com_feature += res[i]
        if not com_feature:
            # 地名 [] type
            if type_start > loc_end:
                for i in range(loc_end+1, type_start):
                    com_feature += res[i]
            # 地名 [] tail
            else:
                for i in range(loc_end+1, type_start):
                    com_feature += res[i]
    elif type_start>0:
        # [] type ...
        for i in range(0, type_start):
            com_feature += res[i]
    else:
        # [] tail ...
        for i in range(0, tail_start):
            com_feature += res[i]
    com_infos = {"com_loc":com_loc,"com_feature":com_feature, "com_type":com_type, 
                "com_tail":com_tail, "com_sub":com_sub, "com_sub_tail":com_sub_tail}
    print(name)
    print(com_infos)
    # if not com_loc:
    #     print(name)
    #     print(res)
    #     print(com_infos)
    # if not com_type and not com_loc:
    #     print(name)
    #     print(res)
    #     print(com_infos)
    return com_infos

def main():
    get_merge()
    # name = "西安普雷尔斯文体竞技俱乐部"
    # res = ['西安', '普雷', '尔斯', '文体', '竞技俱乐部']
    # print(name)
    # do_merge(name, res)

if __name__ == "__main__":
    main()

