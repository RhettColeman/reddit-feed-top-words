import requests
from bs4 import BeautifulSoup
import pprint

res = requests.get('https://news.ycombinator.com/news')
soup = BeautifulSoup(res.text, 'html.parser') #parser converts the HTML from text into an object

links = (soup.select('.storylink'))
subtext = (soup.select('.subtext'))

#To scape second page
res2 = requests.get('https://news.ycombinator.com/news?p=2')
soup2 = BeautifulSoup(res2.text, 'html.parser')
links2 = (soup2.select('.storylink'))
subtext2 = (soup2.select('.subtext'))

mega_links = links + links2
mega_subtext = subtext + subtext2

def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key= lambda k:k['votes'], reverse=True) #Sorts the output by dictionary key 'votes'

def create_custom(links,subtext):
    hn = []
    for idx, item in enumerate(links):
        title = links[idx].getText()
        href = links[idx].get('href', None) #None is default if no url is present
        vote = subtext[idx].select('.score')
        if len(vote): #Will only run if 'score' is present in the subtext
            points = int(vote[0].getText().replace(' points', '')) #Takes the word points off so the numbers can be an int
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hn)


#main function
if __name__ == '__main__':
    pprint.pprint(create_custom(mega_links,mega_subtext))


