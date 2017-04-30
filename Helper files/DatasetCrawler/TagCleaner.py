import pandas as pd
import collections
import os
from nltk.stem import PorterStemmer
import operator
import matplotlib.pyplot as plt
stemCache = {}

def doStemming(w):
    return w
    if w in stemCache:
        return stemCache[w]
    stemmer = PorterStemmer()
    retVal = stemmer.stem(w)
    stemCache[w] = retVal
    return retVal

def GetNewTag(inTag):
    i = inTag
    i = i.replace('[', '')
    i = i.replace(']', '')
    i = i.replace('u\'', '')
    i = i.replace('\'', '')
    i = i.replace(' ', '#')
    i = i.replace(',#', ' ')
    emptyTag = '$$NOTAG$$'
    if not len(i):
        return emptyTag

    i = i.lstrip().rstrip().lower()

    print "Processing: ", i
    iList = i.split()
    newTaglist = []
    for t in set(iList):
        t = t.replace('#', ' ')
        tSubList = t.split()
        tSortedList = []
        for w in tSubList:
            tSortedList.append(doStemming(w))
        tSortedList.sort()
        newTag = " ".join(tSortedList)
        newTaglist.append(newTag)
    return newTaglist

def tagCleaner():
    emptyTag = '$$NOTAG$$'
    base_directory = '/Users/sidverma/Desktop/'
    os.chdir(base_directory)
    #merge two files
    df = pd.read_csv('Final0-1500.csv')
    df2 = pd.read_csv('Final1500-3000.csv')
    df = df.append(df2, axis = 0)
    #start reading Tagscols
    tagsCol = df['Tags']
    index = 0
    for i in tagsCol:
        '''
        if index == 20:
            print "Exitting!"
            return
        print "Initial Tag: ", i
        '''
        if i == '[]':
            df.set_value(index, 'Tags', emptyTag)
            index += 1
            continue
        if not isinstance(i, str):
            df.set_value(index, 'Tags', emptyTag)
            index += 1
            continue
        newTag = GetNewTag(i)
        df.set_value(index, 'Tags', newTag)
        index += 1
    df.to_csv('Final0-2999.csv')
    return


def getTagFreqDict():
    base_directory = '/Users/sidverma/Desktop/'
    os.chdir(base_directory)
    globalTags = []
    df = pd.read_csv('Final0-2999.csv')
    tagsCol = df['Tags']
    index = 0
    emptyTag = '$$NOTAG$$'
    for i in tagsCol:
        iList = i.split()
        for t in iList:
            globalTags.append(t)
    return collections.Counter(globalTagsList)

def Retagger():
    tagCleaner()
    freqDict = getTagFreqDict()
    print len(freqDict)
    '''
    lists = sorted(freqDict.items(), key=operator.itemgetter(1), reverse = True)
    i = 0
    pop_tags = []
    for tup in lists:
        i += 1
        if i == 1000:# if tup[1] < 1000:
            break
    lists = lists[:i]
    f = open('poptags', 'w')
    for tu in lists :
        f.write(str(tu[0])+'\n')
    print 'done'
    f.close()
    '''

Retagger()

# xTicks, y = zip(*lists) # unpack a list of pairs into two tuples
# #plt.figure(figsize = (90,30))
# x = xrange(len(lists))
# plt.xticks(x, xTicks, rotation=90)
# # plt.plot(x,y)
# plt.bar(x, y, color='b')
# plt.show()
# print 'done'