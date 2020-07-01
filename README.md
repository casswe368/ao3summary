# ao3summary
Python script to pull metadata from ao3 browsing pages (history, bookmarks, tags)


# inspiration
I wanted to specifically pull the information of my history since ao3 doesn't let you filter at all on works in your history, to find things like reading amount over time, fandoms I've passed through over the years, the author I've read more than anyone else.

I began writing this from scratch and had most of a first version created when someone pointed me toward alexwlchan's project, ao3, an unofficial API which pulls metadata from the work page of a specific ao3 work. Based on the things I learned from their project (first and most importantly the existance of BeautifulSoup, which I was trying to do manually), I rewrote the code twice and each time it got similar to their code because they made choices on how to do it that made way more sense than mine.

The reason I didn't switch to using their API to get the data is that I wanted to pull from the browsing page that has the summary of the works instead of from the work page itself, that way I would be able to see information like number of times I visited the work, if it is marked from later, etc.

The other benefit of pulling from the browsing page is that since I don't need any information from the work page itself, I have to load 20 times fewer pages. Example, if my bookmarks are 10 pages long, I would have to load 10 pages total instead of 200 pages for the 200 works (20 works per page).

I'm capturing all the information available to me so that I can export it all and analyze it in R.
