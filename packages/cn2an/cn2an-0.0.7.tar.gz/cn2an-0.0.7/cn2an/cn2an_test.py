import unittest

from cn2an.cn2an import Cn2An

class Cn2anTest(unittest.TestCase):
    def setUp(self):
        self.test_datas = {
            "零点零零零零五零五": 0.0000505,
            "零点零零零零五零": 0.000050,
            "零点零零零零五": 0.00005,
            "零点零零": 0.00,
            "零点零": 0.0,
            "一": 1,
            "壹": 1,
            "十一": 11,
            "一十一": 11,
            "一百万零五十四": 1000054,
            "壹佰万零伍十肆": 1000054,
        }
    
    def test_a_run(self):
        self.assertEqual(1, 1)  # 测试用例

if __name__ == '__main__':
    unittest.main()