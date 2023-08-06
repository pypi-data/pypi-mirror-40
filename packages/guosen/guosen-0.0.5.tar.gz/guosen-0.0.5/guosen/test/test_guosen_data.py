import unittest
from ..data import data_api_test


class DataTestCase(unittest.TestCase):
    """
    单元测试
    """
    @classmethod
    def tearDownClass(cls):
        pass

    # 必须使用@classmethod 装饰器,所有test运行前运行一次
    @classmethod
    def setUpClass(cls):
        cls.test_data = data_api_test

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_sql_info(self):
        self.assertEqual(len(self.test_data._sql_table_info), 9)
        self.assertTrue('t_private_fund_basic_info' in self.test_data._sql_table_info)
        self.assertTrue('product_name' in self.test_data._sql_table_info['t_product_basic_info'])
        self.assertTrue('九章幻方量化对冲2号私募基金' in self.test_data._product_name_to_id)
        self.assertTrue('宁波幻方量化投资管理合伙企业（有限合伙）' in self.test_data._fund_name_to_id)

    def test_sql_weekly_report(self):
        path = r'C:\Users\PC\OneDrive\基金研究及网页展示项目\导入数据模板表 - 测试周报数据表.xlsx'
        self.test_data.load_fund_data_from_excel(path)
        data_type = 'weekly_report'
        begin_time = '2018-12-5'
        df = self.test_data.get_fund_data(data_type=data_type, begin_time=begin_time)
        self.assertTrue(len(df), 1)
        self.assertTrue(df.iloc[0, 2], 'aaa')

    def test_sql_update(self):
        path = r'C:\Users\PC\OneDrive\基金研究及网页展示项目\导入数据模板表1.xlsx'
        self.test_data.load_fund_data_from_excel(path)

        data_type = 'fund_info'
        name = '宁波幻方量化投资管理合伙企业（有限合伙）'
        df = self.test_data.get_fund_data(data_type=data_type, name=name)
        self.assertTrue(len(df), 1)
        self.assertTrue(df.iloc[0, 2], '70亿')

        data_type = 'product_info'
        name = '九章幻方量化对冲1号私募基金'
        df = self.test_data.get_fund_data(data_type=data_type, name=name)
        self.assertTrue(len(df), 1)
        self.assertTrue(df.iloc[0, 8], '测试')

        data_type = 'quant_hedging_strategy'
        name = '九章幻方量化对冲1号私募基金'
        df = self.test_data.get_fund_data(data_type=data_type, name=name)
        self.assertTrue(len(df), 1)
        self.assertTrue(df.iloc[0, 3], "沪深300")
        pass

    def test_get_strategy_type(self):
        data_type = 'strategy_type'
        name = '量化对冲'
        df = self.test_data.get_fund_data(data_type=data_type, name=name)
        self.assertTrue(len(df), 1)
        self.assertTrue(df.iloc[0, 1], "quant_hedging")
        pass

    def test_sql_is_connect(self):
        self.test_data.connect_sql()
        self.assertTrue(self.test_data.sql_is_connect())

    def test_db_is_create(self):
        # self.test_data.create_db()
        # self.assertTrue(self.test_data.db_is_create())
        pass

    def test_load_fund_data_from_excel(self):
        # path = r'C:\Users\PC\OneDrive\基金研究及网页展示项目\导入数据模板表.xlsx'
        # path = r'/Users/kaizhang/OneDrive/基金研究及网页展示项目/导入数据模板表.xlsx'
        # self.test_data.load_fund_data_from_excel(path)
        # self.assertTrue(self.test_data._product_name_to_id.has_key('九章幻方量化对冲1号私募基金'))
        pass

    def test_get_fund_info_data(self):
        data_type = 'fund_info'
        df = self.test_data.get_fund_data(data_type=data_type)
        self.assertTrue(len(df), 2)
        self.assertTrue(df.iloc[0, 0], '宁波幻方量化投资管理合伙企业（有限合伙）')
        self.assertEqual(len(df.columns), 7)
        self.assertEqual(df.columns[5], "core_team")

    def test_get_product_info_data(self):
        data_type = 'product_info'
        # fund_name = '宁波幻方量化投资管理合伙企业（有限合伙）'
        df = self.test_data.get_fund_data(data_type=data_type, name='')
        self.assertTrue(len(df), 2)
        self.assertTrue(df.iloc[1, 1], '九章幻方量化对冲2号私募基金')
        self.assertEqual(len(df.columns), 9)
        self.assertEqual(df.columns[5], "capital_size")

    def test_get_quant_hedging_strategy_data(self):
        data_type = 'quant_hedging_strategy'
        product_name = '九章幻方量化对冲1号私募基金'
        df = self.test_data.get_fund_data(data_type=data_type, name=product_name)
        self.assertTrue(len(df), 1)
        self.assertTrue(df.iloc[0, 4], 0.2)
        self.assertEqual(len(df.columns), 7)
        self.assertEqual(df.columns[4], "risk_exposure")

    def test_get_index_enhance_strategy_data(self):
        data_type = 'index_enhance_strategy'
        product_name = '九章幻方量化对重2号私募基金'
        df = self.test_data.get_fund_data(data_type=data_type, name=product_name)
        self.assertTrue(len(df), 1)
        self.assertTrue(df.iloc[0, 3], "ccc")
        self.assertEqual(len(df.columns), 5)
        self.assertEqual(df.columns[3], "benchmark")

    def test_get_net_worth_data(self):
        data_type = 'product_price'
        product_name = '九章幻方量化对冲1号私募基金'
        df = self.test_data.get_fund_data(data_type=data_type, name=product_name)
        self.assertTrue(len(df), 85)
        self.assertEqual(len(df.columns), 5)
        self.assertEqual(df.columns[3], "net_price")


if __name__ == '__main__':
    unittest.main()
