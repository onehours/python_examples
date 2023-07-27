import requests
import os
import parsel
from urllib.parse import urljoin

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}

#url = 'https://mirrors.cloud.tencent.com/epel/6/x86_64/'
url = 'https://repo.saltproject.io/salt/py3/redhat/7/x86_64/latest/'

def downfile(fileurl):
    filepath = fileurl.replace(url,'')
    pathname, filename = os.path.split(filepath)
    if pathname and not os.path.exists(pathname):
        os.makedirs(pathname, exist_ok=True) # 忽略已存在的目录错误
    if filepath and  os.path.exists(filepath):
        return
    print("正在下载:",filepath)
    file_data = requests.get(url=fileurl,headers=headers).content 
    with open(filepath,'wb') as fp: 
        fp.write(file_data)


def urlparsel(url):
    res = requests.get(url,headers=headers)
    res.raise_for_status()
    selector = parsel.Selector(res.text)
    for i in selector.css('a::attr(href)')[1:]:
        href = i.get()
        # 拼接url
        absolute_url = urljoin(url, href)
        if href[-1] == '/':     
            # 递归解析页面
            urlparsel(absolute_url)
        else:
            # 文件下载
            downfile(absolute_url)

urlparsel(url)
