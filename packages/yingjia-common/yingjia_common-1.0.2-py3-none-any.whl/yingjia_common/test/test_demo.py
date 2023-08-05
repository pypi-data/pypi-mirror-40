# coding=utf-8

# 测试解析数据
import unittest
from yingjia_common.test.HTMLTestRunner import HTMLTestRunner
import coverage


class TestJiaoYiJieXi(unittest.TestCase):
    '''
    测试终端
    ...
    '''

    # @classmethod
    # def setUpClass(cls):
    #     print('这是所有case的前置条件01')
    #
    # @classmethod
    # def tearDownClass(cls):
    #     print('这是所有case的后置条件01')
    #
    def setUp(self):
        print('这是每条case的前置条件01')

    def tearDown(self):
        print('这是每条case的后置条件01')


    def test_xingu_xinxi(self):
        ''' 解析新股信息
        :return:
        '''

        self.assertTrue(1==1)

    def test_xingu_edu(self):
        '''解析
        异常测试
        :return:
        '''
        raise Exception('ex str')


def run():
    cov = None
    if True:
        cov = coverage.Coverage()
        cov.start()

    is_run_all = False  # 是否运行所有用例
    filepath = './test_demo.html'
    ftp = open(filepath, 'wb')

    if not is_run_all:
        # 查询持仓列表
        suite = unittest.TestSuite()
        suite.addTest(TestJiaoYiJieXi('test_xingu_edu'))
        suite.addTest(TestJiaoYiJieXi('test_xingu_xinxi'))
        HTMLTestRunner(stream=ftp, title='', verbosity = 2).run(suite)

    ftp.flush()
    ftp.close()

    if cov is not None:
        cov.stop()
        cov.save()
        cov.html_report(directory='test_demo')

    r = None
    with open(filepath, 'rb') as f:
        r = f.read()
    return r


if __name__ == '__main__':
    r = run()
    pass