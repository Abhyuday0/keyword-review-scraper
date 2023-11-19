from bs4 import BeautifulSoup
import re
import itertools
import pandas as pd
import requests

all_reviews= 0
url = "https://letterboxd.com/film/beijing-watermelon/"
url = url + "/reviews/by/activity/page/"
keyword = "cinema"

def parse_page(url = url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup

def collect_data(all_reviews = all_reviews, keyword = keyword):
    df_reviews = pd.DataFrame(columns=['URL', 'Rating', 'Review'])

    for review in enumerate(all_reviews):

        review_item = review[1]
        review_text = review_item.find('div', class_="body-text -prose collapsible-text").text
        if review_text.endswith('...'):   
            review_text = parse_page(full_review_url).text
        #filter
        relevance = keyword in review_text
        
        if relevance:
            # print(relevance)
            full_review_url = "https://letterboxd.com"+review_item.find('div', class_="body-text -prose collapsible-text")['data-full-text-url']
            
            
            try:
                rating = review_item.find('span', class_=lambda value: value and 'rated' in value).text
            except:
                rating = None
            
            review_data = [[full_review_url, rating, review_text]]
            df_row = pd.DataFrame(review_data, columns=['URL', 'Rating', 'Review'])
            df_reviews = pd.concat([df_reviews,df_row])
        # print(review_item.prettify())
        # break
    
    return df_reviews

def get_reviews(url = url, keyword = keyword):
    all_review_data = pd.DataFrame(columns=['URL', 'Rating', 'Review'])
    for i in itertools.count(start=1):
        page_url = url+str(i)
        page = parse_page(page_url)

        all_reviews = page.find_all('div', {'class':'film-detail-content'})
        if len(all_reviews) == 0:
            break

        review_data = collect_data(all_reviews, keyword)
        all_review_data = pd.concat([all_review_data, review_data])
        # print(i)
    return(all_review_data)

data = get_reviews(url= url, keyword = keyword)
print(data)
print('done')
