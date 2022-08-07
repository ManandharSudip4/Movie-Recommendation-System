import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import os

def get_all_titles(soup):
    result_topics=[]
    all_topics=soup.find_all('h3',{"class":"lister-item-header"})
    for topic in all_topics:
        topic = str(topic.find('a'))
        topic = topic.replace("<","=")
        topic = topic.replace(">","=")
        topic = topic.split('=')
        topic = topic[int(len(topic)/2)]
        result_topics.append(topic)
    print("GG Titles: ", result_topics)
    return result_topics

def post_process(genres):
    post_process_genres = []
    for i in genres:
        i = i.replace('\n','')
        i = i.replace(" ","")
        post_process_genres.append(i)
    print("GG Genres: ", post_process_genres)
    return post_process_genres
 
def check_repeated_comma(x):
    list_x = x.split(',')
    if len(list_x) == 3:
        return x 
    else:
        return np.nan 

def get_all_genre(soup):
    result_genres=[]
    all_genres=soup.find_all('p',{"class":"text-muted"})
    print("GG1")
    print(all_genres)
    print("GG2")
    for genre in all_genres:
        genre = str(genre.find_all('span',{"class":"genre"}))
        if genre=='[]':
            pass
        else:
            genre = genre.replace("<","=")
            genre = genre.replace(">","=")
            genre = genre.split('=')
            genre = genre[int(len(genre)/2)]
            result_genres.append(genre)
    print("This is it",result_genres)
    return result_genres


def data_set(url):
    dataset = pd.DataFrame(columns=["Movie","Primary Genre","Secondary Genre","Tertiary Genre"])

    # Initially get the page from the url and from the content extract all the things properly so page is extracted
    page=requests.get(url)
 
    # Soup is created where all the content is parsed as html format for so it can be extracted as seen in webpages
    soup = BeautifulSoup(page.content,'html.parser')
    title = get_all_titles(soup)
    print('Titles Scraped')
    print(title)
    genres = get_all_genre(soup)
    print('Genres Scraped')
    genres = post_process(genres)
    print('Genres processed')
    dataset["Movie"] = pd.Series(title)
    dataset["Primary Genre"] = pd.Series(genres)
    dataset["Primary Genre"] = dataset["Primary Genre"].apply(check_repeated_comma)
    dataset["Secondary Genre"] = dataset["Secondary Genre"].fillna('To Be filled')
    dataset["Tertiary Genre"] = dataset["Tertiary Genre"].fillna('To be filled')
    dataset = dataset.loc[dataset['Primary Genre'] != np.NaN]
    dataset = dataset.dropna(how="any")
    dataset[["Primary Genre","Secondary Genre","Tertiary Genre"]] = dataset["Primary Genre"].str.split(',',expand=True)
    print(dataset.head())
    dataset.to_csv("Dataset.csv",mode='a',header=False)
    print("Dataset created successfully")
 
# main
import os
os.system('clear')
print("IMDB Scrapper")
number_of_pages = int(input("Number of pages to scrap: "))
count = 1
for i in range(number_of_pages):
    url=f'https://www.imdb.com/search/title/?genres=adventure&start={count}&ref_=adv_nxt'
    # print(url)
    data_set(url)
    count+=50