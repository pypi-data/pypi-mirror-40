"""
企查查的爬虫
"""
import os
import re
import time
import json
import requests
from lxml import etree
from tqdm import tqdm
import pymongo
import wcc
import random
import jsonfiler
import pmt
from bs4 import BeautifulSoup
import traceback
import comcom


def get_gsinfo(url):
    """
    如果url是gs_，则在这个方法中处理
    页面元素参考 https://www.qichacha.com/gs_1473977081543754269
    """
    global HEADERS
    try:
        resp_text = wcc.getpage_qichacha(url,timeout=50,max_try=30)
        if resp_text is None:
            return None
    except Exception as err:
        return None
    try:
        html = etree.HTML(resp_text)
        item = {}
        # 公司名
        if html.xpath('//span[@class="clear"]/span[1]//text()'):
            item['name'] = html.xpath('//span[@class="clear"]/span[1]//text()')[0]
        else:
            item['name'] = ""
        # 统一社会信用代码 
        # 用code代表信用代码
        if html.xpath('//ul[@class="company-base"]//li/label[contains(text(), "统一社会信用代码")]/..//text()'):
            item['code'] = html.xpath('//ul[@class="company-base"]//li/label[contains(text(), "统一社会信用代码")]/..//text()')[1]
        else:
            item['code'] = ""
        # 注册号
        # 有的公司,"统一社会信用代码"和"注册号"可以同时存在.参考 https://www.qichacha.com/gs_1478515181544192110
        if html.xpath('//ul[@class="company-base"]//li/label[contains(text(), "注册号")]/..//text()'):
            item['code_reg'] = html.xpath('//ul[@class="company-base"]//li/label[contains(text(), "注册号")]/..//text()')[1]
        else:
            item['code_reg'] = ""

        # 经营状态
        if html.xpath('//ul[@class="company-base"]//li/label[contains(text(), "经营状态")]/..//text()'):
            item['status'] = html.xpath('//ul[@class="company-base"]//li/label[contains(text(), "经营状态")]/..//text()')[1]
        else:
            item['status'] = ""
        # 公司类型
        if html.xpath('//ul[@class="company-base"]//li/label[contains(text(), "公司类型")]/..//text()'):
            item['type'] = html.xpath('//ul[@class="company-base"]//li/label[contains(text(), "公司类型")]/..//text()')[1]
        else:
            item['type'] = ""
        # 成立日期
        if html.xpath('//ul[@class="company-base"]//li/label[contains(text(), "成立日期")]/..//text()'):
            item['date_est'] = html.xpath('//ul[@class="company-base"]//li/label[contains(text(), "成立日期")]/..//text()')[1]
        else:
            item['date_est'] = ""
        # 法定代表人, 需要修改字段名
        if html.xpath('//ul[@class="company-base"]//li/label[contains(text(), "法定代表")]/..//text()'):
            legalp = html.xpath('//ul[@class="company-base"]//li/label[contains(text(), "法定代表")]/..//text()')[2]
        else:
            legalp = ""
        item['legalp'] = legalp.strip() if legalp else ""
        # 注册资本
        if html.xpath('//ul[@class="company-base"]//li/label[contains(text(), "注册资本")]/..//text()'):
            item['capital_reg'] = html.xpath('//ul[@class="company-base"]//li/label[contains(text(), "注册资本")]/..//text()')[1]
        else:
            item['capital_reg'] = ""
        # 营业期限
        if html.xpath('//ul[@class="company-base"]//li/label[contains(text(), "营业期限")]/..//text()'):
            item['validity'] = html.xpath('//ul[@class="company-base"]//li/label[contains(text(), "营业期限")]/..//text()')[1]
        else:
            item['validity'] = ""
        # 登记机关
        if html.xpath('//ul[@class="company-base"]//li/label[contains(text(), "登记机关")]/..//text()'):
            item['issuer'] = html.xpath('//ul[@class="company-base"]//li/label[contains(text(), "登记机关")]/..//text()')[1]
        else:
            item['issuer'] = ""
        # 发照日期
        if html.xpath('//ul[@class="company-base"]//li/label[contains(text(), "发照日期")]/..//text()'):
            item['date_aprv'] = html.xpath('//ul[@class="company-base"]//li/label[contains(text(), "发照日期")]/..//text()')[1]
        else:
            item['date_aprv'] = ""
        # 企业地址
        if html.xpath('//ul[@class="company-base"]//li/label[contains(text(), "企业地址")]/..//text()'):
            item['addr'] = html.xpath('//ul[@class="company-base"]//li/label[contains(text(), "企业地址")]/..//text()')[2]
        else:
            item['addr'] = ""
        # 经营范围
        if html.xpath('//ul[@class="company-base"]//li/label[contains(text(), "经营范围")]/..//text()'):
            scope = html.xpath('//ul[@class="company-base"]//li/label[contains(text(), "经营范围")]/..//text()')[2]
        else:
            scope = ""
        item['tel'] = ""
        item['bank'] = ""
        item['account'] = ""
        item['scope'] = scope.strip() if scope else ""
        # 信息来源
        item['from'] = '企查查gs'
        # 获取信息的时间
        item['ctime'] = int(time.time())
        # 信源的url
        item['url'] = url
        # 信源页面快照
        url_part = url.replace("https://www.qichacha.com/","").replace(".html","")
        item['html'] = wcc.uploadHtml(resp_text,url=url_part)
        return item
    except Exception as err:
        print(traceback.format_exc())
        print(url+" err "+str(err))
        return None

