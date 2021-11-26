# -*- coding:utf-8 -*-
#作者:修仙队zz020zz
from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
from bs4 import BeautifulSoup
import time
import win32api,win32con
import os
import re
import logging
# 学习强国各页面链接
## 首页
HOME_PAGE = 'https://www.xuexi.cn/'
## 登录
LOGIN_LINK = 'https://pc.xuexi.cn/points/login.html'
## 学习时评
ARTICLES_LINK = 'https://www.xuexi.cn/d05cad69216e688d304bb91ef3aac4c6/9a3668c13f6e303932b5e0e100fc248b.html'
## 重要活动视频专辑
VIDEO_LINK = 'https://www.xuexi.cn/a191dbc3067d516c3e2e17e2e08953d6/b87d700beee2c44826a9202c75d18c85.html'
## 新闻联播
LONG_VIDEO_LINK = 'https://www.xuexi.cn/8e35a343fca20ee32c79d67e35dfca90/7f9f27c65e84e71e1b7189b7132b4710.html'
## 我的分数
SCORES_LINK = 'https://pc.xuexi.cn/points/my-points.html'
##每日答题
DAY_PAGE = 'https://pc.xuexi.cn/points/exam-practice.html'
WEEK_PAGE = 'https://pc.xuexi.cn/points/exam-weekly-list.html'
ZHUANXIANG_PAGE = 'https://pc.xuexi.cn/points/exam-paper-list.html'

# 浏览器加载选项,options下两个方法是不记录日志：连到系统上的设备没有发挥作用
options = webdriver.ChromeOptions()
options.add_argument('–log-level=3')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# 使用chrome浏览器 指定webdriver.exe地址
browser = webdriver.Chrome(executable_path=r'chromedriver.exe',options=options)
"""
设置隐性等待最长时间
有的页面加载快 有的加载慢 使用隐性等待 加载完即执行 
比sleep(30)强制等待要智能
全局设置一次即可
"""
browser.implicitly_wait(4)
#日志设置
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='my.log', level=logging.INFO, format=LOG_FORMAT)
logging.debug("This is a debug1 log.")
logging.info("This is a info log.")
def login_simulation():
    """
    模拟登录
    :由于token有时效，过一段时间就失效了
    :所以这个版本仅支持手工登录
    :后续版本看是否能改成自动登录
    """
    # 方式一：使用cookies方式
    # 先自己登录，然后复制token值覆盖
    # cookies = {'name': 'token', 'value': ''}
    # browser.add_cookie(cookies)
 
    # 方式二：自己扫码登录
    browser.get(LOGIN_LINK) # 打开登录页面
    browser.maximize_window() # 窗口最大化
    # 自动滚到最下面
    browser.execute_script("var q=document.documentElement.scrollTop=1000")
    # 打开一个“确定”弹窗 等待手工操作点确认 类似于cmd的pause
    win32api.MessageBox(0, "扫描完二维码以后点击我", "提醒",win32con.MB_ICONASTERISK)
    
    browser.get(HOME_PAGE) # 登陆完毕跳转到主页
    print("模拟登录完毕\n")
 
def read_articles():
    """阅读文章"""
    # 打开 学习时评页面
    browser.get(ARTICLES_LINK)
    print("自动阅读文章...\n")
    # 获取页面上所有的文章的链接列表
    articles = browser.find_elements_by_xpath("//span[@class='text']")
    print("捕获文章"+str(len(articles))+"个")
    for index, article in enumerate(articles):
        # 每篇文章后面跟着的日期的也是一个链接 点击同样有效
        if (index%2) != 0: 
            continue
        if index > 12: # 阅读文章数达到6篇即可
            break
        article.click() # 点击文章
        all_handles = browser.window_handles # 获得所有浏览器窗口句柄
        browser.switch_to.window(all_handles[-1]) # 切换到最后一个打开的窗口
        # 模拟人工阅读文章
        # 每隔5秒向下滚动一下屏幕
        for i in range(0, 2000, 200):
            js_code = "var q=document.documentElement.scrollTop=" + str(i)
            browser.execute_script(js_code)
            time.sleep(5)
        # 每隔5秒向上滚动一下屏幕
        for i in range(2000, 0, -200):
            js_code = "var q=document.documentElement.scrollTop=" + str(i)
            browser.execute_script(js_code)
            time.sleep(5)
        time.sleep(2) # 再等待80秒
        # 每篇文章的阅读时间是: (2000/200)*5+(2000/200)*5+80=180秒
        browser.close() # 关闭当前窗口
        browser.switch_to.window(all_handles[0]) # 切换到第一个窗口
    print("阅读文章完毕\n")

