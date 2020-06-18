# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WenshuScItem(scrapy.Item):
    # define the fields for your item here like:
    wid = scrapy.Field()  # 文书id
    sdate = scrapy.Field()  # 审结时间
    procedure = scrapy.Field()  # 审理程序
    status = scrapy.Field()  # 案件状态
    causecode = scrapy.Field()  # 案由编号
    causename = scrapy.Field()  # 案由
    result = scrapy.Field()  # 结果
    judgeresult = scrapy.Field()  # 判决结果
    yiju = scrapy.Field()  # 依据
    caf = scrapy.Field()  # 案件受理费
    mid = scrapy.Field()  # mid
    updated = scrapy.Field()  # 修改日期
    wslx = scrapy.Field()  # 文书类型
    postTime = scrapy.Field()  # 发布时间
    court = scrapy.Field()  # 法院
    judge = scrapy.Field()  # 审判人员
    sortTime = scrapy.Field()  # 裁判日期
    caseType = scrapy.Field()  # 案件类型
    caseNo = scrapy.Field()  # 案号
    title = scrapy.Field()  # 标题
    body = scrapy.Field()  # 正文
    detailUrl = scrapy.Field()  # 详情url
    crawlTime = scrapy.Field()  # 采集时间
    provinces = scrapy.Field()  # 省份
    MD5 = scrapy.Field()  # md5码
    source = scrapy.Field()  # 来源
    plaintiff = scrapy.Field()  # 原告
    deffendant = scrapy.Field()  # 被告