def get_firminfo(url):
    """
    从url获取对应的信息，url可以参考：https://www.qichacha.com/firm_8c9f7ddc1a7bcee3d1f7676773fe9404.html
    """
    global HEADERS
    
    if "firm_CN_" in url:url.replace("firm_CN_", "cbase_")
    if "cbase_CN_" in url:url.replace("cbase_CN_", "cbase_")
    url = url.replace("firm_", "cbase_")
    try:
        resp_text = wcc.getpage_qichacha(url,max_try=30)
        if resp_text is None:
            return None
    except Exception as err:
        return None
    try:
        html = etree.HTML(resp_text)
        soup = BeautifulSoup(resp_text,"html.parser")
        item = {}
        # 公司名,firm页面的公司名确实不同的网页有不同的写法
        """
        https://www.qichacha.com/firm_d5a788511649fbf2e472c05d48d5be5f.html#base
        便是 <div class="row title jk-tip">
                <h1>固原地震台招待所</h1> 
        """

        """
        https://www.qichacha.com/firm_44a28adbedaf8245d0d3043fcf295ee9.html#base
        <div class="content"> 
            <div class="row title" style="margin-top: -2px;margin-bottom: 10px;">贺兰县富兴南街风格秀服装店
        """
        com_name_xpath1 = '//div[@class="content"]/div[@class="row title jk-tip"]/h1/text()'
        com_name_xpath2 = '//div[@class="content"]/div[@class="row title"]/text()'
        if html.xpath(com_name_xpath1):
            com_name = html.xpath(com_name_xpath1)[0]
        elif html.xpath(com_name_xpath2):
            com_name = html.xpath(com_name_xpath2)[0]
        else:
            com_name = ""
        if com_name == "":
            raise Exception(url+" html match no com name")
        item["name"] = com_name
       
        # 公司名
        item["legalp"] = soup.select(".seo")[0].text
        #######################     上面部分信息      ##############################
        # 官网
        if html.xpath('//div[@class="content"]/div[@class="row"]//span[contains(text(), "官网")]/following-sibling::*[1]//a/@href'):
            item['site'] = html.xpath('//div[@class="content"]/div[@class="row"]//span[contains(text(), "官网")]/following-sibling::*[1]//a/@href')[0].strip()
        elif html.xpath('//div[@class="content"]/div[@class="row"]//span[contains(text(), "官网")]/following-sibling::*[1]//text()'):
            item['site'] = html.xpath('//div[@class="content"]/div[@class="row"]//span[contains(text(), "官网")]/following-sibling::*[1]//text()')[0].strip()
        else:
            item['site'] = ''
        # 邮箱
        if html.xpath('//div[@class="content"]/div[@class="row"]//span[contains(text(), "邮箱")]/following-sibling::*[1]//a//text()'):
            item['email'] = html.xpath('//div[@class="content"]/div[@class="row"]//span[contains(text(), "邮箱")]/following-sibling::*[1]//a//text()')[0].strip()
        else:
            item['email'] = ''
        # 简介
        if html.xpath('//div[@class="content"]/div[@class="row"]//span[contains(text(), "简介")]/following-sibling::*[1]//text()'):
            item['intro'] = html.xpath('//div[@class="content"]/div[@class="row"]//span[contains(text(), "简介")]/following-sibling::*[1]//text()')[0].strip()
        else:
            item['intro'] = ""
        #######################     上面部分信息      ##############################

        #######################     下面部分信息      ##############################
        # 注册资本
        if html.xpath('//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "注册资本")]/following-sibling::*[1]//text()'):
            item['capital_reg'] = html.xpath('//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "注册资本")]/following-sibling::*[1]//text()')[0].strip()
        else:
            item['capital_reg'] = ""
        # 实缴资本
        if html.xpath('//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "实缴资本")]/following-sibling::*[1]//text()'):
            item['capital_paid'] = html.xpath(
                '//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "实缴资本")]/following-sibling::*[1]//text()')[0].strip()
        else:
            item['capital_paid'] = ""
        # 经营状态
        if html.xpath('//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "经营状态")]/following-sibling::*[1]//text()'):
            item['status'] = html.xpath('//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "经营状态")]/following-sibling::*[1]//text()')[0].strip()
        else:
            item['status'] = ""
        # 成立日期
        if html.xpath('//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "成立日期")]/following-sibling::*[1]//text()'):
            item['date_est'] = html.xpath('//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "成立日期")]/following-sibling::*[1]//text()')[0].strip()
        else:
            item['date_est'] = ""
        # 统一社会信用代码
        if html.xpath('//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "统一社会信用代码")]/following-sibling::*[1]//text()'):
            item['code'] = html.xpath(
                '//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "统一社会信用代码")]/following-sibling::*[1]//text()')[0].strip()
        else:
            item['code'] = ""
        # 纳税人识别号
        if html.xpath('//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "纳税人识别号")]/following-sibling::*[1]//text()'):
            item['code_tax'] = html.xpath(
                '//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "纳税人识别号")]/following-sibling::*[1]//text()')[0].strip()
        else:
            item['code_tax'] = ""
        # 注册号
        if html.xpath('//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "注册号")]/following-sibling::*[1]//text()'):
            item['code_reg'] = html.xpath(
                '//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "注册号")]/following-sibling::*[1]//text()')[0].strip()
        else:
            item['code_reg'] = ""
        # 组织机构代码
        if html.xpath('//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "组织机构代码")]/following-sibling::*[1]//text()'):
            item['code_org'] = html.xpath(
                '//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "组织机构代码")]/following-sibling::*[1]//text()')[0].strip()
        else:
            item['code_org'] = ""
        # 公司类型
        if html.xpath('//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "公司类型")]/following-sibling::*[1]//text()'):
            item['type'] = html.xpath(
                '//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "公司类型")]/following-sibling::*[1]//text()')[0].strip()
        else:
            item['type'] = ""
        # 所属行业
        if html.xpath('//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "所属行业")]/following-sibling::*[1]//text()'):
            item['industry'] = html.xpath(
                '//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "所属行业")]/following-sibling::*[1]//text()')[0].strip()
        else:
            item['industry'] = ""
        # 核准日期
        if html.xpath('//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "核准日期")]/following-sibling::*[1]//text()'):
            item['date_aprv'] = html.xpath(
                '//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "核准日期")]/following-sibling::*[1]//text()')[0].strip()
        else:
            item['date_aprv'] = ""
        # 登记机关
        if html.xpath('//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "登记机关")]/following-sibling::*[1]//text()'):
            item['issuer'] = html.xpath(
                '//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "登记机关")]/following-sibling::*[1]//text()')[0].strip()
        else:
            item['issuer'] = ""
        # 所属地区
        if html.xpath('//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "所属地区")]/following-sibling::*[1]//text()'):
            item['district'] = html.xpath(
                '//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "所属地区")]/following-sibling::*[1]//text()')[0].strip()
        else:
            item['district'] = ""
        # 英文名
        if html.xpath('//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "英文名")]/following-sibling::*[1]//text()'):
            item['name_en'] = html.xpath(
                '//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "英文名")]/following-sibling::*[1]//text()')[0].strip()
        else:
            item['name_en'] = ""
        # 曾用名
        if html.xpath('//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "曾用名")]/following-sibling::*[1]//span/text()'):
            name_used = html.xpath(
                '//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "曾用名")]/following-sibling::*[1]//span/text()')
        else:
            name_used = ""
        item['name_used'] = ""
        for i in name_used:
            item['name_used'] += i.strip()
        # 参保人数
        if html.xpath('//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "参保人数")]/following-sibling::*[1]//text()'):
            item['cbrs'] = html.xpath(
                '//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "参保人数")]/following-sibling::*[1]//text()')[0].strip()
        else:
            item['cbrs'] = ""
        # 人员规模
        if html.xpath('//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "人员规模")]/following-sibling::*[1]//text()'):
            item['staff'] = html.xpath(
                '//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "人员规模")]/following-sibling::*[1]//text()')[0].strip()
        else:
            item['staff'] = ""
        # 营业期限
        if html.xpath('//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "营业期限")]/following-sibling::*[1]//text()'):
            item['validity'] = html.xpath('//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "营业期限")]/following-sibling::*[1]//text()')[0].strip().replace(" ", "")
        else:
            item['validity'] = ""
        # 企业地址
        if html.xpath('//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "企业地址")]/following-sibling::*[1]//text()'):
            item['addr'] = html.xpath(
                '//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "企业地址")]/following-sibling::*[1]//text()')[0].strip()
        else:
            item['addr'] = ""
        # 经营范围
        if html.xpath('//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "经营范围")]/following-sibling::*[1]//text()'):
            item['scope'] = html.xpath(
                '//section[@id="Cominfo"]//table[@class="ntable"]//td[contains(text(), "经营范围")]/following-sibling::*[1]//text()')[0].strip()
        else:
            item['scope'] = ""

        #######################     右下角的信息      ##############################
        firm = str(re.findall("cbase_(.*?).html", url)[0])
        api_url = 'https://www.qichacha.com/tax_view?keyno=' + firm + '&ajaxflag=1'
        data = None
        try:
            data_text = wcc.getpage_qichacha(api_url,max_try=50,timeout=30)
            data_json = json.loads(data_text)
            data = data_json['data']
        except Exception as err:
            print(traceback.format_exc())
            print(err)
            date = None
        if data:
            # 电话
            if 'PhoneNumber' in data:
                item['tel'] = data['PhoneNumber']
            else:
                item['tel'] = ""
            # 开户银行
            if 'Bank' in data:
                item['bank'] = data['Bank']
            else:
                item['bank'] = ""
            # 银行账户
            if 'Bankaccount' in data:
                item['account'] = data['Bankaccount']
            else:
                item['account'] = ""
        else:
            item['tel'] = ""
            item['bank'] = ""
            item['account'] = ""
        if 'tel' not in item:
            item['tel'] = ""
        elif not item['tel']:
            item['tel'] = ""
        if 'bank' not in item:
            item['bank'] = ""
        elif not item['bank']:
            item['bank'] = ""
        if 'account' not in item:
            item['account'] = ""
        elif not item['account']:
            item['account'] = ""
        # 信息来源
        item['from'] = '企查查cbase'
        # 获取信息的时间
        item['ctime'] = int(time.time())
        # 信源的url
        item['url'] = url
        # 信源页面快照
        url_part = url.replace("https://www.qichacha.com/","").replace(".html","").replace(".shtml","")
        item['html'] = wcc.uploadHtml(resp_text,url=url_part)
        return item
    except Exception as err:
        print(traceback.format_exc())
        print(url+" err "+str(err))
        return None



