import json
import re
import os
import requests


def get_ImageUrl(url, headers):
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'  # res.text 为str类型的html源码
    re_text = r'(?<=thumbURL":")(https.*?(?=\"))'
    pattern = re.compile(re_text)
    match_text = re.findall(pattern, res.text)
    return match_text


def get_res_json(url, headers) -> str:
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    # print(type(res.content))
    return res.content.decode('utf-8')  # res.content为byte类型


if __name__ == '__main__':
    headers = {
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        # 'Accept-Encoding': 'gzip, deflate, sdch',
        # 'Accept-Language': 'zh-CN,zh;q=0.8',
        # 'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/100.0.4896.75 Safari/537.36'
    }
    url = 'https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?province='

    # res = json.dumps(get_res(url, headers).decode('utf-8'))
    provinces = ['湖北', '安徽', '上海', '湖南', '广东']
    dir = r'C:\Users\zhuliu4\Desktop\covid_info'
    # number = 0
    if not os.path.exists(dir):
        os.mkdir(dir)
    data = []
    for province in provinces:
        res = get_res_json(url + province, headers)  # res是json格式，ptyhon识别为str
        # output_file = os.path.join(dir, province + '.txt')
        output_file = os.path.join(dir, '全国.txt')
        data += json.loads(res)['data']  # res转换成字典格式，随后去data部分数据
    with open(output_file, 'w') as file:
        file.write(str(data))
    # for i in res:
    #     output_file = os.path.join(dir, '{}.jpg'.format(number))
    #     print(i, output_file, requests.get(i).content)
    #     # urlllib.request.urlretrieve(i, output_file)
    #     number += 1
