'''
从tushare中下载常用指数的日线数据存储到基金评价分析的数据库中
'''
import tushare as ts
import pandas as pd
from .core import data_api


def index_data_init():
    data_api.connect_sql()
    data_api.execute('use db_fund_info;')
    data_api.execute('truncate t_index_data;')
    data_api.close_sql()


def save_index_data(sql_statement):
    data_api.connect_sql()
    data_api.execute('use db_fund_info;')
    data_api.execute(sql_statement)
    data_api.close_sql()


def get_sql_statement(benchmark_name, benchmark_code, benchmark_data):
    sql_statement = []
    for i in range(len(benchmark_data)):
        temp_date = benchmark_data.iat[i, 0]
        temp_close = benchmark_data.iat[i, 2]
        sql_statement.append(str((benchmark_name, benchmark_code, temp_date, temp_close)))

    return "insert into t_index_data values " + ','.join(sql_statement)


def load_data():
    index_data_init()

    stk_code = '000905'
    stk_name = '中证500'
    temp_df = ts.get_k_data(stk_code, index=True)
    save_index_data(get_sql_statement(stk_name, stk_code, temp_df))

    stk_code = '000300'
    stk_name = '沪深300'
    temp_df = ts.get_k_data(stk_code, index=True)
    save_index_data(get_sql_statement(stk_name, stk_code, temp_df))


if __name__ == '__main__':
    load_data()
    print("update index data complete!")
