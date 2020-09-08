import requests
import random
from lxml import etree
import csv

headers =[
            {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like G"},
            {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; ) "
                           "AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12"},
            {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; "
                           "WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727;"
                           " .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E"},
            {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) "
                           "AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"},
            {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) "
                           "AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"}]


class University_SX():
    def __init__(self):
        self.url =  "https://baike.baidu.com/item/{}"
        self.list = ["山西大学",'山西农业大学', '山西师范大学', '晋中学院',
                     '忻州师范学院', '吕梁学院', '山西传媒学院',
                     '太原科技大学', '山西医科大学', '太原师范学院',
                     '长治学院', '山西财经大学', '太原学院', '山西警察学院',
                     '中北大学', '山西大同大学', '长治医学院', '运城学院',
                     '山西中医药大学', '山西工商学院', '太原工业学院']

    #获取数据
    def get_data(self,university_name):
        self.data = requests.get(self.url.format(university_name), headers=headers[random.randint(0, len(headers) - 1)]).content.decode()

    #处理数据
    def parse_data(self):
        s1 = etree.HTML(self.data)

        university_list = s1.xpath('//dd[@class="basicInfo-item value"]')
        university_trace = s1.xpath('//dt[@class="basicInfo-item name"]')

        lis1 = ["中文名", "所在地址", "创办时间", "办学性质", "学校类别", "学校特色", "主管部门", "本科专业", "院系设置", "学校简介"]
        self.lis2 = []
        for i in range(0, len(university_trace)):
            university_trace[i] = university_trace[i].text.strip()
            
        #基本信息数据获取
        for i in lis1:
            if i in university_trace:

                i_index = university_trace.index(i)
                lis3 = s1.xpath('//dl[@class="basicInfo-block basicInfo-left"]/dt[@class="basicInfo-item name"]/text()')

                if university_trace[i_index] in lis3:
                    i_list = s1.xpath(
                        '//dl[@class="basicInfo-block basicInfo-left"]/dd[{}]/a[@target="_blank"]/text()'.format(
                            i_index + 1))
                else:
                    i_list = s1.xpath(
                        '//dl[@class="basicInfo-block basicInfo-right"]/dd[{}]/a[@target="_blank"]/text()'.format(
                            i_index + 1))

                if i_list == []:
                    self.lis2.append((i, university_list[university_trace.index(i)].text.strip()))
                else:
                    data = "、".join(i_list)
                    self.lis2.append((i, university_list[i_index].text.strip() + data))

        s = s1.xpath('//div[@class="lemma-summary"]/div')

        #获取简介数据
        account = ""
        for i in range(0, len(s)):
            data = s[i].xpath('string(.)').strip()
            account += data
        account = "".join(account.split())
        self.lis2.append(("学校简介", account))

    def running(self):
        for i in self.list:
            self.get_data(i)
            self.parse_data()
            self.lis2[0] = (self.lis2[0][1],"")
            with open('./ceshi.csv', 'a', newline='') as f:
                cw = csv.writer(f)
                cw.writerows(self.lis2)

if __name__ == "__main__":
    University_SX().running()
