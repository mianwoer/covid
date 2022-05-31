from __future__ import absolute_import
import json
from tutorial.celery import app
from datetime import datetime
import requests


# from covid_ksh_demo.pachong import lishishuju, yqday, yqveryday, ssrd, parse, fxdq, Moon_Tow_Near

# 数据更新
@app.task
def start_get_data():
    print('正在获取历史数据...')
    requests.get('http://127.0.0.1:9000/covid_ksh/v1/HistoryDataUpdate')  # 历史数据
    print('正在获取中国今日疫情情况...')
    requests.get('http://127.0.0.1:9000/covid_ksh/v1/YQToday')  # 中国今日疫情情况
    print('正在获取中国每日疫情...')
    requests.get('http://127.0.0.1:9000/covid_ksh/v1/YqEveryday')  # 中国每日疫情
    print('正在获取实时热点...')
    requests.get('http://127.0.0.1:9000/covid_ksh/v1/SsrdUpdate')  # 实时热点
    print('正在获取国内各省目前疫情...')
    requests.get('http://127.0.0.1:9000/covid_ksh/v1/XyyqUpdate')  # 国内各省目前疫情
    print('正在获取国内风险地区...')
    requests.get('http://127.0.0.1:9000/covid_ksh/v1/FxdqUpdate')  # 国内风险地区
    print('正在获取近两月份的疫情趋势...')
    requests.get('http://127.0.0.1:9000/covid_ksh/v1/PastTwoMonthUpdate')

    nowtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('demo/data/UpdateTime.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps({
            'code': 200,
            '数据获取时间': nowtime
        }, ensure_ascii=False, indent=4))
    print('获取完毕数据已更新!')
    print('更新时间:' + nowtime)
