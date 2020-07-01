"""Cas Sweeney
History Code
Rewritten to include classes
28-June-2020"""


from Fic import Fic

def openFile():
    file = open('testHistory.txt', 'r', encoding='utf-8')
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
    ficText=''
    
    if source == 'History':
        for line in lst:
            line = line.strip()
            if line == '':
                continue
            if line == '<a href="/works/new">Post</a>':
                continue
            if line == '<!--title, author, fandom-->':
                #create new list to hold fic info
                ficText=''
            #add all the info to the fic string
            ficText+=line
            
            #stop the string and add it to the list
            if '<form class="ajax-remove"' in line:
                fic = Fic(ficText)
                #ficData=defineFic(fic, source)
                fics.append(fic)
                #print(ficData)
    return fics


"""def defineFic(fic,source):
    #shouldn't do this until ready to export
    #can call the fields as generating the line to print
    if source == 'History':
        ficData=[fic.title,
              fic.worknumber,
              fic.authors,
              fic.giftees,
              fic.lockedStatus,
              fic.fandoms,
              fic.rating,
              fic.warnings,
              fic.categories,
              fic.wip,
              fic.pubDate,
              fic.relationships,
              fic.characters,
              fic.freeformTags,
              fic.summary,
              fic.series,
              fic.language,
              fic.wordCount,
              fic.chaptersWritten,
              fic.chaptersTotal,
              fic.collections,
              fic.comments,
              fic.kudos,
              fic.bookmarks,
              fic.hits,
              fic.visitedDate,
              fic.updateStatus,
              fic.visitCount,
              fic.later]
    return ficData"""
        
    
def makeString(value):
    #make a field that is a list into a string
    if isinstance(value, list):
        lineString=', '.join(value)
    else:
        lineString=value

    return lineString    
    
def exportAll(fics,source):
    f = open('allData.txt','w', encoding='utf-8')
    if source == 'History':
        f.write('title|worknumber|authors|giftees|lockedStatus|fandoms|rating|warnings|categories|wip|pubDate|relationships|characters|freeformTags|summary|series|language|wordCount|chaptersWritten|chaptersTotal|collections|comments|kudos|bookmarks|hits|visitedDate|updateStatus|visitCount|later')
    if source == 'Bookmarks':
        f.write('title|worknumber|authors|giftees|lockedStatus|fandoms|rating|warnings|categories|wip|pubDate|relationships|characters|freeformTags|summary|series|works|language|wordCount|chaptersWritten|chaptersTotal|collections|comments|kudos|bookmarks|hits|bookmarkType|bookmarkDate|bookmarkTags|notes')  
    f.write('\n')
    for fic in fics:
        ficData=[fic.title,
              fic.worknumber,
              makeString(fic.authors),
              makeString(fic.giftees),
              fic.lockedStatus,
              makeString(fic.fandoms),
              fic.rating,
              makeString(fic.warnings),
              makeString(fic.categories),
              fic.wip,
              fic.pubDate,
              makeString(fic.relationships),
              makeString(fic.characters),
              makeString(fic.freeformTags),
              fic.summary,
              fic.series,
              fic.language,
              fic.wordCount,
              fic.chaptersWritten,
              fic.chaptersTotal,
              fic.collections,
              fic.comments,
              fic.kudos,
              fic.bookmarks,
              fic.hits,
              fic.visitedDate,
              fic.updateStatus,
              fic.visitCount,
              fic.later]
        f.write('|'.join(ficData))
        f.write('\n')
    f.close()


def main():
    source='History'
    lst=openFile()
    
    fics=createFicList(lst,source)
    exportAll(fics, source)
    

main()