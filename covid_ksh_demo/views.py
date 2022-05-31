import json
import logging
import re
import time
import traceback
from datetime import datetime

from django.http import HttpResponse

from covid_ksh_demo.models import Ssrd
from covid_ksh_demo.visualization import *
from utils.pachong2 import get_res_json
from bs4 import BeautifulSoup

from django.shortcuts import render

# Create your views here.
from covid_ksh_demo.serializers import *
from rest_framework import mixins
from utils import auth, wrappers
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.views import APIView, Response
from django.db import transaction

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/100.0.4896.75 Safari/537.36'
}


def response_as_json(data):
    json_str = json.dumps(data)
    response = HttpResponse(
        json_str,
        content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response


def json_response(data, code=200):
    data = {
        "code": code,
        "msg": "success",
        "data": data,
    }
    return response_as_json(data)


class HistoryData(ModelViewSet):
    authentication_classes = []
    permission_classes = []
    serializer_class = CnCovidHistorySerializer
    pagination_class = auth.GeneralPagination
    queryset = models.Gnlssj.objects.all()


class HistoryDataUpdate(APIView):
    """
    提供接口：根据第三方接口数据，更新国内covid历史数据
    更新表：Gnlssj
    """

    def get(self, request, *args, **kwargs):
        logger.info("HistoryDataUpdate接口触发，更新gnlssj")
        start_timestamp = time.time()
        provinces = ['安徽', '上海', '澳门', '北京', '福建', '甘肃', '广东', '广西', '贵州', '海南',
                     '河北', '河南', '黑龙江', '湖北', '湖南', '吉林', '江苏', '江西', '辽宁', '内蒙古', '宁夏',
                     '青海', '山东', '山西', '陕西', '四川', '台湾', '天津', '西藏', '香港', '新疆', '云南', '浙江', '重庆']
        url = 'https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?province='
        datas = []
        objects_list = []
        try:
            for province in provinces:
                res = get_res_json(url + province, headers)  # res是json格式，ptyhon识别为str
                # output_file = os.path.join(dir, province + '.txt')
                datas += json.loads(res)['data']
            for data in datas:
                Gnlssj_obj = models.Gnlssj()
                Gnlssj_obj.year = data['year']
                Gnlssj_obj.date = data['date']
                Gnlssj_obj.country = data['country']
                Gnlssj_obj.province = data['province']
                Gnlssj_obj.confirm = data['confirm']
                Gnlssj_obj.dead = data['dead']
                Gnlssj_obj.heal = data['heal']
                Gnlssj_obj.confirm_add = data['confirm_add']
                Gnlssj_obj.confirm_cuts = data['confirm_cuts']
                Gnlssj_obj.dead_cuts = data['dead_cuts']
                Gnlssj_obj.now_confirm_cuts = data['now_confirm_cuts']
                Gnlssj_obj.heal_cuts = data['heal_cuts']
                Gnlssj_obj.newconfirm = data['newConfirm']
                Gnlssj_obj.newheal = data['newHeal']
                Gnlssj_obj.newdead = data['newDead']
                Gnlssj_obj.description = data['description']
                Gnlssj_obj.wzz = data['wzz']
                Gnlssj_obj.wzz_add = data['wzz_add']
                Gnlssj_obj.dateid = time.strftime('%F %H:%M:%S', time.localtime())
                # Gnlssj_obj.save()
                """过滤掉时间"""
                latest_GnlssjBAk_obj = models.GnlssjBAk.objects.order_by('-dateid').first()
                # latest_Gnlssj_obj = models.Gnlssj.objects.order_by('-dateid').first()
                latest_GnlssjBAk_obj_time = latest_GnlssjBAk_obj.dateid if latest_GnlssjBAk_obj else '2019-01-01 00:00:00'
                if datetime.strptime(str(Gnlssj_obj.year) + str(Gnlssj_obj.date), '%Y%m.%d') \
                        > datetime.strptime(latest_GnlssjBAk_obj_time, '%Y-%m-%d %H:%M:%S'):
                    objects_list.append(Gnlssj_obj)
                    logger.info("本次任务需要添加数据%s,%s-%s" % (Gnlssj_obj.province, Gnlssj_obj.year, Gnlssj_obj.date))
                else:
                    logger.info("已存在的数据%s,%s-%s，本次任务过滤" % (Gnlssj_obj.province, Gnlssj_obj.year, Gnlssj_obj.date))
            logger.info("开始批量保存数据。。。")
            models.Gnlssj.objects.bulk_create(objects_list)
            end_timestamp = time.time()
            logger.info("保存完毕，任务耗时%.3f秒" % (end_timestamp - start_timestamp))
            return Response({'ret': '更新数据任务成功',
                             'msg': ''})
        except Exception as e:
            raise e
            # return Response({'ret': '更新数据任务失败',
            #                  'msg': ''})


class YqToday(ModelViewSet):
    authentication_classes = []
    permission_classes = []
    serializer_class = YqTodaySerializer
    pagination_class = auth.GeneralPagination
    queryset = models.Bentuxianyou31.objects.all()


class YqTodayUpdate(APIView):
    """
      提供接口：根据第三方接口数据，更新本土现有数据
      更新表：Bentuxianyou31
      """

    def get(self, request, *args, **kwargs):
        logger.info("YqTodayUpdate接口触发，更新Bentuxianyou31")
        start_timestamp = time.time()
        url = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=statisGradeCityDetail,diseaseh5Shelf'
        datas_list = json.loads(get_res_json(url, headers)).get('data').get('statisGradeCityDetail')
        Bentuxianyou31_obj_list = []
        try:
            for data in datas_list:
                Bentuxianyou31_obj = models.Bentuxianyou31()
                Bentuxianyou31_obj.address = data['province'] + data['city']
                Bentuxianyou31_obj.addqz = data['confirmAdd']
                Bentuxianyou31_obj.xyqz = data['nowConfirm']
                Bentuxianyou31_obj.fxqy = data['grade']
                if not models.Bentuxianyou31.objects.filter(address=data['province'] + data['city'],
                                                            addqz=data['confirmAdd'],
                                                            xyqz=data['nowConfirm'],
                                                            fxqy=data['grade']):
                    logger.info("本次任务需要添加数据%s，%s" % (Bentuxianyou31_obj.address, data['date']))
                    Bentuxianyou31_obj_list.append(Bentuxianyou31_obj)
                    # Gnlssj_obj.save()
                else:
                    logger.info("過濾已存在的数据%s，%s" % (Bentuxianyou31_obj.address, data['date']))
            logger.info("开始批量保存数据。。。")
            models.Bentuxianyou31.objects.bulk_create(Bentuxianyou31_obj_list)
            end_timestamp = time.time()
            logger.info("保存完毕，任务耗时%.0f秒" % (end_timestamp - start_timestamp))
            return Response({'ret': '更新数据任务成功',
                             'msg': ''})
        except Exception as e:
            raise e


class YqEveryday(ModelViewSet):
    authentication_classes = []
    permission_classes = []
    serializer_class = YqEverydaySerializer
    pagination_class = auth.GeneralPagination
    queryset = models.Mrsj.objects.all()


class YqEverydayUpdate(APIView):
    """
      提供接口：根据第三方接口数据，更新國內每日数据
      更新表：Mrsj
      """

    def get(self, request, *args, **kwargs):
        logger.info("YqEverydayUpdate接口触发，更新Mrsj")
        start_timestamp = time.time()
        url = 'https://file1.dxycdn.com/2021/1228/171/2851867762198723253-135.json?t=27344362'
        datas_list = json.loads(get_res_json(url, headers)).get('data')
        Mrsj_obj_list = []
        try:
            for data in datas_list:
                Mrsj_obj = models.Mrsj()
                Mrsj_obj.confirmedcount = data['confirmedCount']
                Mrsj_obj.confirmedincr = data['confirmedIncr']
                Mrsj_obj.curedcount = data['curedCount']
                Mrsj_obj.curedincr = data['curedIncr']
                Mrsj_obj.currentconfirmedcount = data['currentConfirmedCount']
                Mrsj_obj.currentconfirmedincr = data['currentConfirmedIncr']
                Mrsj_obj.dateid = data['dateId']
                Mrsj_obj.deadcount = data['deadCount']
                Mrsj_obj.deadincr = data['deadIncr']
                Mrsj_obj.highdangercount = data['highDangerCount']
                Mrsj_obj.middangercount = data['midDangerCount']
                Mrsj_obj.suspectedcount = data['suspectedCount']
                Mrsj_obj.suspectedcountincr = data['suspectedCountIncr']
                if not models.Mrsj.objects.filter(dateid=data['dateId']):
                    logger.info("Mrsj更新任务需要添加%s日數據" % Mrsj_obj.dateid)
                    Mrsj_obj_list.append(Mrsj_obj)
                else:
                    logger.info("過濾Mrsj表已存在的%s日数据" % Mrsj_obj.dateid)
            logger.info("开始批量保存Mrsj数据。。。")
            models.Mrsj.objects.bulk_create(Mrsj_obj_list)
            end_timestamp = time.time()
            logger.info("保存完毕，任务耗时%.0f秒" % (end_timestamp - start_timestamp))
            return Response({'ret': '更新数据任务成功',
                             'msg': ''})
        except Exception as e:
            raise e


class SsrdUpdate(APIView):
    """
      提供接口：根据第三方接口数据，更新实时热点数据
      更新表：ssrd
      """

    @wrappers.run_time_wrapper("SsrdUpdate")
    def get(self, request, *args, **kwargs):
        logger.info("SsrdUpdate接口触发，更新ssrd")
        # start_timestamp = time.time()
        url = 'https://opendata.baidu.com/data/inner?tn=reserved_all_res_tn&dspName=iphone&from_sf=1&dsp=iphone&resource_id=28565&alr=1&query=%E5%9B%BD%E5%86%85%E6%96%B0%E5%9E%8B%E8%82%BA%E7%82%8E%E6%9C%80%E6%96%B0%E5%8A%A8%E6%80%81&cb=jsonp_1642854207390_27502'
        datas_list = json.loads(get_res_json(url, headers).split('(')[1][:-1])['Result'][0]['DisplayData']['result'][
            'items']
        Ssrd_obj_list = []
        try:
            for data in datas_list:
                Ssrd_obj = models.Ssrd()
                Ssrd_obj.eventdescription = data['eventDescription']
                Ssrd_obj.eventtime = time.strftime('%Y-%m-%d %H:%M:%d', time.localtime(float(data['eventTime'])))
                Ssrd_obj.eventurl = data['eventUrl']
                Ssrd_obj.homepageurl = data['homepageUrl']
                Ssrd_obj.item_avatar = data['item_avatar']
                Ssrd_obj.sitename = data['siteName']
                if not models.Ssrd.objects.filter(eventtime=Ssrd_obj.eventtime, sitename=data['siteName']):
                    logger.info("Ssrd更新任务需要添加%s的%s數據" % (Ssrd_obj.sitename, Ssrd_obj.eventtime))
                    Ssrd_obj_list.append(Ssrd_obj)
                else:
                    logger.info("過濾Ssrd表已存在%s的%s数据" % (Ssrd_obj.sitename, Ssrd_obj.eventtime))
            logger.info("开始批量保存Ssrd数据。。。")
            models.Ssrd.objects.bulk_create(Ssrd_obj_list)
            # end_timestamp = time.time()
            # logger.info("保存完毕，任务耗时%.0f秒" % (end_timestamp - start_timestamp))
            return Response({'ret': '更新数据任务成功',
                             'msg': ''})
        except Exception as e:
            logging.error("Main program error:")
            logging.error(e)
            logging.error(traceback.format_exc())
            return Response({'ret': '更新数据任务失败',
                             'msg': '未知异常'})


class XyyqUpdate(APIView):
    """
      提供接口：根据第三方接口数据，更新国内各省目前疫情
      更新表：xyyq
      """

    @wrappers.run_time_wrapper("XyyqUpdate")
    def get(self, request, *args, **kwargs):
        logger.info("XyyqUpdate接口触发，更新xyyq")
        url = 'https://ncov.dxy.cn/ncovh5/view/pneumonia'
        res_file = get_res_json(url, headers)
        res = BeautifulSoup(res_file, 'html.parser')  # 利用bs4解析数据
        res = res.find('script', {'id': 'getAreaStat'}).text  # 利用bs4获取国内的数据
        res = re.findall(r'try \{ window.getAreaStat = (.*)}catch', res, re.S)[0]  # 利用正则表达式先取得里面的所有数据
        res = re.findall(r'\{(.*?)]}', res)  # 利用正则表达式再去取每个省的数据
        Xyyq_obj_list = []
        try:
            for data in res:
                provinceName = re.findall('"provinceName":"(.*?)"', data)  # 取省份名
                cityName = re.findall('"cityName":"(.*?)"', data)  # 取城市名
                if len(cityName) == 0:  # 判断城市的长度是否为0
                    cityName = provinceName  # 为零则把城市 = 省份 方便后面的保存
                else:
                    cityName.insert(0, provinceName[0])  # 在城市列表最开始的位置插入省份名
                currentConfirmedCount = re.findall('"currentConfirmedCount":(.*?),', data)  # 取现有确诊
                confirmedCount = re.findall('"confirmedCount":(.*?),', data)  # 去取累计确诊
                curedCount = re.findall('"curedCount":(.*?),', data)  # 取累计治愈
                deadCount = re.findall('"deadCount":(.*?),', data)  # 取累计死亡
                for i in range(0, len(currentConfirmedCount)):  # 遍历存到列表t
                    Xyyq_obj = models.Xyyq()
                    Xyyq_obj.provincename = cityName[0]
                    Xyyq_obj.cityname = cityName[i]
                    Xyyq_obj.currentconfirmedcount = currentConfirmedCount[i]
                    Xyyq_obj.confirmedcount = confirmedCount[i]
                    Xyyq_obj.curedcount = curedCount[i]
                    Xyyq_obj.deadcount = deadCount[i]
                    logger.info("Xyyq更新任务需要添加%s，%s的數據" % (Xyyq_obj.provincename, Xyyq_obj.cityname))
                    Xyyq_obj_list.append(Xyyq_obj)
            logger.info("开始批量保存Xyyq数据。。。")
            with transaction.atomic():
                models.Xyyq.objects.raw("truncate table xyyq")
                models.Xyyq.objects.bulk_create(Xyyq_obj_list)
            return Response({'ret': '更新数据任务成功',
                             'msg': ''})
        except Exception as e:
            logging.error(e)
            logging.error(traceback.format_exc())
            return Response({'ret': '更新数据任务失败',
                             'msg': '未知异常'})


class FxdqUpdate(APIView):
    """
      提供接口：根据第三方接口数据，更新国内各省目前疫情
      更新表：fxdq
      """

    @wrappers.run_time_wrapper("FxdqUpdate")
    def get(self, request, *args, **kwargs):
        logger.info("FxdqUpdate接口触发，更新fxdq")
        url = 'https://file1.dxycdn.com/2021/0202/196/1680100273140422643-135.json'
        resdata = json.loads(get_res_json(url, headers)).get('data')
        fxdq_obj_list = []
        try:
            for items in resdata:
                for dangerPros in items['dangerPros']:
                    for dangerAreas in dangerPros['dangerAreas']:
                        fxdq_obj = models.Fxdq()
                        fxdq_obj.dangerlevel = items['dangerLevel']
                        fxdq_obj.provinceid = dangerPros['provinceId']
                        fxdq_obj.provincename = dangerPros['provinceName']
                        fxdq_obj.cityname = dangerAreas['cityName']
                        fxdq_obj.areaname = dangerAreas['areaName']
                        fxdq_obj_list.append(fxdq_obj)
                        logger.info("Fxdq更新任务需要添加%s，%s的數據" % (fxdq_obj.provincename, fxdq_obj.cityname))
            logger.info("开始批量保存Fxdq数据。。。")
            with transaction.atomic():
                models.Fxdq.objects.raw("truncate table fxdq")
                models.Fxdq.objects.bulk_create(fxdq_obj_list)
            return Response({'ret': '更新数据任务成功',
                             'msg': ''})
        except Exception as e:
            logging.error(e)
            logging.error(traceback.format_exc())
            return Response({'ret': '更新数据任务失败',
                             'msg': '未知异常'})


class PastTwoMonthUpdate(APIView):
    """
      提供接口：根据第三方接口数据，更新近2个月新增情况,近2个月累计情况
      更新表：j2yxz,j2ylj
      """

    @wrappers.run_time_wrapper("PastTwoMonthUpdate")
    def get(self, request, *args, **kwargs):
        logger.info("PastTwoMonthUpdate接口触发，更新j2yxz,j2ylj")
        url = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList,chinaDayAddList,nowConfirmStatis,provinceCompare'
        resdata = json.loads(get_res_json(url, headers)).get('data')
        j2yxz_obj_list = []
        j2ylj_obj_list = []
        try:
            for chinaDayAddList in resdata['chinaDayAddList']:
                j2yxz_obj = models.J2Yxz()
                j2yxz_obj.dead = chinaDayAddList.get('dead')
                j2yxz_obj.heal = chinaDayAddList.get('heal')
                j2yxz_obj.importedcase = chinaDayAddList.get('importedCase')
                j2yxz_obj.infect = chinaDayAddList.get('infect')
                j2yxz_obj.localinfectionadd = chinaDayAddList.get('localinfectionadd')
                j2yxz_obj.localconfirmadd = chinaDayAddList.get('localConfirmadd')
                j2yxz_obj.suspect = chinaDayAddList.get('suspect')
                j2yxz_obj.deadrate = chinaDayAddList.get('deadRate')
                j2yxz_obj.healrate = chinaDayAddList.get('healRate')
                j2yxz_obj.date = chinaDayAddList.get('date')
                j2yxz_obj.y = chinaDayAddList.get('y')
                j2yxz_obj.confirm = chinaDayAddList.get('confirm')
                j2yxz_obj.dateid = chinaDayAddList.get('y') + '.' + chinaDayAddList.get('date')
                if not models.J2Yxz.objects.filter(dateid=j2yxz_obj.dateid):
                    logger.info("J2Yxz更新任务需要添加 %s 數據" % j2yxz_obj.dateid)
                    j2yxz_obj_list.append(j2yxz_obj)
                logger.info("J2Yxz已存在 %s 數據，本次过滤" % j2yxz_obj.dateid)
            for chinaDayList in resdata['chinaDayList']:
                j2ylj_obj = models.J2Ylj()
                j2ylj_obj.confirm = chinaDayList.get('confirm')
                j2ylj_obj.nowconfirm = chinaDayList.get('nowConfirm')
                j2ylj_obj.nowsevere = chinaDayList.get('nowSevere')
                j2ylj_obj.noinfecth5 = chinaDayList.get('noInfectH5')
                j2ylj_obj.local_acc_confirm = chinaDayList.get('local_acc_confirm')
                j2ylj_obj.dead = chinaDayList.get('dead')
                j2ylj_obj.healrate = chinaDayList.get('healRate')
                j2ylj_obj.deadrate = chinaDayList.get('deadRate')
                j2ylj_obj.localconfirm = chinaDayList.get('localConfirm')
                j2ylj_obj.suspect = chinaDayList.get('suspect')
                j2ylj_obj.heal = chinaDayList.get('heal')
                j2ylj_obj.importedcase = chinaDayList.get('importedCase')
                j2ylj_obj.date = chinaDayList.get('date')
                j2ylj_obj.y = chinaDayList.get('y')
                j2ylj_obj.noinfect = chinaDayList.get('noInfect')
                j2ylj_obj.localconfirmh5 = chinaDayList.get('localConfirmH5')
                j2ylj_obj.dateid = chinaDayList.get('y') + '.' + chinaDayList.get('date')
                if not models.J2Ylj.objects.filter(dateid=j2ylj_obj.dateid):
                    logger.info("J2Ylj更新任务需要添加 %s 數據" % j2ylj_obj.dateid)
                    j2ylj_obj_list.append(j2ylj_obj)
                logger.info("J2Ylj已存在 %s 數據，本次过滤" % j2ylj_obj.dateid)
            logger.info("开始批量保存近2个月新增和累计数据。。。")
            models.J2Yxz.objects.bulk_create(j2yxz_obj_list)
            models.J2Ylj.objects.bulk_create(j2ylj_obj_list)
            return Response({'ret': '更新数据任务成功',
                             'msg': ''})
        except Exception as e:
            logging.error(e)
            logging.error(traceback.format_exc())
            return Response({'ret': '更新数据任务失败',
                             'msg': '未知异常'})


####################################################################
# 全国疫情
class qgyq(APIView):
    def get(self, request, *args, **kwargs):
        return json_response(json.loads(xyqz()))


# 中国疫情地图
class Zgdt(APIView):
    def get(self, request, *args, **kwargs):
        return json_response(json.loads(zgdt()))


# 中国疫情地图
class Yqbt(APIView):
    def get(self, request, *args, **kwargs):
        return json_response(json.loads(yqbt()))


# 近期31省区市本土现有病例
class Bg(APIView):
    def get(self, request, *args, **kwargs):
        return json_response(json.loads(bg()))


# 高风险地区
class gfx1(APIView):
    def get(self, request, *args, **kwargs):
        return json_response(json.loads(gfx('高风险')))


# 中风险地区
class zfx1(APIView):
    def get(self, request, *args, **kwargs):
        return json_response(json.loads(gfx('中风险')))


# 风险地区
class fxdq1(APIView):
    def get(self, request, *args, **kwargs):
        with open('covid_ksh_demo/data/风险地区.json', 'r', encoding='utf-8') as f:
            data = f.read()
        return json_response(json.loads(data))


# 中国疫情
class chinayq1(APIView):
    def get(self, request, *args, **kwargs):
        with open('covid_ksh_demo/data/中国疫情.json', 'r', encoding='utf-8') as f:
            data = f.read()
        return json_response(json.loads(data))


# 实时热点
class ssrd1(APIView):
    def get(self, request, *args, **kwargs):
        ssrd = Ssrd.objects.all()
        serializer = ReDianSerializer(ssrd, many=True)
        return json_response(serializer.data)


# 主页
class IndexView(APIView):
    def get(self, request, *args, **kwargs):
        return HttpResponse(content=open("./templates/index.html", 'rb').read())

