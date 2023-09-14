import requests
import re

header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }

def get_Response(html_Url):  # 对于任意一个网址url，获取其html文件
    
    response = requests.get(html_Url, headers=header)
    if response.ok:
        response.encoding = 'utf-8'
        return response
    # 如果执行到这一步，就说明请求失败，报错并退出
    print(f"请求网页失败,状态码：{response.status_code}")
    SystemExit()

def get_Target_Video(target, num): # 从B站搜索栏中找排名前num的视频，爬取他们的BV号，target为搜索内容
    matches = []
    page = 0
    #从格式为 bvid:"BV....."中提取BV号
    match_Text = r'bvid:"([^"]+)"'
    for index in range(0,num,42): # 每次爬取42个BV号
        target_Url = f"https://search.bilibili.com/all?keyword={target}&o={index}&page={page}"
        print(target_Url)
        content = requests.get(target_Url,headers= header).text
        print(content)
        print(re.findall(match_Text,content))
        matches.extend(re.findall(match_Text,content))
        page += 1
    return matches[0:num]

    

def get_Cid(BV):  # 对于一个B站视频网址，获取其cid(即存储弹幕的网站key),输入为BV号
    bili_Url = f"https://www.ibilibili.com/video/{BV}/"
    content = get_Response(bili_Url).text
    # 我们用正则从html文件中提取 "bcid":"1252950136" 中的cid号
    match_Text = r'"bcid":"(\d*)"'
    match = re.search(match_Text, content)
    if match:
        cid = match.group(1)
        return cid
    # 如果执行到这一步，说明没有匹配到cid，报错并退出
    print("解析弹幕cid失败")
    SystemExit()


def get_Danmaku(cid):  # 对于一个cid，进入弹幕网站并爬取弹幕
    # danmaku(だんまく)就是弹幕的意思
    danmaku_Url = f"https://api.bilibili.com/x/v1/dm/list.so?oid={cid}"
    content = get_Response(danmaku_Url).text
    # 这样写看上去和上一个函数没什么两样，但我觉得可读性应该会好一点
    match_Text = r'<d[^>]*>([^<]+)</d>'  # 这次的格式是<d p=......>我是弹幕</d>
    matches = re.findall(match_Text, content)
    for match in matches:
        print(match)


def main():
    target = "日本核污染水排海"
    matches = get_Target_Video(target,50)
    


if __name__ == "__main__":
    main()
    # input("Press <Enter> to close\n")
