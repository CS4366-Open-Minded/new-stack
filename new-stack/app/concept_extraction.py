import string
import json
import os
import argparse
from nltk.corpus import stopwords

def get_parser():
    parser = argparse.ArgumentParser(description="Reddit Downloader")
    parser.add_argument("-t",
                        "--type",
                        dest="filetype",
                        help="Type of file to pull text from",
                        default=None)

    parser.add_argument("-f",
                        "--file",
                        dest="filename",
                        help="Name of file to pull text from",
                        default=None)

    return parser

def text_extractor(name, typ):
    if typ=="JSON":
        with open(name) as f:
            d = json.load(f)
        for i in d:
            text = d[i][0]['text']
    elif typ=="TXT":
        with open(name) as f:
            lines = f.readlines()
            text = []
            for line in lines:
                text.append(line)
    return text

def concept_extractor(name, text, stopwordList, typ):
    text = text.lower() #Makes all uppercase letters lowercase.
    if typ == "JSON":
        text = text.replace(".", "_")
        text = text.replace("?", "_")
        text = text.replace("!", "_")
    punctuationString = "!#$%&'()*,-./:;<=>?@[]^`{|}~\""
    text = str(text).translate(None, punctuationString)
    text = text.split()
    text = [word for word in text if word not in stopwordList]
    if typ == "JSON":
        text = ', '.join(text)
    else:
        text = ' '.join(text)
    text = text.replace('_,',' |')
    text = text.replace(', |',' |')
    text = text.replace('||,','||')
    text = text.replace('|| | ','|| ')
    text = text.split(' ')
    sent = []
    
    if typ=="JSON":
        with open(name.split(".",1)[0]+'_concepts.txt', "w") as f:
            for w in text:
                if w == "|":
                    f.write(str(sent)+'\n')
                    sent = []
                else:
                    sent.append(w.replace(',',''))
    
    return text
    

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    with open('custom_stopwords.txt') as e:
        stopwordList=e.read()+','.join(set(stopwords.words('english')))
    
    urlHold = []
    text = text_extractor(args.filename, args.filetype)
    for s in text:
        ttemp = s.split()
        #ttemp = ttemp.split(" ")
        urlHold.append(ttemp[-1])
    print "/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/"
    if args.filetype=="TXT":
        retText = []
        for i in text:
            x = concept_extractor(args.filename, i, stopwordList, args.filetype)
            retText.append(x[1:-1])
            #urlHold.append(x[-1])
        with open(args.filename.split(".",1)[0]+'_concepts.txt', "w") as f:
            for l in retText:
                f.write(str(l)+'\n')
    else:
        retText = concept_extractor(args.filename, text, stopwordList, args.filetype)
    with open('url.txt', 'w') as out:
        for i in range(0, len(urlHold)):
            out.write(urlHold[i]+'\n')
    print retText