def watch_videos():
    """观看视频"""
    print("自动观看视频...\n")
    # 打开 重要活动专辑 页面
    browser.get(VIDEO_LINK)
    videos = browser.find_elements_by_xpath("//span[@class='text']")
    print("捕获视频："+str(len(videos))+"个")
    for i, video in enumerate(videos):
        # 每篇文章后面跟着的日期的也是一个链接 点击同样有效
        if (i%2) != 0: 
            continue
        if i > 8:
            break
        video.click() # 点击视频
        all_handles = browser.window_handles # 获得所有浏览器窗口句柄
        logging.info(str("视频all_handles：{0}").format(all_handles))
        browser.switch_to.window(all_handles[-1]) # 切换到最后一个打开的窗口
        while True:
            try:
                obj = re.findall('重新播放',browser.find_element_by_xpath("//*[@class='replay-btn']").text)
                logging.info('触发obj')
                break
            except Exception as e:
                logging.info('未找到重新播放,继续while')
                time.sleep(10)
                continue
        browser.close()
        browser.switch_to.window(all_handles[0])
    print("视频观看完毕\n")
    return
def get_scores():
    """获取当前积分"""
    browser.get(SCORES_LINK)
    time.sleep(2)
    gross_score = browser.find_element_by_xpath("//*[@id='app']/div/div[2]/div/div[2]/div[2]/span[1]")\
        .get_attribute('innerText')
    today_score = browser.find_element_by_xpath("//span[@class='my-points-points']").get_attribute('innerText')
    logging.info(str("当前总积分:{0}").format(str(gross_score)))
    logging.info(str("今日积分:{0}").format(str(today_score)))
    print("当前总积分：" + str(gross_score))
    print("今日积分：" + str(today_score))
    print("获取积分完毕，即将退出\n")
 
def isElementExist(element):
    flag=True
    try:
        browser.find_element_by_xpath(element)
        return flag
    except:
        flag=False
        return flag
#判断提示里有几个font和获取font内容
def isFontExist():
    #初始化参数
    flag_list = []
    flag_font = 0
    font_txt = 'empty'
    try:
        #获取页面中的提示个数
        for i in range(1,7):
            logging.info(str("获取答案循环{0}").format(i))
            time.sleep(0.5)
            font_txt = browser.find_element_by_xpath("//*[@class='line-feed']/font["+str(i)+"]").text
            logging.info(str("答案为{0}").format(font_txt))
            time.sleep(0.5)
            flag_font = i#标记值
            flag_list.append(font_txt)#加入list中
    except:
        logging.info('提示获取完毕，抛出')
        try:
            #针对有些题目导致list[0]为''，故作此判断
            #20211124bug：将0值触发函数改到这里触发,flag_font-1
            if flag_list[0] == '':
                logging.info(str("出现空值，删掉{0}").format(flag_list[0]))
                flag_list.pop(0)
                flag_font = flag_font -1
        except Exception as e:
            logging.info(str("删除空值错误：{0}").format(e))
        #将list补全为五个元素，满足绝大部分场景
        logging.info('将list补全为五个元素')
        for j in range(5):
            if flag_font != 5:
                flag_list.append('empty')
                flag_font = flag_font + 1
            else:
                break
        return flag_font,flag_list
#匹配后进行选择操作
def click_xuanze(flag_font,flag_list):
    k = False#如果没有值匹配上，k值为0，则触发备用机制点击默认第一项保证正常运行
    logging.info('进入选择函数')
    for i in range(5):
        for j in flag_list:
            pattern = '.*?' + j + '.*?'#正则表达式匹配全部元素
            logging.info(str("尝试模糊匹配pattern值与答案:{0}").format(pattern))
            obj = re.findall(pattern,browser.find_element_by_xpath("//*[@class='q-answers']/div["+str(i+1)+"]").text)
            if len(obj)>0:
                try:
                    logging.info('匹配成功,点击')
                    k = True
                    browser.find_element_by_xpath("//*[@class='q-answers']/div["+str(i+1)+"]").click()
                    time.sleep(0.5)
                    flag_list.remove(j)
                except Exception as e:
                    logging.info(str("匹配失败，找不见选择项：{0}").format(e))
                    continue
            else:
                logging.info('匹配失败')
    #20211124bug：k为false才能触发该IF
    if k == False:
        logging.info('触发容错，点击默认第一项和第二项（防止是多选）')
        browser.find_element_by_xpath("//*[@class='q-answers']/div[1]").click()
        browser.find_element_by_xpath("//*[@class='q-answers']/div[2]").click()
