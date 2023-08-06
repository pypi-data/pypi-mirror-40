# stock_grpc

stock_grpc目前包含的功能主要有：

 实现股票关键信息RPC查询功能

## 服务端安装方式
    cd sense_data_service/
    nohup python server.py &

## 客户端安装方式
    pip install sense-data

## 将settings.ini放到用户的根目录（cd ~）

## 客户端使用指南
    from sense_data import *

## 使用方法，初始化一个实例，如何调用方法，以字符串的形式输入股票或公司代码

    sen = SenseDataService()

    ## 输入公司代码，得到公司的别名，输出形式为别名形成的列表
    sen.get_company_alias(company_code)

    ## 输入公司代码，输出懂事和监事的信息，每个人的数据形式是对象，然后将对象存入列表中
    sen.get_chairman_supervisor(company_code)

    ## 输入公司代码，输出股东信息，每个股东的数据形式是对象，然后将对象存入列表中
    sen.get_stockholder(company_code)

    ## 输入公司代码，输出子公司信息，每个子公司的数据形式是对象，然后将对象存入列表中
    sen.get_subcompany(company_code)

    ## 输入股票代码，输出最新一天的实时股票数据，数据形式是对象
    sen.get_stock_price_tick(stock_code)

    ## 输入股票代码，输出该股票历史信息
    sen.get_stock_price_day(*args)
    有三种查询方式，sen.get_stock_price_day('000020')，输出有史以来的所有数据，数据形式为对象列表；
    sen.get_stock_price_day('000020', '2018-12-2')，输出指定某一天的数据，数据形式为对象；
    sen.get_stock_price_day('000020', '2018-12-2', '2019-1-4')，输出指定时间段的数据，数据形式为对象列表；

    ## 输入股票代码，输出公司基础信息，数据形式为对象（字典）
    sen.get_company_info(stock_code)

    ## 输入股票代码，输出对应的行业概念信息，数据形式为对象（字典）
    sen.get_industry_concept(stock_code)








