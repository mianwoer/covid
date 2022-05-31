import re
import os
import urllib.request


# 爬下网页代码，类型bytes
def acfun_Get(url):
    req = urllib.request.Request(url, headers=ua_headers)
    page = urllib.request.urlopen(req)
    html = page.read()
    return html


# 该函数截取百度图片网址的img地址
def get_Baidu_Pic(html):
    bdpic_html = html.decode('utf-8')
    print(type(bdpic_html))
    # bdpic_html = str(html)
    reg_baidu = r'(?<=thumbURL":")(https.*?(?=\"))'
    reg_baidupic = re.compile(reg_baidu)
    img_list = re.findall(reg_baidupic, bdpic_html)
    img_list = list(img_list)
    return img_list


if __name__ == '__main__':
    ua_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
                                ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
    baidu_pic_url = 'https://image.baidu.com/search/index?ct=201326592&cl=2&st=-1&lm=-1&nc=1&ie=utf-8&tn=baiduimage&ipn=r&rps=1&pv=&fm=rs2&word=%E5%A3%81%E7%BA%B8%E5%9B%BE%E7%89%87%20%E9%94%81%E5%B1%8F&oriquery=%E5%A3%81%E7%BA%B8&ofr=%E5%A3%81%E7%BA%B8&sensitive=0'
    baidu_pic_html = acfun_Get(baidu_pic_url)
    with open(r'C:\Users\zhuliu4\Desktop\baidu_pic.html', 'wb') as f:
        f.write(baidu_pic_html)
    baidu_img_urls = list(get_Baidu_Pic(baidu_pic_html))
    with open(r'C:\Users\zhuliu4\Desktop\baidu_pic.txt', 'w') as image:
        image.write(str(baidu_img_urls))
    dir = r'C:\Users\zhuliu4\Desktop\百度图片'
    number = 0
    if not os.path.exists(dir):
        os.mkdir(dir)
    for i in baidu_img_urls:
        output_file = os.path.join(dir, '{}.jpg'.format(number))
        print(i, output_file)
        urllib.request.urlretrieve(i, output_file)
        number += 1
