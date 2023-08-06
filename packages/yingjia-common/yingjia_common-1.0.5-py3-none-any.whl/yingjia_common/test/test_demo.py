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
        '''   九州虚拟机版，账号登录接口
            测试账号密码：17710556243 888888
            交易账号密码：刘彬彬账号 余额 0： custid=83131004230&trdpwd_rsa=178215
            九州证券 小邱账号 余额200：83131004259 密码 159753
            http://jiaoyi.365ycyj.com/api/jzmlogin?token=b9f67ca68d0d4b189d93f5bdaaecc7ac&custid=83131004230&trdpwd_rsa=178215
        '''
        a = 1
        self.assertTrue(1==1)

    def test_xingu_edu(self):
        '''解析
        异常测试
        :return:
        '''
        raise Exception('ex str')


def run():
    cov = None
    if False:
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