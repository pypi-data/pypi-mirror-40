#针对企查查的爬虫代码.
#import wcc
from wcc import getpage_qichacha
from wcc import get_orginfo
from wcc import get_firminfo

def main1():
    
    #url = "https://www.qichacha.com/cbase_s27c65101960060e65d0a975ca503e19.html"
    url = "https://www.qichacha.com/cbase_b6dfd8fd3ecf8560a768fbc757fd07d4.html"
    #测试有些页面通过seo找不到法人
    url = "https://www.qichacha.com/cbase_4d8b7f1d12b71a8b6008bc1a3cf505b8.html"
    url = "https://www.qichacha.com/cbase_60cbfa629c36b8deaf4f4f44c82fca30.html" 
    url = "https://www.qichacha.com/cbase_1dbdd40b84bcb48d90319fbb444d230f.html"
    url = "https://www.qichacha.com/cbase_44ab562711f16ba7dd7fd0c6cf84cf40.html"
    url = "https://www.qichacha.com/cbase_d8ce9113da609c28500cd19ceaa83530.html"
    resp_text = getpage_qichacha(url)
    com = get_firminfo(url,resp_text)
    print(com)

#测试连接没有以.html结束
def main2():
    
    #url = "https://www.qichacha.com/cbase_05866048402c2e792f7b305e75eb2740"
    url = "https://www.qichacha.com/cbase_05866048402c2e792f7b305e75eb2740.html"
    resp_text = getpage_qichacha(url)
    com = get_firminfo(url,resp_text)
    print(com)


if __name__ == "__main__":
    main1()

