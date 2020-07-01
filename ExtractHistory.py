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
    'visitCount':27}

"""
def openFile():

    file = open('raw_bookmarks', 'r')
    lst = file.readlines()
    file.close()

    lines=[]
    for line in lst:
        line=line.replace('|','/')
        lines.append(line)

    return lines


def createFicList(lst,source):
    
    fics=list()
    fic=list()

    if source == 'History':
        for line in lst:
            line = line.strip()
            if line == '':
                continue
            if line == '<a href="/works/new">Post</a>':
                continue
            if line == '<!--title, author, fandom-->':
                #create new list to hold fic info
                fic=list()
            #add all the info to the fic string
            fic.append(line)

            #stop the string and add it to the list
            if 'role=\"article\">' in line:
                fics.append(fic)
                #print(fic)
                
    if source == 'Bookmarks':
        for line in lst:
            line = line.strip()
            if line == '':
                continue
            if line == '<a href="/works/new">Post</a>':
                continue
            if line == '<!--bookmark icons-->':
                #create new list to hold fic info
                fic=list()
            #add all the info to the fic string
            fic.append(line)

            #stop the string and add it to the list
            if line == '<!--navigation and actions-->':
                fics.append(fic)
                #print(fic)

    return fics

def findLines(fic,source):

    
    giftees=['']
    lockedStatus='Unlocked'
    #rating='N/A'
    #warnings='N/A'
    #categories='N/A'
    #wip='N/A'
    collections=''
    series=''
    comments=''
    bookmarks=''
    summary=''
    wordCount=''
    kudos=''
    works=''
    language=''
    chaptersWritten=''
    chaptersTotal=''
    hits=''
    
    lineNumber = 0
    summaryFound = 'No'
    isSeries = 'No'
    isExternal = 'No'
    
    for line in fic:


        
        #get lines
        if line == '<!--title etc-->':
            isSeries = 'Yes'

        if isSeries == 'Yes':
            if line.startswith('<a href="/series/') == True:
                title, worknumber=getTitleInfo(fic[lineNumber],17)
                #print(line)
            if line == '<dt>Words:</dt>':
                words=fic[lineNumber+1]
                wordCount=words[4:-6]
                #print(wordCount)
            if line == '<dt>Works:</dt>':
                workLine=fic[lineNumber+1]
                works=workLine[4:-6]
                #print(works)
            
        if line == '<ul class="required-tags">':
            tagsSection=fic[lineNumber-1:lineNumber+13]
            rating, warnings, categories, wip, pubDate, relationships, characters, freeformTags = getTags(tagsSection)

        if line.startswith('<a href="/external_works/') == True:
            title, worknumber=getTitleInfo(fic[lineNumber],25)
            isExternal = 'Yes'
            #print(line)
            
        if line.startswith('<a href=\"/works/') == True:
            title, worknumber=getTitleInfo(fic[lineNumber],16)
            #print(line)
            
        if line == 'by':
            if isExternal == 'No':
                authors=makeSectionList(fic[lineNumber+2])
            if isExternal == 'Yes':
                authors=fic[lineNumber+1]
            #print(authors)

        if line.startswith('for <a href="') == True:
            giftees=makeSectionList(fic[lineNumber])

        if line == '<img alt="(Restricted)" title="Restricted" src="/images/lockblue.png" width="15" height="15"/>':
            lockedStatus='Locked'
            
        if line.startswith('<span class="landmark">Fandom')==True:
            fandoms = makeSectionList(fic[lineNumber + 1])

        if line == '<!--required tags-->':
            tagsSection=fic[lineNumber:lineNumber+13]
            rating, warnings, categories, wip, pubDate, relationships, characters, freeformTags = getTags(tagsSection)

        if line == '<!--summary-->':
            summaryStart=lineNumber+2

        if line == '</blockquote>':
            if summaryFound == 'No':
                
                summary=getSummary(fic[summaryStart+1:lineNumber])
                summaryFound = 'Yes'


        if line == '<h6 class="landmark heading">Series</h6>':
            series=pullText(fic[lineNumber+3],4)

        if line.startswith('<dd class="language">') == True:
            language=pullText(line,5)

        if line.startswith('<dd class="words">') == True:
            wordCount=pullText(line,5)

        if line.startswith('<dd class="chapters">') == True:
            if line.startswith('<dd class="chapters"><a href="') == True:
                chapters=pullText(line[21:],5)
                chapters=chapters.replace('</a>','')
            else:
                chapters=pullText(line,5)
            chaptersList=chapters.split('/')
            chaptersWritten=chaptersList[0]
            chaptersTotal=chaptersList[1]

        if line.startswith('<dd class="collections">') == True:
            collections=pullText(line[24:],9)

        if line.startswith('<dd class="comments">') == True:
            comments=pullText(line[21:],9)
            
        if line.startswith('<dd class="kudos">') == True:
            kudos=pullText(line[18:],9)

        if line.startswith('<dd class="bookmarks">') == True:
            bookmarks=pullText(line[22:],9)

        if line == '<dt>Bookmarks:</dt>':
            bookmarkLine=fic[lineNumber+1]
            bookmarks=pullText(bookmarkLine,9)
            #print(bookmarks)

        if line.startswith('<dd class="hits">') == True:
            hits=pullText(line,5)

        if source == 'History':
            if line.startswith('<span>Last visited:</span>') == True:
                visitedDate=line[27:]
                updateStatus=getUpdateStatus(fic[lineNumber+1])
                visitCount=getVisitCount(fic[lineNumber+2])

        if source == 'Bookmarks':
            if line == '<!--bookmark icons-->':
                bookmarkType=getBookmarkType(fic[lineNumber+2])
            if line == '<!--bookmarker, time-->':
                bookmarkDate=pullText(fic[lineNumber+4],4)                
            if line == '<!--meta-->':
                bookmarkTagsStart=lineNumber
            if line == '<!--notes-->':
                bookmarkSection=fic[bookmarkTagsStart+3:lineNumber-1]
                bookmarkTags=getBookmarkTags(bookmarkSection)
                notesStart=lineNumber
            if line == '<!--navigation and actions-->':
                notes=getNotes(fic[notesStart+2:lineNumber-1])
                

        lineNumber += 1     
    
    
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
              works,
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
              visitCount]
    if source == 'Bookmarks':
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
              works,
              language,
              wordCount,
              chaptersWritten,
              chaptersTotal,
              collections,
              comments,
              kudos,
              bookmarks,
              hits,
              bookmarkType,
              bookmarkDate,   
              bookmarkTags,
              notes]

    
    #print('print lines: ',*ficData,sep='\n')
    return ficData

def pullText(section,number):
    start=section.find('\">') + 2
    text=section[start:-number]
    return text

def pullTextFromTags(section,number):
    start=section.find('text">')+6
    text=section[start:-number]
    return text

def getTitleInfo(titleSection,number):
    endNumber=titleSection.find('\">')
    worknumber=titleSection[number:endNumber]
    title=pullText(titleSection,4)
    return title, worknumber

def makeSectionList(section):
    #if there could be more than one on the line
    lineSplit = section.split(',')
    sectionList=[]
    for line in lineSplit:
        item=pullText(line,4)
        sectionList.append(item)
    return sectionList

def pullTags(section):
    tagList=section.split('</li>')
    relationships=[]
    characters=[]
    freeformTags=[]
    for tag in tagList:
        tag=tag.strip()
        if tag.startswith('<li class=\'relationships\'>') == True:
            ship=pullText(tag,4)
            relationships.append(ship)
        if tag.startswith('<li class=\'characters\'>') == True:
            character=pullText(tag,4)
            characters.append(character)
        if tag.startswith('<li class=\'freeforms\'>') == True:
            tagText=pullText(tag,4)
            freeformTags.append(tagText)
            
    return relationships,characters,freeformTags
        
def getTags(tagsSection):
    rating=pullTextFromTags(tagsSection[2],23)
    warningString=pullTextFromTags(tagsSection[3],23)
    warnings=warningString.split(', ')
    categoryString=pullTextFromTags(tagsSection[4],23)
    categories=categoryString.split(', ')
    wip=pullTextFromTags(tagsSection[5],23)
    pubDate=pullText(tagsSection[7],4)
    relationships,characters,freeformTags=pullTags(tagsSection[12])
    return rating, warnings, categories, wip, pubDate, relationships, characters, freeformTags

def getSummary(section):
    summary=' '.join(section)
    summary=summary.replace('<p>','')
    summary=summary.replace('</p>',' ')
    summary=summary.replace('<em>','')
    summary=summary.replace('</em>','')
    summary=summary.replace('<strong>','')
    summary=summary.replace('</strong>','')
    summary=summary.replace('<br/>','')
    summary=summary.strip()
    return summary

def getUpdateStatus(section):
    updateStatus=section.replace('(','')
    updateStatus=updateStatus.replace('.','')
    updateStatus=updateStatus.replace(')','')
    return updateStatus

def getVisitCount(section):
    if section == 'Visited once':
        visitCount='1'
    else:
        visitCount=section[8:-6]
    return visitCount

def getBookmarkType(section):
    bookmarkType=pullTextFromTags(section,18)
    return bookmarkType

def getBookmarkTags(section):
    tags=[]
    for line in section:
        tag=pullText(line,9)
        tags.append(tag)
    return tags

def getNotes(section):
    notes=' '.join(section)
    notes=notes.replace('<p>','')
    notes=notes.replace('</p>',' ')
    notes=notes.replace('<em>','')
    notes=notes.replace('</em>','')
    notes=notes.replace('<strong>','')
    notes=notes.replace('</strong>','')
    notes=notes.strip()
    return notes

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
    f = open('allData.txt','w')
    if source == 'History':
        f.write('title|worknumber|authors|giftees|lockedStatus|fandoms|rating|warnings|categories|wip|pubDate|relationships|characters|freeformTags|summary|series|works|language|wordCount|chaptersWritten|chaptersTotal|collections|comments|kudos|bookmarks|hits|visitedDate|updateStatus|visitCount')
    if source == 'Bookmarks':
      f.write('title|worknumber|authors|giftees|lockedStatus|fandoms|rating|warnings|categories|wip|pubDate|relationships|characters|freeformTags|summary|series|works|language|wordCount|chaptersWritten|chaptersTotal|collections|comments|kudos|bookmarks|hits|bookmarkType|bookmarkDate|bookmarkTags|notes')  
    f.write('\n')
    for line in allData:
        lineString='|'.join(line)
        f.write(lineString)
        f.write('\n')
    f.close()

def main():


    lst=openFile()
    source='Bookmarks'
    fics=createFicList(lst,source)
    

    print('start of fic 1')

    fic=fics[1]

    #print('print fic: ',*fic, sep='\n')

    titleline = ''

    allData=[]
    


    for fic in fics[1:]:
        ficData = findLines(fic,source)
        ficDataStringList=makeStringList(ficData)
        allData.append(ficDataStringList)

    exportAll(allData,source)

    
main()
