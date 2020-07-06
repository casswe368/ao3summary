"""Fic Class"""

from bs4 import BeautifulSoup
import re

class Fic:
    def __init__(self,text):
        self.soup=BeautifulSoup(text, 'html.parser')

    @property
    def title(self):
        #Title
        #Required field
        #<a href="/works/111111">Title</a>
        try:
            title_data = self.soup.h4.a.text
        except:
            title_data=''
        return title_data
        
    @property
    def worknumber(self):
        #Work Number
        #Required field
        #<a href="/works/111111">Title</a>
        try:
            worknumber_data=self.soup.h4.a['href'][7:]
        except:
            worknumber_data=''
        return worknumber_data
           
    @property
    def authors(self):
        #All authors of the work
        #Required field
        #<a rel="author" href="/users/username1/pseuds/username1">Username1</a>
        #<a rel="author" href="/users/username1/pseuds/username1">Username1</a>, <a rel="author" href="/users/username2/pseuds/pseudofusername2">PseudOfUsername2 (Username2)</a>, <a rel="author" href="/users/username3/pseuds/username3">Username3</a>
        authors_data = []
        for item in self.soup.h4.find_all('a', rel='author'):
            authors_data.append(item.text)
        if authors_data == []:
            authors_data = ['Anonymous']
        if self.deleted == 'Y':
            authors_data = []
        return authors_data       
        
    @property
    def giftees(self):
        #All giftees of the work
        #If there are no giftees, returns a blank list
        #for <a href="/users/username1/gifts">Username1</a>
        #for <a href="/users/username1/gifts">Username1</a>, <a href="/users/username2/gifts">Username2</a>
        giftees_data = []
        for item in self.soup.h4.find_all('a', href=re.compile('gifts')):
            giftees_data.append(item.text)
        return giftees_data
    
    @property
    def lockedStatus(self):
        #Is the work restricted to people logged in, aka "Locked"?
        #Default is Unlocked
        #<img alt="(Restricted)" title="Restricted" src="/images/lockblue.png" width="15" height="15"/>
        lockedStatus_data = 'Unlocked'
        if self.soup.find('img', alt='(Restricted)') != None:
            lockedStatus_data='Locked'
        return lockedStatus_data
       
    @property
    def fandoms(self):
        #Fandom tags, uses what the author wrote, not the canon tag
        #<h5 class="fandoms heading">
        #   <span class="landmark">Fandoms:</span>
        #   <a class="tag" href="/tags/Les%20Mis%C3%A9rables%20-%20All%20Media%20Types/works">Les Misérables - All Media Types</a>
        #   &nbsp;
        #</h5>
        fandoms_data = []
        try:
            for item in self.soup.h5.find_all('a', class_='tag'):
                fandoms_data.append(item.text)
        except:
            pass
        return fandoms_data     
    
    @property
    def requiredTags(self):
        #get the required tags block to pull rating, warnings, categories, wip
        #<ul class="required-tags">
        #   <li> <a class="help symbol question modal" title="Symbols key" aria-controls="#modal" href="/help/symbols-key.html"><span class="rating-teen rating" title="Teen And Up Audiences"><span class="text">Teen And Up Audiences</span></span></a></li>
        #   <li> <a class="help symbol question modal" title="Symbols key" aria-controls="#modal" href="/help/symbols-key.html"><span class="warning-no warnings" title="No Archive Warnings Apply"><span class="text">No Archive Warnings Apply</span></span></a></li>
        #   <li> <a class="help symbol question modal" title="Symbols key" aria-controls="#modal" href="/help/symbols-key.html"><span class="category-multi category" title="F/F, Gen"><span class="text">F/F, Gen</span></span></a></li>
        #   <li> <a class="help symbol question modal" title="Symbols key" aria-controls="#modal" href="/help/symbols-key.html"><span class="complete-no iswip" title="Work in Progress"><span class="text">Work in Progress</span></span></a></li>
        #</ul>
        try:
            requiredTags_data=self.soup.find('ul', class_='required-tags').find_all('span', class_='text')
        except:
            requiredTags_data=[]
        return requiredTags_data
    
    @property
    def rating(self):
        #Rating: General Audiences through Explicit
        #<li> <a class="help symbol question modal" title="Symbols key" aria-controls="#modal" href="/help/symbols-key.html"><span class="rating-teen rating" title="Teen And Up Audiences"><span class="text">Teen And Up Audiences</span></span></a></li>
        try:
            rating_data=self.requiredTags[0].text
        except:
            rating_data=''
        return rating_data
    
    @property
    def warnings(self):
        #Warnings
        #Can have multiple warnings
        #If no warnings are selected, warning category will be "No Archive Warnings Apply"
        #<li> <a class="help symbol question modal" title="Symbols key" aria-controls="#modal" href="/help/symbols-key.html"><span class="warning-no warnings" title="No Archive Warnings Apply"><span class="text">No Archive Warnings Apply</span></span></a></li>
        #<li> <a class="help symbol question modal" title="Symbols key" aria-controls="#modal" href="/help/symbols-key.html"><span class="warning-yes warnings" title="Graphic Depictions Of Violence, Rape/Non-Con"><span class="text">Graphic Depictions Of Violence, Rape/Non-Con</span></span></a></li>
        try:
            warnings_data=self.requiredTags[1].text.split(', ')
        except:
            warnings_data=[]
        return warnings_data
    
    @property
    def categories(self):
        #Categories: M/M, F/F, F/M, Gen, Other, Multi
        #Can have multiple categories
        #<li> <a class="help symbol question modal" title="Symbols key" aria-controls="#modal" href="/help/symbols-key.html"><span class="category-gen category" title="Gen"><span class="text">Gen</span></span></a></li>
        #<li> <a class="help symbol question modal" title="Symbols key" aria-controls="#modal" href="/help/symbols-key.html"><span class="category-multi category" title="F/M, M/M"><span class="text">F/M, M/M</span></span></a></li>
        try:
            categories_data=self.requiredTags[2].text.split(', ')
        except:
            categories_data=[]
        return categories_data
    
    @property
    def wip(self):
        #Is the work complete or a work in progress?
        #<li> <a class="help symbol question modal" title="Symbols key" aria-controls="#modal" href="/help/symbols-key.html"><span class="complete-no iswip" title="Work in Progress"><span class="text">Work in Progress</span></span></a></li>
        try:
            wip_data=self.requiredTags[3].text
        except:
            wip_data=''
        return wip_data
    
    @property
    def pubDate(self):
        #Date latest update was published
        #<p class="datetime">09 Dec 2015</p>
        try:
            pubDate_data=self.soup.find('p', class_='datetime').text
        except:
            pubDate_data=''
        return pubDate_data
    
    @property
    def relationships(self):
        #Relationship tags, uses what the author wrote, not the canon tag
        #Can have multiple relationships
        #If there are no relationships, returns a blank list
        #<li class='relationships'><a class="tag" href="/tags/Clark%20Kent*s*Bruce%20Wayne/works">Clark Kent/Bruce Wayne</a>
        #<li class='relationships'><a class="tag" href="/tags/Amilyn%20Holdo*s*Leia%20Organa/works">Amilyn Holdo/Leia Organa</a></li> <li class='relationships'><a class="tag" href="/tags/Poe%20Dameron*s*Leia%20Organa/works">Poe Dameron/Leia Organa</a></li> <li class='relationships'><a class="tag" href="/tags/Poe%20Dameron*s*Amilyn%20Holdo/works">Poe Dameron/Amilyn Holdo</a></li> <li class='relationships'><a class="tag" href="/tags/Amilyn%20Holdo*s*Poe%20Dameron*s*Leia%20Organa/works">Amilyn Holdo/Poe Dameron/Leia Organa</a></li>
        relationships_data = []
        for tag in self.soup.find_all('li', class_='relationships'):
            relationships_data.append(tag.a.text)
        return relationships_data
    
    @property
    def characters(self):
        #Character tags, uses what the author wrote, not the canon tag
        #Can have multiple relationships
        #If there are no characters, returns a blank list
        #<li class='characters'><a class="tag" href="/tags/Nicole%20(Dogs%20Lost%20In%20A%20Maze%20That%20Is%20Also%20In%20Egypt)/works">Nicole (Dogs Lost In A Maze That Is Also In Egypt)</a></li> <li class='characters'><a class="tag" href="/tags/Pat%20(Dogs%20Lost%20In%20A%20Maze%20That%20Is%20Also%20In%20Egypt)/works">Pat (Dogs Lost In A Maze That Is Also In Egypt)</a></li> <li class='characters'><a class="tag" href="/tags/Fletcher%20(Dogs%20Lost%20In%20A%20Maze%20That%20Is%20Also%20In%20Egypt)/works">Fletcher (Dogs Lost In A Maze That Is Also In Egypt)</a></li>
        characters_data = []
        for tag in self.soup.find_all('li', class_='characters'):
            characters_data.append(tag.a.text)
        return characters_data
    
    @property
    def freeformTags(self):
        #Freeform Tags
        #All tags not included in the above categories
        #Can have multiple freeform tags
        #If there are no tags, returns a blank list (but that would be odd)
        #<li class='freeforms'><a class="tag" href="/tags/Yuletide%202018/works">Yuletide 2018</a></li> <li class='freeforms'><a class="tag" href="/tags/Dogs/works">Dogs</a></li> <li class='freeforms'><a class="tag" href="/tags/good%20dogs/works">good dogs</a></li> <li class='freeforms'><a class="tag" href="/tags/Very%20Good%20Dogs/works">Very Good Dogs</a></li> <li class='freeforms'><a class="tag" href="/tags/excellent%20dogs/works">excellent dogs</a></li>
        freeformTags_data = []
        for tag in self.soup.find_all('li', class_='freeforms'):
            freeformTags_data.append(tag.a.text)
        return freeformTags_data
    
    @property
    def summary(self):
        #Summary
        #Could be blank, if blank the tag type will not be present at all
        #<blockquote class="userstuff summary">
        #   <p>We are playing with the bones! Grr-wag-wag-wag! Grr-wag-wag-wag! We are fighting each other but secretly it is playing because we are good dogs.</p>
        #</blockquote>
        summary_data = ''
        if self.soup.find('blockquote', class_='userstuff summary') != None:
            summary_data=self.soup.find('blockquote', class_='userstuff summary').text.replace("\t", " ")
        return summary_data
    
    @property
    def series(self):
        #Series that the work is part of
        #Could be blank, if blank the tag type will not be present at all
        #<ul class="series">
        #   <li>
        #       Part <strong>2</strong> of <a href="/series/1111111">Series1</a>
        #   </li>
        #</ul>
        series_data = ''
        if self.soup.find('ul', class_='series') != None:
            series_data=self.soup.find('ul', class_='series').a.text
        return series_data
    
    @property
    def language(self):
        #Language the work is written in
        #<dd class="language">English</dd>
        try:
            language_data=self.soup.find('dd', class_='language').text
        except:
            language_data=''
        return language_data
            
        
    @property
    def wordCount(self):
        #Word Count of the work
        #<dd class="words">14,313</dd>
        try:
            wordCount_data=self.soup.find('dd', class_='words').text
        except:
            wordCount_data=''
        return wordCount_data

    @property
    def chaptersWritten(self):
        #Number of chapters written so far
        #<dd class="chapters">2/?</dd>
        #<dd class="chapters">6/6</dd>
        #<dd class="chapters">1/1</dd>
        try:
            chaptersWritten_data=self.soup.find('dd', class_='chapters').text.split('/')[0]
        except:
            chaptersWritten_data=''
        return chaptersWritten_data            

    @property
    def chaptersTotal(self):
        #Number of total chapters (including planned)
        #<dd class="chapters">2/?</dd>
        #<dd class="chapters">6/6</dd>
        #<dd class="chapters">1/1</dd>
        try:
            chaptersTotal_data=self.soup.find('dd', class_='chapters').text.split('/')[1]
        except:
            chaptersTotal_data=''
        return chaptersTotal_data 

    @property
    def collections(self):
        #Number of collections the work is part of
        #Could be blank, if blank the tag type will not be present at all
        #<dd class="collections"><a href="/works/22551325/collections">2</a></dd>
        collections_data = '0'
        if self.soup.find('dd', class_='collections') != None:
            collections_data=self.soup.find('dd', class_='collections').text
        return collections_data
    
    @property
    def comments(self):
        #Number of comments on the work
        #Could be blank, if blank the tag type will not be present at all
        #dd class="comments"><a href="/works/22551325?show_comments=true#comments">247</a></dd>
        comments_data = '0'
        if self.soup.find('dd', class_='comments') != None:
            comments_data=self.soup.find('dd', class_='comments').text
        return comments_data

    @property
    def kudos(self):
        #Number of kudos on the work
        #Could be blank, if blank the tag type will not be present at all
        #<dd class="kudos"><a href="/works/22551325#comments">6043</a></dd>
        kudos_data = '0'
        if self.soup.find('dd', class_='kudos') != None:
            kudos_data=self.soup.find('dd', class_='kudos').text
        return kudos_data      

    @property
    def bookmarks(self):
        #Number of kudos on the work
        #Could be blank, if blank the tag type will not be present at all
        #<dd class="kudos"><a href="/works/22551325#comments">6043</a></dd>
        bookmarks_data = '0'
        if self.soup.find('dd', class_='bookmarks') != None:
            bookmarks_data=self.soup.find('dd', class_='bookmarks').text
        return bookmarks_data

    @property
    def hits(self):
        #Number of hits on the work
        #<dd class="hits">32523</dd>
        hits_data = '0'
        if self.soup.find('dd', class_='bookmarks') != None:
            hits_data=self.soup.find('dd', class_='hits').text
        return hits_data

    @property
    def historyInfo(self):
        #get the history block to pull visited date, update status, visit info, and marked for later status
        #<h4 class="viewed heading">
        #   <span>Last visited:</span> 05 Nov 2019
        #       (Latest version.)
        #       Visited 11 times
        #       (Marked for Later.)
        #</h4>
        try:
            historyInfo_data=self.soup.find('h4', class_='viewed heading').span.next_sibling
        except:
            historyInfo_data=''
        return historyInfo_data

    @property
    def visitedDate(self):
        #Last Date the work was viewed by the user
        #<span>Last visited:</span> 05 Nov 2019
        if self.deleted == 'Y':
            visitedDate_data=self.soup.h4.text[-12:-1]
        else:
            visitedDate_data=self.historyInfo.split('(')[0].strip()
        return visitedDate_data
    
    @property
    def updateStatus(self):
        #The level of updates made since the user last viewed the work
        #(Latest version.)
        #(Minor edits made since then.)
        #(Update available.)
        if self.historyInfo=='':
            updateStatus_data=''
        else:
            statusStart = self.historyInfo.find('(')+1
            statusEnd = self.historyInfo.find(')')-1
            updateStatus_data=self.historyInfo[statusStart:statusEnd]
        return updateStatus_data
    
    @property
    def visitInfo(self):
        #get the visit block to pull visit info and marked for later status
        #<h4 class="viewed heading">
        #   <span>Last visited:</span> 05 Nov 2019
        #       (Latest version.)
        #       Visited 11 times
        #       (Marked for Later.)
        #</h4>
        if self.historyInfo=='':
            visitInfo_data=''
        else:
            visitInfo_data=self.historyInfo.split('Visited ')[1] 
        return visitInfo_data      
    
    @property
    def visitCount(self):
        #The number of times the user has viewed the work
        #Visited once
        #Visited 2 times
        if self.historyInfo=='':
            visitCount_data=''
        else:
            if 'once' in  self.visitInfo:
                visitCount_data = '1'
            else:
                if "(" in self.visitInfo:
                    visitCount_data = self.visitInfo.split("(")[0][:-5]
                else:
                    visitCount_data = self.visitInfo[:-6]
        return visitCount_data
    
    @property
    def later(self):
        #Is the work marked for later?
        #Could be blank, if blank the tag type will not be present at all
        #(Marked for Later.)
        later_data='N'
        if "(" in self.visitInfo:
            later_data='Y'
        return later_data

    @property
    def deleted(self):
        #Is this a deleted work?
        #<li class="deleted reading work blurb group" role="article">
        #(Deleted work, last visited 26 Nov 2019)
        deleted_data='N'
        if self.soup.find('li', class_="deleted reading work blurb group") != None:
            deleted_data='Y'
        return deleted_data    


        
    
