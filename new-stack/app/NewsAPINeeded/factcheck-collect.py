import requests
from bs4 import BeautifulSoup
import argparse
from unidecode import unidecode
import re
import datetime

def get_parser():
    parser = argparse.ArgumentParser(description="FactCheck Retriever")
    parser.add_argument("-p",
                        "--pages",
                        dest="pages",
                        help="Number of FactCheck.org Pages to Pull From",
                        default='12')
    return parser

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    p = int(args.pages)

    page = 'https://www.factcheck.org/'
    nw = datetime.datetime.now()
    pastYear = []
    print str(nw.year) + " " + str(nw.month).zfill(2)
    m = nw.month
    y = nw.year
    for i in range(0,p):
        if not m > 0:
            y-=1
            m=12
        pastYear.append(page+str(y)+"/"+str(m).zfill(2)+"/")
        m-=1
    session = requests.session()
    articleCollect = []
    
    clean = re.compile('<.*?>')
    urlExpansion = []
    for url in pastYear:
        urlBase = url
        pageNum = 2
        while True:
            testUrl = url + 'page/' + str(pageNum) + '/'
            req = session.get(testUrl)
            doc = BeautifulSoup(req.content,'html.parser')
            lastP = doc.find_all(id='error-404-wrapper')
            if lastP == []:
                if not testUrl in pastYear:
                    urlExpansion.append(testUrl)
                pageNum+=1
            else:
                break
    urlExpansion = urlExpansion + pastYear

    for url in urlExpansion:
        req = session.get(url)
        doc = BeautifulSoup(req.content,'html.parser')
        roughArticles = doc.find_all(attrs={"class": "at-below-post-arch-page addthis_tool"})
        for a in roughArticles:
            b = a.get('data-url')
            if not b in articleCollect:
                articleCollect.append(b)
    with open("factCheckSheet.txt", "w") as f:
        for u in articleCollect:
            print "Accessing {}".format(u)
            req = session.get(u)
            doc = BeautifulSoup(req.content,'html.parser')
            roughArticles = doc.find_all(attrs={"class": "entry-content"})
            for a in roughArticles:
                try:
                    cl = clean.sub('',str(a.p.strong))
                    if cl[0:2] == "Q:":
                        allQ = a.find_all('p')
                        a1 = clean.sub('',str(allQ[0]))
                        a2 = clean.sub('',str(allQ[1]))
                        a1 = unidecode(unicode(a1, encoding = "utf-8"))
                        a2 = unidecode(unicode(a2, encoding = "utf-8"))
                        a1 = a1.strip()
                        a2 = a2.strip()
                        a1Temp = a1[3:]
                        a2Temp = a2[3:]
                        answerCount = a1Temp.find('\n')
                        a1copy = a1Temp
                        if answerCount > 1:
                            a1Temp = a1Temp[:answerCount]
                            a2Temp = a1.replace(a1Temp, "")
                            a2Temp = a2Temp[7:]
                        if a2Temp[:2] == "No":
                            f.write("False   | "+ str(a1Temp.strip())+" "+u+"\n")
                        elif a2Temp[:3] == "Yes":
                            f.write("True    | "+ str(a1Temp.strip())+" "+u+"\n")
                        else:
                            f.write("Unknown | "+ str(a1Temp.strip())+" "+u+"\n")    
                except:
                    pass

