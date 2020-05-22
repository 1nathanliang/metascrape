'''
Created on May 21, 2020

@author: Nathan Liang
'''

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import csv
    

def scrape(query, cap):
    '''
    Webscraping from PhilPapers
    and writing to csv
    '''
    finalList = []
    
    counter = 0
    while counter < cap + 1:
        my_URL = 'https://philpapers.org/asearch.pl?hideAbstracts=&onlineOnly=&sort=relevance&categorizerOn=&showCategories=on&langFilter=&searchStr='+query+'&publishedOnly=&freeOnly=&sqc=&filterByAreas=&newWindow=on&proOnly=on&filterMode=keywords&format=html&start='+str(counter)+'&limit='+str(cap)+'&jlist=&ap_c1=&ap_c2='        
        uClient = uReq(my_URL)
        page_html = uClient.read()
        uClient.close()
        page_soup = soup(page_html, 'html.parser')
        articles = page_soup.findAll('li', {'class': 'entry'})
        for article in articles:
            
            # Initialize entry for each article
            each_article = []
            
            # Find article title
            title = article.findAll('span', {'class':'articleTitle recTitle'})       
            if title[0].text[-1] in '.':
                each_article.append(title[0].text[:-1])
            else:
                each_article.append(title[0].text)
            
            # Find article authors
            authors = article.findAll('a', {'class':'discreet'})       
            authorString = ''
            for author in authors:
                name = author.findAll('span',{'class':'name'})
                authorString += name[0].text + ', '
            authorString = authorString[:-2]
            each_article.append(authorString)
                            
            # Find article year
            year = article.findAll('span',{'class':'pubYear'})
            each_article.append(year[0].text)
            
            # Find article journal
            journal = article.findAll('em',{'class':'pubName'})
            try: 
                findYear = journal[0].text
            except:
                findYear = 'No Journal'
            each_article.append(findYear)
            
            # Find article volume
#             volume = article.findAll('span',{'class':'pubInfo'})
     
            # Find article issue
            
            # Find article page
            
            # Add each entry to final list
            finalList.append(each_article)

        counter += 50 # 50 results per page

    filename = query + '_' + str(cap) + '_output.csv'
    with open(filename, 'w+', encoding="utf-8", newline='') as csvfile:
        fields = ['title','author','year','journal']
        filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(fields)
        for idx in range(len(finalList)):
            filewriter.writerow(finalList[idx])

if __name__ == '__main__':
    scrape('causal+norm', 100)
