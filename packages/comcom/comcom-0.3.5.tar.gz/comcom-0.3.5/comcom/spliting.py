"""

"""
import jieba
import tqdm
import re
from tqdm import tqdm
import ml3

def spliting():
    with open(r"user_dict/com_names5000.dat", "r", encoding = "utf-8") as f:
        data = f.readlines()
    data = [x.strip() for x in data][:5000]

    jieba.load_userdict("user_dict/com_types_user_dict.dat")
    jieba.load_userdict("user_dict/com_tail_user_dict.dat")
    jieba.load_userdict("user_dict/citys.dat")

    front = [""]   # 需要向前追加的列表
    com_infos = {}
    print("开始分词...")
    for name in tqdm(data):
        name = name.replace("（", "(")
        name = name.replace("）", ")")
        # pattern = re.compile(r"（.*）")
        # name = pattern.sub("", name)
        # pattern = re.compile(r"《.*》")
        # name = pattern.sub("", name)
        # name = re.sub(u"\\(.*?\\)", "", name)
        cut = jieba.cut(name)
        cut_list = []
        for word in cut:
            word = word.replace("(", "").replace(")", "").strip()
            if word:
                if word in front and cut_list:
                    cut_list[-1] += word
                else:
                    cut_list.append(word)
        com_infos[name] = cut_list
    print("分词结果写入文件...")
    ml3.tools.dump_json_file(com_infos, "results.json", indent=4)
    print("success")

def main():
    spliting()

if __name__ == "__main__":
    main()