def thread_main(thread_id, thread_jobs, thread_params, thread_results):
    """
    获取数据库连接
    """
    env_dict = os.environ
    try:
        mongo_data_uri = env_dict["MONGO_DAT_URI"]
        client = pymongo.MongoClient(mongo_data_uri)
        db = client["comdb"]
        col_combasic = db["combasic"]
        col_firmurls = db["firmurls"]
    except Exception as err:
        print(err)
        return None
    loop_count = thread_params["loop_count"]
    for loopc in range(loop_count+1):
        try:
            """
            爬取一个url对应的具体信息
            :param url: 需要爬取信息的url
                        例如:   https://www.qichacha.com/firm_b698f85595deef3e0ee2517790eccc7b.html
                        或：    https://www.qichacha.com/gs_1473975991543754066
            :return item: 爬取到的信息
            """
            cur_time = int(time.time())
            dbrow = col_firmurls.find_one_and_update({"ut":None}, {"$set":{"ut":cur_time}})
            if not dbrow:
                print("found none urls")
                break
            url = dbrow["url"]
            if ".shtml" in url:
                url = url.replace(".shtml",".html")
            
            cbase_url = url.replace("firm_","cbase_")
            if col_combasic.find_one({"url":cbase_url}):
                print("t"+str(thread_id)+" "+cbase_url+" skip")
                continue
            item = None
            if re.findall("https://www.qichacha.com/gs_", url):
                item = get_gsinfo(url)
            elif "firm_CN_" in url:
                firm_url = url.replace("firm_CN_","firm_")
                item = get_firminfo(firm_url)
            elif "firm_" in url:
                cbase_url = url.replace("firm_","cbase_")
                item = get_firminfo(cbase_url)
            elif "tax_view" in url:
                print("t"+str(thread_id)+" "+url+" ignore ")
                continue
            else:
                print("t"+str(thread_id)+" "+url+" bad ")
                continue 


            if item:
                if comcom.is_combasic(item):
                    thread_results["done_urls"].append(url)
                    thread_results["combasic"].append(item)
                    addinfo = comcom.add_combasic([item])
                    print("t"+str(thread_id)+" "+url+" ok "+str(addinfo))
                else:
                    print("t"+str(thread_id)+" "+url+" badformat")
            else:
                thread_results["error_urls"].append(url)
                print("t"+str(thread_id)+" "+url+" error")
        except Exception as err:
            thread_results["error_urls"].append(url)
            print(traceback.format_exc())
            print(err)
            continue

def wcc_qcc_combasic(THREAD_N):
    thread_params = {"loop_count":1000}
    thread_results={"combasic":[],"error_urls":[],"done_urls":[]}
    thread_jobs = [x for x in range(THREAD_N)]
    thread_results = pmt.domt(
        thread_main, 
        THREAD_N, 
        thread_jobs,
        thread_params,
        thread_results
    )
    #done_urls.extend(thread_results["done_urls"]) 
    #error_urls.extend(thread_results["error_urls"])
    #combasic_list = thread_results["combasic"]
    print("over") 

if __name__ == "__main__":
    wcc_qcc_combasic(1)
