import imageio.v2
import jieba
import requests
import re, os
import jieba.analyse
from wordcloud import WordCloud, STOPWORDS
from imageio import imread
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号 #有中文出现的情况，需要u'内容'
comment_path = 'bilibili1.csv'
if os.path.exists(comment_path):
    os.remove(comment_path)


def get_cid(BV):
    cidurl = f'https://api.bilibili.com/x/player/pagelist?bvid={BV}&jsonp=jsonp'
    headers = {
        "cookie": "buvid3=F942B32B-43AC-FCDF-6E09-6DD855E9FA0601384infoc; buvid4=5CEE2C66-3E07-5302-D83C-766198380E7C02378-022032419-m4T90WVXeag15sInPdSApA%3D%3D; buvid_fp=6ec5f5ae8ff3cb1b991959f3c93eb519; b_nut=100; _uuid=1C88310AC-8B8F-CF99-10DE1-CA22AE7D58FC53060infoc; FEED_LIVE_VERSION=V8; header_theme_version=CLOSE; home_feed_column=4; browser_resolution=962-920; CURRENT_FNVAL=4048; SESSDATA=45ae8951%2C1709699058%2Ce1fc1%2A91; bili_jct=0138f8e4b63c9a9932f810410e3e3064; DedeUserID=12983819; DedeUserID__ckMd5=b701a17483aa8790; rpdid=|(J|lmRkmulJ0J'uYmuukY~lR; fingerprint=6ec5f5ae8ff3cb1b991959f3c93eb519; buvid_fp_plain=undefined; CURRENT_QUALITY=116; bp_video_offset_12983819=838969501359800323; PVID=2; LIVE_BUVID=AUTO5816913242132159; CURRENT_BLACKGAP=0; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTQzNjQyNTIsImlhdCI6MTY5NDEwNTA1MiwicGx0IjotMX0.wfqY8QmVdO0PIzTpZQLo00GQKQkJSgRVZ1iyimA0yV0; bili_ticket_expires=1694364252; b_lsid=779CCAB1_18A7D8C0794; sid=8ro2tlgc; bsource=search_bing",
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0'
    }
    cidres = requests.get(cidurl, headers=headers)
    # print(cidres.json())
    cid = cidres.json()['data'][0]['cid']
    # print(cid)
    return cid


def spider(cid):
    url = f'https://comment.bilibili.com/{cid}.xml'
    headers = {
        "cookie": "buvid3=F942B32B-43AC-FCDF-6E09-6DD855E9FA0601384infoc; buvid4=5CEE2C66-3E07-5302-D83C-766198380E7C02378-022032419-m4T90WVXeag15sInPdSApA%3D%3D; buvid_fp=6ec5f5ae8ff3cb1b991959f3c93eb519; b_nut=100; _uuid=1C88310AC-8B8F-CF99-10DE1-CA22AE7D58FC53060infoc; FEED_LIVE_VERSION=V8; header_theme_version=CLOSE; home_feed_column=4; browser_resolution=962-920; CURRENT_FNVAL=4048; SESSDATA=45ae8951%2C1709699058%2Ce1fc1%2A91; bili_jct=0138f8e4b63c9a9932f810410e3e3064; DedeUserID=12983819; DedeUserID__ckMd5=b701a17483aa8790; rpdid=|(J|lmRkmulJ0J'uYmuukY~lR; fingerprint=6ec5f5ae8ff3cb1b991959f3c93eb519; buvid_fp_plain=undefined; CURRENT_QUALITY=116; bp_video_offset_12983819=838969501359800323; PVID=2; LIVE_BUVID=AUTO5816913242132159; CURRENT_BLACKGAP=0; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTQzNjQyNTIsImlhdCI6MTY5NDEwNTA1MiwicGx0IjotMX0.wfqY8QmVdO0PIzTpZQLo00GQKQkJSgRVZ1iyimA0yV0; bili_ticket_expires=1694364252; b_lsid=779CCAB1_18A7D8C0794; sid=8ro2tlgc; bsource=search_bing",
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0'
    }
    resq = requests.get(url, headers=headers)
    resq.encoding = resq.apparent_encoding
    content_list = re.findall('<d p=".*?">(.*?)</d>', resq.text)
    # print(content_list)
    for item in content_list:
        with open(comment_path, 'a', encoding='utf-8') as fin:
            fin.write(item + '\n')
        # print(item)
    # print("down")