#每日答题
def anwser_dayquestion(Page):
    print('自动答题中...')
    logging.info('进入答题主函数')
    logging.info('答题类型判断')
    DatiJudge(Page)
    logging.info('判断完成，开始答题')
    for i in range(0,14):
        try:
            #可用：获取提示和提示中的红字
            browser.find_element_by_class_name("tips").click()
            logging.info('isFontExist获取提示中的答案')
            flag_font, flag_list = isFontExist()
            #获取提示后直接吧提示点没
            browser.find_element_by_class_name("tips").click()
            logging.info(str("flag_font和flag_list为：{0},{1}").format(flag_font,flag_list))
            if isElementExist("//*[@class='q-body']/div/input"):
                if flag_font != 0:
                    logging.info("判断为视频或填空题")
                    try:
                        logging.info('尝试将flag_list填入视频或填空题中')
                        for j in range(3):
                            browser.find_element_by_xpath("//*[@class='q-body']/div["+str(j+1)+"]/input").send_keys(flag_list[j])
                    except Exception as e:
                        logging.info(str("填入出错：{0}").format(e))
            if isElementExist("//*[@class='q-answers']"):
                logging.info("判断为选择题,尝试匹配点击")
                try:
                    logging.info("执行click_xuanze函数")
                    click_xuanze(flag_font,flag_list)
                except Exception as e:
                    logging.info(str("执行click_xuanze函数出错：{0}").format(e))
            time.sleep(1)
            try:
                logging.info('点击确定')
                browser.find_element_by_xpath("//*[@class='ant-btn next-btn ant-btn-primary']").click()
                time.sleep(1)
                try:
                    logging.info('点击下一题')
                    browser.find_element_by_xpath("//*[@class='ant-btn next-btn ant-btn-primary']").click()
                    browser.find_element_by_xpath("//*[@class='ant-btn submit-btn ant-btn-primary ant-btn-background-ghost']").click()#点击交卷
                except Exception as e:
                    logging.info(str("没有下一题了：{0}").format(e))
            except UnexpectedAlertPresentException:
                print('弹窗报错了吗？')
                #防止弹窗报错
                browser.switch_to.alert.accept()
                continue
        except Exception as e:
            logging.info(str("答题大循环：{0}").format(e))
            continue
def DatiJudge(Page):
    if Page == WEEK_PAGE or Page == ZHUANXIANG_PAGE:
        logging.info('周或专项答题，需要做判断是否有可用题目')
        browser.get(Page)
        time.sleep(5)
        try:
            for i in range(50):
                try:
                    time.sleep(0.5)
                    logging.info('查找可答题目')
                    browser.find_element_by_xpath("//*[@class='ant-btn button ant-btn-primary']").click()
                    break
                except Exception as e:
                    logging.info(str("本页没有可答题目了：{0}").format(e))
                    logging.info('点击下一页')
                    time.sleep(0.5)
                    browser.find_element_by_xpath("//*[@class='anticon anticon-right']").click()
                    continue
        except Exception as e:
            logging.info(str("DatiJudge报错：{0}").format(e))
    else:
        logging.info('进入每日答题')
        browser.get(Page)
if __name__ == '__main__':
    print("---------"+time.strftime('%Y.%m.%d',time.localtime(time.time())))
    login_simulation()  # 模拟登录
    read_articles()     # 阅读文章
    watch_videos()      # 观看视频
    anwser_dayquestion(DAY_PAGE)#每日答题
    anwser_dayquestion(WEEK_PAGE)#每周答题
    anwser_dayquestion(ZHUANXIANG_PAGE)#专项答题
    get_scores()        # 获得今日积分
    browser.quit()      # 关闭浏览器
    input()