# =============================================================================
# #For Testing
#       
# def main():
# 
#     """
#     file = open('sampleDeletedFic.txt', 'r', encoding='utf-8')
#     lst = file.readlines()
#     file.close()
#     
#     lines=""
#     for line in lst:
#         line=line.replace('|','/')
#         line=line.strip()
#         if line == '':
#             continue
#         lines+=line
#         print(line)
#         
#     print(lines)"""
#     
#     
#     sampleFic="""<!--title, author, fandom--><div class="header module"><h4 class="heading"><a href="/works/111111">This is a Title</a>by<!-- do not cache --><a rel="author" href="/users/username1/pseuds/username1">Username1</a>for <a href="/users/username2/gifts">Username2</a></h4><h5 class="fandoms heading"><span class="landmark">Fandoms:</span><a class="tag" href="/tags/Community/works">Community</a>&nbsp;</h5><!--required tags--><ul class="required-tags"><li> <a class="help symbol question modal" title="Symbols key" aria-controls="#modal" href="/help/symbols-key.html"><span class="rating-general-audience rating" title="General Audiences"><span class="text">General Audiences</span></span></a></li><li> <a class="help symbol question modal" title="Symbols key" aria-controls="#modal" href="/help/symbols-key.html"><span class="warning-no warnings" title="No Archive Warnings Apply"><span class="text">No Archive Warnings Apply</span></span></a></li><li> <a class="help symbol question modal" title="Symbols key" aria-controls="#modal" href="/help/symbols-key.html"><span class="category-slash category" title="M/M"><span class="text">M/M</span></span></a></li><li> <a class="help symbol question modal" title="Symbols key" aria-controls="#modal" href="/help/symbols-key.html"><span class="complete-yes iswip" title="Complete Work"><span class="text">Complete Work</span></span></a></li></ul><p class="datetime">01 Jan 1951</p></div><!--warnings again, cast, freeform tags--><h6 class="landmark heading">Tags</h6><ul class="tags commas"><li class='warnings'><strong><a class="tag" href="/tags/No%20Archive%20Warnings%20Apply/works">No Archive Warnings Apply</a></strong></li><li class='relationships'><a class="tag" href="/tags/Troy%20Barnes*s*Abed%20Nadir/works">Troy Barnes/Abed Nadir</a></li><li class='characters'><a class="tag" href="/tags/Troy%20Barnes/works">Troy Barnes</a></li> <li class='characters'><a class="tag" href="/tags/Abed%20Nadir/works">Abed Nadir</a></li> <li class='characters'><a class="tag" href="/tags/Annie%20Edison/works">Annie Edison</a></li> <li class='characters'><a class="tag" href="/tags/Jeff%20Winger/works">Jeff Winger</a></li> <li class='characters'><a class="tag" href="/tags/Pierce%20Hawthorne/works">Pierce Hawthorne</a></li> <li class='characters'><a class="tag" href="/tags/Shirley%20Bennett/works">Shirley Bennett</a></li> <li class='characters'><a class="tag" href="/tags/Britta%20Perry/works">Britta Perry</a></li><li class='freeforms'><a class="tag" href="/tags/Chromatic%20Yuletide/works">Chromatic Yuletide</a></li></ul><!--summary--><h6 class="landmark heading">Summary</h6><blockquote class="userstuff summary"><p>This is a summary of the work</p></blockquote><!--stats--><dl class="stats"><dt class="language">Language:</dt><dd class="language">English</dd><dt class="words">Words:</dt><dd class="words">6,166</dd><dt class="chapters">Chapters:</dt><dd class="chapters">1/1</dd><dt class="collections">Collections:</dt><dd class="collections"><a href="/works/302238/collections">1</a></dd><dt class="comments">Comments:</dt><dd class="comments"><a href="/works/111111?show_comments=true#comments">365</a></dd><dt class="kudos">Kudos:</dt><dd class="kudos"><a href="/works/111111#comments">999</a></dd><dt class="bookmarks">Bookmarks:</dt><dd class="bookmarks"><a href="/works/111111/bookmarks">1951</a></dd><dt class="hits">Hits:</dt><dd class="hits">12345</dd></dl><div class="user module group"><h4 class="viewed heading"><span>Last visited:</span> 25 May 2020(Latest version.)Visited once</h4><ul class="actions" role="menu"><li>"""
#     sampleDeletedFic="""<li class="deleted reading work blurb group" role="article"><div class="user module group"><h4 class="viewed heading">(Deleted work, last visited 26 Nov 2019)</h4><ul class="actions" role="menu"><li><li class="deleted reading work blurb group" role="article"><div class="user module group"><h4 class="viewed heading">(Deleted work, last visited 26 Nov 2019)</h4><ul class="actions" role="menu"><li>"""
#     fic=Fic(sampleFic)
#     delfic=Fic(sampleDeletedFic)
# 
#     
#     
#     print(fic.title, fic.worknumber, fic.authors, fic.giftees, fic.lockedStatus, fic.fandoms, fic.requiredTags)
#     print(fic.rating, fic.warnings, fic.categories, fic.wip, fic.pubDate)
#     print(fic.relationships, fic.characters, fic.freeformTags)
#     print(fic.summary, fic.series, fic.language, fic.wordCount, fic.chaptersWritten, fic.chaptersTotal)
#     print(fic.collections, fic.comments, fic.kudos, fic.bookmarks, fic.hits)
#     print(fic.visitedDate, fic.updateStatus, fic.visitCount, fic.later,fic.deleted)
# 
# 
#     
#     print(delfic.title, delfic.worknumber, delfic.authors, delfic.giftees, delfic.lockedStatus, delfic.fandoms, delfic.requiredTags)
#     print(delfic.rating, delfic.warnings, delfic.categories, delfic.wip, delfic.pubDate)
#     print(delfic.relationships, delfic.characters, delfic.freeformTags)
#     print(delfic.summary, delfic.series, delfic.language, delfic.wordCount, delfic.chaptersWritten, delfic.chaptersTotal)
#     print(delfic.collections, delfic.comments, delfic.kudos, delfic.bookmarks, delfic.hits)
#     print(delfic.visitedDate, delfic.updateStatus, delfic.visitCount, delfic.later,delfic.deleted)
# 
#     
# main()
# =============================================================================
