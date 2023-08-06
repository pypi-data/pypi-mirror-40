#针对企查查的爬虫代码.
#import wcc
from wcc import getpage_qichacha

def main():
    url = "https://www.qichacha.com/gs_1473975991543754066"
    resp_html = getpage_qichacha(url)
    print(resp_html)


if __name__ == "__main__":
    main()

