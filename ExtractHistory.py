"""
reference
    'title':0,
    'worknumber':1,
    'authors':2,
    'giftees':3,
    'lockedStatus':4,
    'fandoms':5,
    'rating':6,
    'warnings':7,
    'categories':8,
    'wip':9,
    'pubDate':10,
    'relationships':11,
    'characters':12,
    'freeformTags':13,
    'summary':14,
    'series':15,
    'language':16,
    'wordCount':17,
    'chaptersWritten':18,
    'chaptersTotal':19,
    'collections':20,
    'comments':21,
    'kudos':22,
    'bookmarks':23,
    'hits':24,
    'visitedDate':25,
    'updateStatus':26,
    'visitCount':27
    'later':28

"""

from bs4 import BeautifulSoup
import re

def openFile():

    file = open('HistoryHTML.txt', 'r', encoding='utf-8')
    lst = file.readlines()
    file.close()

    lines=[]
    for line in lst:
        line=line.replace('|','/')
        lines.append(line)
        #print(line)

    return lines


def createFicList(lst,source):
    
    fics=[]
    fic=''

    if source == 'History':
        for line in lst:
            line = line.strip()
            if line == '':
                continue
            if line == '<a href="/works/new">Post</a>':
                continue
            if line == '<!--title, author, fandom-->':
                #create new list to hold fic info
                fic=''
            #add all the info to the fic string
            fic+=line
            #print(line)
            #print(fic)
            


            #stop the string and add it to the list
            if '<form class="ajax-remove"' in line:
                fics.append(fic)
                #print('LOOK HERE: ',fic)
                
    if source == 'Bookmarks':
        for line in lst:
            line = line.strip()
            if line == '':
                continue
            if line == '<a href="/works/new">Post</a>':
                continue
            if line == '<!--bookmark icons-->':
                #create new list to hold fic info
                fic=''
            #add all the info to the fic string
            fic+=line

            #stop the string and add it to the list
            if line == '<!--navigation and actions-->':
                fics.append(fic)
                #print(fic)

    return fics

def findLines(fic,source):
    #print('\n\n\n')
    #print(fic)
    fic=BeautifulSoup(fic, 'html.parser')
    
    authors=[]
    fandoms=[]
    relationships=[]
    characters=[]
    freeformTags=[]
    giftees=[]
    lockedStatus='Unlocked'
    #rating='N/A'
    #warnings='N/A'
    #categories='N/A'
    #wip='N/A'
    collections='0'
    series=''
    comments='0'
    bookmarks='0'
    summary=''
    wordCount=''
    kudos='0'
    #works=''
    language=''
    chaptersWritten=''
    chaptersTotal=''
    hits=''
    later='N'
    
    
    title=fic.h4.a.text
    worknumber=fic.h4.a['href'][7:]
    for item in fic.h4.find_all('a', rel='author'):
        authors.append(item.text)
    for item in fic.h4.find_all('a', href=re.compile('gifts')):
        giftees.append(item.text)
    if fic.find('img', alt='(Restricted)') != None:
        lockedStatus='Locked'
    for item in fic.h5.find_all('a', class_='tag'):
        fandoms.append(item.text)
    requiredTags=fic.find('ul', class_='required-tags').find_all('span', class_='text')
    rating=requiredTags[0].text
    warnings=requiredTags[1].text.split(', ')
    categories=requiredTags[2].text.split(', ')
    wip=requiredTags[3].text
    pubDate=fic.find('p', class_='datetime').text
    for tag in fic.find_all('li', class_='relationships'):
        relationships.append(tag.a.text)
    for tag in fic.find_all('li', class_='characters'):
        characters.append(tag.a.text)
    for tag in fic.find_all('li', class_='freeforms'):
        freeformTags.append(tag.a.text)
    if fic.find('blockquote', class_='userstuff summary') != None:
        summary=fic.find('blockquote', class_='userstuff summary').text.replace("\t", " ")
    if fic.find('ul', class_='series') != None:
        series=fic.find('ul', class_='series').a.text
    language=fic.find('dd', class_='language').text
    wordCount=fic.find('dd', class_='words').text
    chaptersWritten=fic.find('dd', class_='chapters').text.split('/')[0]
    chaptersTotal=fic.find('dd', class_='chapters').text.split('/')[1]
    if fic.find('dd', class_='collections') != None:
        collections=fic.find('dd', class_='collections').text    
    if fic.find('dd', class_='comments') != None:    
        comments=fic.find('dd', class_='comments').text
    if fic.find('dd', class_='kudos') != None:    
        kudos=fic.find('dd', class_='kudos').text    
    if fic.find('dd', class_='bookmarks') != None:    
        bookmarks=fic.find('dd', class_='bookmarks').text  
    hits=fic.find('dd', class_='hits').text
    historyInfo=fic.find('h4', class_='viewed heading').span.next_sibling
    visitedDate=historyInfo.split('(')[0].strip()
    updateStatus=historyInfo[historyInfo.find('(')+1:historyInfo.find(')')-1]
    visitInfo=historyInfo.split('Visited ')[1]
    print(historyInfo)
    if visitInfo == 'once':
        visitCount = '1'
    else:
        if "(" in visitInfo:
            visitCount = visitInfo.split("(")[0][:-5]
            later='Y'
        else:
            visitCount = visitInfo[:-5]
    
    #print(summary)
    """print()
    print('title: ',title)
    print('worknumber: ',worknumber)
    print('author: ',authors)
    print('giftees: ', giftees)
    print('lockedStatus: ', lockedStatus)
    print('fandoms: ', fandoms)
    print('rating: ',rating)
    print('warnings: ', warnings)
    print('categories: ', categories)
    print('wip: ',wip)
    print('pubDate: ', pubDate)
    print('relationships: ', relationships)
    print('characters: ', characters)
    print('freeformTags: ',freeformTags)
    print('summary: ', summary)
    print('series: ', series)
    print('language: ', language)
    print('wordCount: ', wordCount)
    print('chaptersWritten: ', chaptersWritten)
    print('chaptersTotal: ', chaptersTotal)
    print('collections: ', collections)
    print('comments: ', comments)
    print('kudos: ', kudos)
    print('bookmarks: ', bookmarks)
    print('hits: ', hits)
    print('visitedDate: ', visitedDate)
    print('updateStatus: ', updateStatus)
    print('visitCount: ', visitCount)
    print('later: ', later)"""

    


   
    
    
    if source == 'History':
        ficData=[title,
              worknumber,
              authors,
              giftees,
              lockedStatus,
              fandoms,
              rating,
              warnings,
              categories,
              wip,
              pubDate,
              relationships,
              characters,
              freeformTags,
              summary,
              series,
              language,
              wordCount,
              chaptersWritten,
              chaptersTotal,
              collections,
              comments,
              kudos,
              bookmarks,
              hits,
              visitedDate,
              updateStatus,
              visitCount,
              later]


    
    #print('print lines: ',*ficData,sep='\n')"""
    return ficData




