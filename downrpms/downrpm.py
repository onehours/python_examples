import requests
from uaeragent import getheaders
import os
import parsel
from urllib.parse import urljoin
import shutil
import  time

url = 'https://mirrors.cloud.tencent.com/epel/6/x86_64/'

filename = "urllist.txt"

def downfile(fileurl,filepath):
    print("正在下载:",filepath)
    try:
        #file_data = requests.get(url=fileurl,headers=getheaders()).content 
        with requests.get(url=fileurl, stream=True) as r:
            with open(filepath, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
    except Exception as e:
        # 异常处理只是打印 相当于跳过
        print("异常：",e)
    return True

def urlparsel(url):
    res = requests.get(url,headers=getheaders())
    res.raise_for_status()
    selector = parsel.Selector(res.text)
    for i in selector.css('a::attr(href)')[1:]:
        href = i.get()
        # 拼接url和文件路径
        absolute_url = urljoin(url, href)
        # 判断是否是目录
        if href[-1] == '/':   
            # 递归解析页面
            urlparsel(absolute_url)
        else:
            # 把获取的rpm链接保存到文件中
            with open(filename,mode='a+',encoding='utf-8') as f:
                f.write(f"{absolute_url}\n")

if os.path.exists(filename):
    status = 0
    with open("down_status",mode='r',encoding='utf-8') as f2:
        status = int(f2.read())
    with open(filename,mode='r',encoding='utf-8') as f:
        if status:
            f.seek(status)
        while True:
            try:
                i = f.readline()
                fileurl = i.strip()
                # 读取空的时候退出运行
                if not fileurl:
                    break
                filepath = fileurl.replace(url,'')
                pathname, filename = os.path.split(filepath)
                if pathname and not os.path.exists(pathname):
                    os.makedirs(pathname, exist_ok=True) # 忽略已存在的目录错误
                if filepath and  os.path.exists(filepath):
                    continue
                if downfile(fileurl,filepath):
                    with open("down_status",mode='w+',encoding='utf-8') as f2:
                        f2.write(str(f.tell()))
            except Exception as e:
                print(e)
            
else:
    print("xiazai url")
    urlparsel(url)