def chinese_word_cut(mytext):
    jieba.initialize()  # 初始化jieba
    # 文本预处理 ：去除一些无用的字符只提取出中文出来
    new_data = re.findall('[\u4e00-\u9fa5]+', mytext, re.S)
    wordcount = Counter(new_data).most_common(20)
    print("词频前二十的词语为：",wordcount)
    new_data = " ".join(new_data)
    # print(new_data)
    # 文本分词
    seg_list_exact = jieba.lcut(new_data)
    result_list = []
    # 读取停用词库
    with open('stopwords.txt', encoding='utf-8') as f:  # 可根据需要打开停用词库，然后加上不想显示的词语
        con = f.readlines()
        stop_words = set()
        for i in con:
            i = i.replace("\n", "")  # 去掉读取每一行数据的\n
            stop_words.add(i)
    # 去除停用词并且去除单字
    for word in seg_list_exact:
        if word not in stop_words and len(word) > 1:
            result_list.append(word)
    return result_list


def get_serch(keyword, page):
    headers = {
        "cookie": "buvid3=F942B32B-43AC-FCDF-6E09-6DD855E9FA0601384infoc; buvid4=5CEE2C66-3E07-5302-D83C-766198380E7C02378-022032419-m4T90WVXeag15sInPdSApA%3D%3D; buvid_fp=6ec5f5ae8ff3cb1b991959f3c93eb519; b_nut=100; _uuid=1C88310AC-8B8F-CF99-10DE1-CA22AE7D58FC53060infoc; FEED_LIVE_VERSION=V8; header_theme_version=CLOSE; home_feed_column=4; browser_resolution=962-920; CURRENT_FNVAL=4048; SESSDATA=45ae8951%2C1709699058%2Ce1fc1%2A91; bili_jct=0138f8e4b63c9a9932f810410e3e3064; DedeUserID=12983819; DedeUserID__ckMd5=b701a17483aa8790; rpdid=|(J|lmRkmulJ0J'uYmuukY~lR; fingerprint=6ec5f5ae8ff3cb1b991959f3c93eb519; buvid_fp_plain=undefined; CURRENT_QUALITY=116; bp_video_offset_12983819=838969501359800323; PVID=2; LIVE_BUVID=AUTO5816913242132159; CURRENT_BLACKGAP=0; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTQzNjQyNTIsImlhdCI6MTY5NDEwNTA1MiwicGx0IjotMX0.wfqY8QmVdO0PIzTpZQLo00GQKQkJSgRVZ1iyimA0yV0; bili_ticket_expires=1694364252; b_lsid=779CCAB1_18A7D8C0794; sid=8ro2tlgc; bsource=search_bing",
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0'
    }
    url = f'https://api.bilibili.com/x/web-interface/wbi/search/type?page={page}&page_size=42&keyword={keyword}&search_type=video'
    res = requests.get(url, headers=headers).json()
    video_data = [item for item in res["data"]["result"] if item.get("type") == "video"]  # 获取每个result代码块中type为video的
    bvid_list = []
    for item in video_data:
        bvid_list.append(item['bvid'])
    return bvid_list


def get_bvlist(key):
    bv_list = []
    for i in range(1, 9):
        bv_list.extend(get_serch(key, i))
    # print(len(bv_list))
    return bv_list


def data_visual():
    with open(comment_path, encoding='utf-8') as file:
        comment_text = file.read()
        wordlist = chinese_word_cut(comment_text)

        new_wordlist = ' '.join(wordlist)
        mask = np.array(Image.open('rr.jpg'))
        wordcloud = WordCloud(font_path='C:/Windows/Fonts/msyh.ttc', collocations=False,
                              background_color="white",mask=mask).generate(new_wordlist)
        wordcloud.to_file('picture1.png')

        # 生成柱状图
        word_count = Counter(wordlist)
        top_words = word_count.most_common(10)  # 获取词频最高的前10个词语
        top_words, top_word_counts = zip(*top_words)
        plt.figure(figsize=(10, 6))
        plt.bar(top_words, top_word_counts)
        plt.xlabel('词语')
        plt.ylabel('词频')
        plt.title('词频统计柱状图')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('bar_chart.png')
        plt.show()

        # 生成饼图
        plt.figure(figsize=(8, 8))
        plt.pie(top_word_counts, labels=top_words, autopct='%1.1f%%')
        plt.title('词频统计饼图')
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig('pie_chart.png')
        plt.show()


if __name__ == '__main__':
    #key = input("请输入想要搜索的关键词：")
    key="日本核污染水排海"
    bv_list = get_bvlist(key)
    for i in range(300):
        spider(get_cid(bv_list[i]))
    data_visual()
