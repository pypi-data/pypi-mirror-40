import pymysql
import openpyxl as oxl
import pandas as pd
# from util.logger import LogEngine
from ..util.logger import LogEngine
# from guosen.util.logger import LogEngine


class GuosenConfig(object):
    host = '172.18.32.108'
    port = 3306
    user = 'root'
    passwd = 'guosen'
    charset = 'utf8'


class HomeConfig(object):
    host = '192.168.50.232'
    port = 3306
    user = 'root'
    passwd = 'root'
    charset = 'utf8'


class SqlTableName(object):
    table_name_list = [
        't_private_fund_basic_info',
        't_product_basic_info',
        't_quant_hedging_strategy',
        't_index_enhance_strategy',
        't_net_worth']


class DevConfig(GuosenConfig):
    sql_db_name = 'db_fund_info_test'


class ProductConfig(GuosenConfig):
    sql_db_name = 'db_fund_info'


class GuosenData(object):

    def __init__(self, config=DevConfig):
        self._sql = None
        self._cursor = None
        self._data = None
        self._config = config
        self._log = LogEngine()

        # sql data
        self._sql_table_info = {}
        self._product_name_to_id = {}
        self._fund_name_to_id = {}

        self.get_sql_info()

    def get_product_name_to_id(self):
        return self._product_name_to_id

    def get_fund_name_to_id(self):
        return self._fund_name_to_id

    def get_config(self):
        return self._config

    def set_config(self, config):
        self._config = config

    def connect_sql(self):
        if not self.sql_is_connect():
            try:
                self._sql = pymysql.Connect(
                    host=self._config.host,
                    port=self._config.port,
                    user=self._config.user,
                    passwd=self._config.passwd,
                    charset=self._config.charset
                )

                self._cursor = self._sql.cursor()  # 获取游标
            except Exception as err:
                self._log.error(err)

    def close_sql(self):
        if self.sql_is_connect():
            self._cursor.close()
            self._sql.close()
            self._sql = None
            self._cursor = None

    def sql_is_connect(self):
        if self._sql is None:
            return False

        return True

    def create_db(self):
        pass

    def db_is_create(self):
        if self.sql_is_connect():
            return True

        return False

    def load_fund_data_from_excel(self, file_name):

        try:
            wb = oxl.load_workbook(file_name)
        except Exception as err:
            self._log.error(err)
            return None

        sql_head_dict = {
            't_private_fund_basic_info':
                "insert into t_private_fund_basic_info values \
                (0, '%s', '%s', '%s', '%s', '%s', '%s') \
                on duplicate key update \
                manage_scale = values(manage_scale),\
                strategy_type = values(strategy_type),\
                investment_idea = values(investment_idea),\
                core_team = values(core_team),\
                others = values(others)",

            't_product_basic_info':
                "insert into t_product_basic_info values \
                (0, '%s', %f, '%s', '%s', '%s', '%s','%s', '%s') \
                on duplicate key update \
                begin_time = values(begin_time),\
                capital_size = values(capital_size),\
                strategy_type = values(strategy_type),\
                strategy_logic = values(strategy_logic),\
                others = values(others)",

            't_quant_hedging_strategy':
                "insert into t_quant_hedging_strategy values \
                (0, %d, '%s', '%s', %f, '%s', '%s') \
                on duplicate key update \
                benchmark = values(benchmark),\
                risk_exposure = values(risk_exposure),\
                hedging_tool = values(hedging_tool),\
                others = values(others)",

            't_index_enhance_strategy':
                "insert into t_index_enhance_strategy values \
                (0, %d, '%s', '%s', '%s') \
                on duplicate key update \
                benchmark = values(benchmark),\
                others = values(others)",

            't_net_worth':
                "insert into t_net_worth(product_id, product_name, net_time,net_price) values \
                (%d, '%s', '%s', %f) \
                on duplicate key update \
                net_price = values(net_price)",

            't_weekly_report':
                "insert into t_weekly_report values \
                (0, '%s', '%s', '%s', '%s', '%s', '%s') \
                on duplicate key update \
                update_data = values(update_data),\
                quant_hedging_perform = values(quant_hedging_perform),\
                index_enhance_perform = values(index_enhance_perform),\
                summary = values(summary),\
                others = values(others)",
        }

        self.connect_sql()

        if self.sql_is_connect():

            sql_statement = 'use %s;' % (self._config.sql_db_name,)
            self.execute(sql_statement)

            for table_name, sql_head in sql_head_dict.items():
                try:
                    # table = wb.get_sheet_by_name(table_name)
                    table = wb[table_name]
                except KeyError:
                    self._log.error('Can not Find ' + table_name + ' table!')
                    continue

                excel_row_list = list(table.rows)
                if len(excel_row_list) <= 1:
                    continue

                excel_row_list = excel_row_list[1:]

                if table_name == 't_private_fund_basic_info':
                    self.save_table1(excel_row_list, sql_head)
                    self.update_fund_name_to_id()
                elif table_name == 't_product_basic_info':
                    self.save_table2(excel_row_list, sql_head)
                    self.update_product_name_to_id()
                elif table_name == 't_quant_hedging_strategy':
                    self.save_table3(excel_row_list, sql_head)
                elif table_name == 't_index_enhance_strategy':
                    self.save_table4(excel_row_list, sql_head)
                elif table_name == 't_net_worth':
                    self.save_table5(excel_row_list, sql_head)
                elif table_name == 't_weekly_report':
                    self.save_table6(excel_row_list, sql_head)
                else:
                    self._log.error('Inter Error In load_fund_data!')

            self.close_sql()

        wb.close()
        self._log.info("Save data complete!")

    def save_table6(self, excel_row_list, sql_head):
        for excel_row in excel_row_list:
            self.execute(sql_head % self.excel_row_to_tuple(excel_row))

    def save_table1(self, excel_row_list, sql_head):
        for excel_row in excel_row_list:
            self.execute(sql_head % self.excel_row_to_tuple(excel_row))

    def save_table2(self, excel_row_list, sql_head):
        for excel_row in excel_row_list:
            fund_name = excel_row[1].value

            fund_id = self._fund_name_to_id.get(fund_name, 0)
            if fund_id == 0:
                self._log.error('No fund name %s' % (fund_name,))
            else:
                sql_data = self.excel_row_to_tuple(excel_row)
                sql_statement = sql_head % ((sql_data[0],) + (fund_id,) + sql_data[1:])
                self.execute(sql_statement)

    def save_table3(self, excel_row_list, sql_head):
        self.strategy_table(excel_row_list, sql_head)

    def save_table4(self, excel_row_list, sql_head):
        self.strategy_table(excel_row_list, sql_head)

    def strategy_table(self, excel_row_list, sql_head):
        for excel_row in excel_row_list:
            product_name = excel_row[0].value

            product_id = self._product_name_to_id.get(product_name, 0)

            if product_id == 0:
                self._log.error('No product name %s' % (product_name,))
            else:
                sql_data = self.excel_row_to_tuple(excel_row)
                sql_statement = sql_head % ((product_id,) + sql_data)
                self.execute(sql_statement)

    def save_table5(self, excel_row_list, sql_head):
        '''
        存储表5
        :param excel_row_list:excel行名称的集合
        :param sql_head: sql表的头
        :return: 影响的行数
        '''
        self.strategy_table(excel_row_list, sql_head)

    def get_sql_info(self):
        """
        初始化sql表信息，把sql的表信息都写入缓存中
        :return: None
        """
        self.connect_sql()

        sql_statement = 'use %s;' % (self._config.sql_db_name,)
        self.execute(sql_statement)

        self.get_sql_table_info()
        self.update_product_name_to_id()
        self.update_fund_name_to_id()
        self.close_sql()

    def get_sql_table_info(self):
        """
        获取sql表的名称
        :return: 把sql表的表头名称都存储到缓存中
        """
        sql_statement = 'show tables;'
        _, result = self.execute(sql_statement)
        table_name_list = [table_name[0] for table_name in result]
        for table_name in table_name_list:
            _, head_result = self.get_sql_table_head_name(table_name)
            head_result = [field[0] for field in head_result]
            self._sql_table_info[table_name] = head_result

    def update_product_name_to_id(self):
        sql_statement = 'select product_name,product_id from t_product_basic_info;'
        effect, result = self.execute(sql_statement)
        if result is not None:
            self._product_name_to_id = dict(result)

    def update_fund_name_to_id(self):
        sql_statement = 'select fund_name,fund_id from t_private_fund_basic_info;'
        effect, result = self.execute(sql_statement)
        if result is not None:
            self._fund_name_to_id = dict(result)

    def excel_row_to_tuple(self, excel_row):
        data = []
        for cell in excel_row:
            data.append(cell.value)

        return tuple(data)

    def execute(self, sql_statement):
        effect = None
        result = None
        if self.sql_is_connect():
            try:
                self._cursor.execute(sql_statement)
                effect = self._sql.commit()
                result = self._cursor.fetchall()

            except Exception as e:
                self._log.error(e)
                self._log.error(sql_statement)
                self._sql.rollback()

        return (effect, result)

    def get_fund_data_by_sql_statement(self, sql_statement):
        self.connect_sql()
        db_use_sql = 'use %s;' % (self._config.sql_db_name,)
        self.execute(db_use_sql)
        effect, result = self.execute(sql_statement)
        self.close_sql()

        return (effect, result)

    def get_sql_table_head_name(self, table_name):
        '''
        根据表的名称获取表的字段信息
        :param table_name: 表名称
        :return: 表的字段信息
        '''
        sql_statement = "select COLUMN_NAME from information_schema.COLUMNS where table_name = '%s' and table_schema = '%s';" % (
            table_name, self._config.sql_db_name)
        effect, result = self.execute(sql_statement)

        return (effect, result)

    def sql_result_to_dataframe(self, sql_statement, table_name):
        _, data_result = self.get_fund_data_by_sql_statement(sql_statement)
        head_result = self._sql_table_info[table_name]
        return pd.DataFrame(data=list(data_result), columns=head_result)

    def get_product_data(self, key_id, name, table_name):
        if key_id != 0:
            sql_statement = "select * from %s where product_id = %d" % (table_name, key_id)
        elif name != '':
            sql_statement = "select * from %s where product_name = '%s'" % (table_name, name)
        else:
            sql_statement = "select * from %s" % (table_name,)
            # self._log.error("Please select product_id or product_name")

        return self.sql_result_to_dataframe(sql_statement, table_name)

    def save_visit_record(self, fund_name='', visit_time='', visit_person='', visit_content='', our_person='',
                          others=''):
        # visit_time = datetime.now()
        self.connect_sql()
        db_use_sql = 'use %s;' % (self._config.sql_db_name,)
        self.execute(db_use_sql)
        sql_statement = "insert into t_visit_record values (0, '%s', '%s', '%s', '%s', '%s', '%s')" % (
            fund_name, visit_time, visit_person, visit_content, our_person, others)
        effect, result = self.execute(sql_statement)
        self.close_sql()
        return (effect, result)

    def find_visit_record(self, fund_name='', visit_time='', visit_person='', visit_content='', our_peron='',
                          others=''):
        """
        查询访客信息,目前放回的是所有的访客信息
        :param fund_name: 基金名称
        :param visit_time: 访问时间
        :param visit_person: 访问人员
        :param visit_content: 交谈内容
        :param our_peron: 我方人员
        :param others: 其他信息
        :return: DataFrame
        """
        self.connect_sql()
        db_use_sql = 'use %s;' % (self._config.sql_db_name,)
        self.execute(db_use_sql)
        sql_statement = "select * from t_visit_record;"
        effect, result = self.execute(sql_statement)
        head_result = self._sql_table_info['t_visit_record']
        self.close_sql()
        return pd.DataFrame(data=list(result), columns=head_result)

    def save_index_data(self, index_name='', index_code='', net_time='', net_price=''):
        self.connect_sql()
        db_use_sql = 'use %s;' % (self._config.sql_db_name,)
        self.execute(db_use_sql)
        sql_statement = "insert into t_index_data values ('%s', '%s', '%s', %f) on duplicate key update net_price= values(net_price);" % (
            index_name, index_code, net_time, net_price)
        effect, result = self.execute(sql_statement)
        self.close_sql()
        return (effect, result)

    def update_index_data(self, index_name='', index_code='', net_time='', net_price=''):
        # self.connect_sql()
        # db_use_sql = 'use %s;' % (self._config.sql_db_name,)
        # self.execute(db_use_sql)
        # sql_statement = "insert into t_index_data values ('%s', '%s', '%s', %d)" % (index_name, index_code, net_time, net_price)
        # effect, result = self.execute(sql_statement)
        # self.close_sql()
        # return (effect, result)
        pass

    def find_index_data(self, index_code='', begin_time='', end_time=''):
        """
        查找指数行情数据，行情代码，开始时间，结束时间
        :param index_code: 指数代码
        :param begin_time: 开始时间
        :param end_time: 结束时间
        :return: (effect, result) 指数行情
        """
        self.connect_sql()
        db_use_sql = 'use %s;' % (self._config.sql_db_name,)
        self.execute(db_use_sql)
        if begin_time == '' and end_time == '':
            sql_statement = "select * from t_index_data where index_code = '%s' ;" % index_code
        elif begin_time == '' and end_time != '':
            sql_statement = "select * from t_index_data where index_code = '%s' and net_time <= '%s' ;" % (
                index_code, end_time)
        elif begin_time != '' and end_time == '':
            sql_statement = "select * from t_index_data where index_code = '%s' and net_time >= '%s' ;" % (
                index_code, begin_time)
        elif begin_time != '' and end_time != '':
            sql_statement = "select * from t_index_data where index_code = '%s' and net_time >= '%s' and net_time<= '%s' ;" % (
                index_code, begin_time, end_time)
        else:
            sql_statement = "select * from t_index_data where index_code = '%s' ;" % index_code

        effect, result = self.execute(sql_statement)
        self.close_sql()
        return (effect, result)

    def get_fund_data_by_productID(self, product_id):
        """
        根据产品ID获取机构信息
        :param product_id: 产品ID
        :return: DataFrame 机构信息
        """
        self.connect_sql()
        db_use_sql = 'use %s;' % (self._config.sql_db_name,)

        self.execute(db_use_sql)
        sql_statement = "select * from t_private_fund_basic_info where fund_id = (select fund_id from t_product_basic_info where product_id = %d )" % product_id
        effect, result = self.execute(sql_statement)
        head_result = self._sql_table_info['t_private_fund_basic_info']
        self.close_sql()
        return pd.DataFrame(data=list(result), columns=head_result)

    def get_visit_record_by_product_id(self, product_id):
        """
        根据产品ID获取访客信息
        :param product_id: product_id
        :return:  DataFrame table info
        """

        self.connect_sql()
        db_use_sql = 'use %s;' % self._config.sql_db_name
        self.execute(db_use_sql)
        sql_statement = "select * from t_visit_record where fund_name = (select fund_name from t_product_basic_info where product_id = %d )" % product_id
        effect, result = self.execute(sql_statement)
        head_result = self._sql_table_info['t_visit_record']
        self.close_sql()
        return pd.DataFrame(data=list(result), columns=head_result)

    def get_fund_data(self, data_type='', key_id=0, name='', begin_time='', end_time='', strategy_type=''):
        if data_type == 'fund_info':
            table_name = 't_private_fund_basic_info'
            if key_id != 0:
                sql_statement = "select * from %s where fund_id = %d" % (table_name, key_id)
            elif name != '':
                sql_statement = "select * from %s where fund_name = '%s'" % (table_name, name)
            else:
                sql_statement = "select * from %s" % (table_name,)
                # self._log.error("Please select fund_id or fund_name")

            return self.sql_result_to_dataframe(sql_statement, table_name)

        if data_type == 'product_info':
            table_name = 't_product_basic_info'
            return self.get_product_data(key_id, name, table_name)

        if data_type == 'product_price':
            table_name = 't_net_worth'
            return self.get_product_data(key_id, name, table_name)

        if data_type == 'quant_hedging_strategy':
            table_name = 't_quant_hedging_strategy'
            return self.get_product_data(key_id, name, table_name)

        if data_type == 'index_enhance_strategy':
            table_name = 't_index_enhance_strategy'
            return self.get_product_data(key_id, name, table_name)

        if data_type == 'weekly_report':
            table_name = 't_weekly_report'
            if begin_time != "":
                sql_statement = "select * from %s where time = '%s'" % (table_name, begin_time)
            else:
                sql_statement = "select * from %s order by id desc limit 1" % (table_name,)

            return self.sql_result_to_dataframe(sql_statement, table_name)

        if data_type == 'strategy_type':
            table_name = 't_strategy_type'
            if name != "":
                sql_statement = "select * from %s where strategy_type = '%s'" % (table_name, name)
            else:
                sql_statement = "select * from %s " % (table_name,)

            return self.sql_result_to_dataframe(sql_statement, table_name)

        if data_type == 'product_list':
            table_name = 't_product_basic_info'
            if key_id != 0:
                if strategy_type != '':
                    sql_statement = "select * from %s where fund_id=%d and strategy_type = '%s'" % (
                        table_name, key_id, strategy_type)
                else:
                    sql_statement = "select * from %s where fund_id=%d" % (table_name, key_id)
            else:
                sql_statement = "select * from %s " % (table_name,)

            return self.sql_result_to_dataframe(sql_statement, table_name)

        return None

    def get_index_data(self, index_name='', index_code='', start_date='', end_date=''):
        """
        获取指数的收盘数据
        :param index_name: 指数名称
        :param index_code: 指数代码
        :param start_date: 开始日期
        :param end_date: 结束日期
        :return: DataFrame
        """

        self.connect_sql()
        db_use_sql = 'use %s;' % (self._config.sql_db_name,)
        self.execute(db_use_sql)

        if index_name == '':
            if index_code == '':
                return None
            else:
                sql_statement = "select * from t_index_data where index_code = '%s'" % index_code
        else:
            sql_statement = "select * from t_index_data where index_name = '%s'" % index_name

        effect, result = self.execute(sql_statement)
        head_result = self._sql_table_info['t_index_data']
        self.close_sql()
        return pd.DataFrame(data=list(result), columns=head_result)


data_api = GuosenData(ProductConfig)
data_api_test = GuosenData(DevConfig)


def test():
    print(data_api.get_fund_data_by_productID(1))
    print(data_api.get_visit_record_by_product_id(1))
    # print(data_api.get_index_data(index_name='中证500'))


if __name__ == '__main__':
    test()
