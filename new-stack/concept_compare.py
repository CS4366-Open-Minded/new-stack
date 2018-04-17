from __future__ import division
import string
import os
import argparse

def get_parser():
    parser = argparse.ArgumentParser(description="Reddit Downloader")
    parser.add_argument("-i",
                        "--in",
                        dest="input",
                        help="File to check for similarities in",
                        default=None)

    parser.add_argument("-d",
                        "--dictionary",
                        dest="dictionary",
                        help="List of facts to check against",
                        default=None)

    return parser

def concept_checker(inputFile, dictionary):
    simList = []
    percList = []
    urlList = []
    with open(inputFile, "r") as i:
        with open(dictionary, "r") as d:
            lines = i.readlines()
            dictlines = d.readlines()
            punctuationString = "!#$%&'()*,-./:;<=>?@[]^`{|}~\""
            for line in lines:
                line1=[]
                line = line.split(',')
                line1 = [str(word).translate(None, punctuationString).strip() for word in line if str(word).translate(None, punctuationString).strip() not in line1]
                count=0
                maxCount = 0
                urlCount=0
                wordRep = []
                bestDictLine = ''
                urlCountMax=-1
                for dictline in dictlines:
                    count=0
                    urlCount+=1
                    wordRep=[]
                    dictline = dictline.split(',')
                    dictline1 = []
                    dictline1 = [str(word).translate(None, punctuationString).strip() for word in dictline if str(word).translate(None, punctuationString).strip() not in dictline1]
                    for i in line1:
                        for j in dictline1:
                            if i.lower()==j.lower():
                                if not i.lower() in wordRep:
                                    count+=1
                                    wordRep.append(i.lower())
                    if count>maxCount:
                        urlCountMax = urlCount
                        maxCount=count
                        bestDictLine = dictline
                        bDLC = dictline1
                if maxCount == 0:
                    similarityPercentage = 0
                else:
                    similarityPercentage=(2*maxCount)/(len(line1)+len(bDLC))
                #if similarityPercentage > .3:
                #    print(str(similarityPercentage)+" || "+ str(line) + " || " + str(bestDictLine))
                simList.append(str(bestDictLine))
                percList.append(str(similarityPercentage))
                urlList.append(urlCountMax)
    return simList, percList, urlList


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    sList, pList, uList = concept_checker(args.inputFile, args.dictionary)