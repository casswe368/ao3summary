file = open('raw_history_html_first_7_pages', 'r')
lst = file.readlines()
file.close()

fics=list()
fic=list()

for line in lst:
    line = line.strip()
    if line == '':
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

#fic0 is the header information

print('start of fic 1')

fic1=fics[1]

print(*fic1, sep='\n')

titleline = ''


'''
title line looks like:
<a href="/works/3880675">Selected Citations from Motions in Limine Filed in U.S. v. McCormick (C.D. Cal. 2019) (unpublishable)</a>
'''

#set up strings
titleline = ''
authorline = ''


print("get lines")
for line in fics[2]:

    #get lines
    if line.startswith('<a href=\"/works/') == True:
        titleline = line
        print(titleline)
    if line.startswith('<a rel="author" href="') == True:
        authorline = line
        print(authorline)
        
#extract info
#find the start of title
starttitle=titleline.find('\">') + 2
worknumber=titleline[16:starttitle-2]
print(worknumber)
title=titleline[starttitle:-4]
print(title)
    
    
looking=fics[2].index("<!-- do not cache -->")
print(looking)
