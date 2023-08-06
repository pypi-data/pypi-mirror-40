# stock_grpc

stock_grpc目前包含的功能主要有：

 实现股票关键信息RPC查询功能

## 服务端安装方式
    cd stock_service/
    nohup python server.py &

## 客户端安装方式
    python setup.py install

## 客户端使用指南
    from sense_data import *

## 以字符串的形式输入股票或公司代码

    get_company_alias(company_code)

    get_chairman_supervisor(company_code)

    get_stockholder(company_code)

    get_subcompany(company_code)

    get_stock_price_tick(redis_code)

    get_stock_price_day(sql_code)

    get_company_info(sql_code)

    get_industry_concept(sql_code)

## 比如

    get_basic_data('000001')