def makeStringList(ficData):
    dataStringList=[]
    
    for line in ficData:
        
        if isinstance(line, list):
            lineString=', '.join(line)
        else:
            lineString=line
        dataStringList.append(lineString)

    return dataStringList
                

def exportAll(allData,source):
    f = open('allData.txt','w', encoding='utf-8')
    if source == 'History':
        f.write('title|worknumber|authors|giftees|lockedStatus|fandoms|rating|warnings|categories|wip|pubDate|relationships|characters|freeformTags|summary|series|language|wordCount|chaptersWritten|chaptersTotal|collections|comments|kudos|bookmarks|hits|visitedDate|updateStatus|visitCount|later')
    if source == 'Bookmarks':
      f.write('title|worknumber|authors|giftees|lockedStatus|fandoms|rating|warnings|categories|wip|pubDate|relationships|characters|freeformTags|summary|series|works|language|wordCount|chaptersWritten|chaptersTotal|collections|comments|kudos|bookmarks|hits|bookmarkType|bookmarkDate|bookmarkTags|notes')  
    f.write('\n')
    for line in allData:
        lineString='|'.join(line)
        f.write(lineString)
        f.write('\n')
    f.close()
    

def exportPrimary(allData):
    #f = open('primaryTable.txt','w', encoding='utf-8')
    print('worknumber|title|lockedStatus|rating|wip|pubDate|summary|series|language|wordCount|chaptersWritten|chaptersTotal|comments|kudos|bookmarks|hits|visitedDate|updateStatus|visitCount|later')
    for line in allData:
        lineString=line[1]+'|'+line[0]+'|'+line[4]+'|'+line[6]+'|'+line[9]+'|'+line[10]+'|'+line[14]+'|'+line[15]+'|'+line[16]+'|'+line[17]+'|'+line[18]+'|'+line[19]+'|'+line[21]+'|'+line[22]+'|'+line[23]+'|'+line[24]+'|'+line[25]+'|'+line[26]+'|'+line[27]+'|'+line[28]
        print(lineString)

def main():


    lst=openFile()
    source='History'
    fics=createFicList(lst,source)
    

    #print('start of fic 1')

    #fic=fics[1]
    #fic=BeautifulSoup(fic, 'html.parser')

    #print('print fic: ',*fic, sep='\n')

    #titleline = ''

    allData=[]
    


    for fic in fics:
    #    print(fic)
        ficData = findLines(fic,source)
    #    print(ficData)
        ficDataStringList=makeStringList(ficData)
        allData.append(ficDataStringList)
    
    #print(allData)

    exportAll(allData,source)
    #exportPrimary(allData)

    
main()


