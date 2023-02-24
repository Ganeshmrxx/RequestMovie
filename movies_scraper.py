import requests
from bs4 import BeautifulSoup


url_list = {}
api_key = "ENTER YOUR API KEY HERE"


def search_movies(query):
    movies_list = []
    movies_details = {}
    website = BeautifulSoup(requests.get(f"https://ww1.7movierulz.win/search_movies?s={query.replace(' ', '+')}").text, "html.parser")
    website2 = BeautifulSoup(requests.get(f"https://bolly4u.vip/?s={query.replace(' ', '+')}").text, "html.parser")
    movies2 = website2.find_all('div',{'class': 'w-5/12'})
    mov = website.find('div', {'class': 'content home_style'})
    movies = mov.find_all('div', {'class': 'boxed film'}) 
    try:
        check = mov.find("h2").text
    except:
        for movie in movies:
            if movie:
                movies_details["id"] = f"link{movies.index(movie)}"
                movies_details["title"] = movie.find("p").text
                url_list[movies_details["id"]] = movie.find('a')['href']
            movies_list.append(movies_details)
            movies_details = {}
    for movie2 in movies2:
        if movie2:
            movies_details["id"] = f"link2{movies2.index(movie2)}"
            mo2 =  mo2 = movie2.find('div',{'class': 'mt-2'}).text
            re2 = mo2.replace("\n", "")
            movies_details["title"] = re2
            url_list[movies_details["id"]] = movie2.find('a')['href']
        movies_list.append(movies_details)
        movies_details = {}        
    return movies_list


def search_moviess(query):
    movies_list = []
    movies_details = {}
    website = BeautifulSoup(requests.get(f"https://ww1.7movierulz.win/search_movies?s={query.replace(' ', '+')}").text, "html.parser")
    mov3 = website.find('div', {'class': 'content home_style'})
    movies3 = mov3.find_all('div', {'class': 'boxed film'}) 
    for movie3 in movies3:
        if movie3:
            movies_details["id"] = f"link{movies3.index(movie3)}"
            movies_details["title"] = movie3.find("p").text
            url_list[movies_details["id"]] = movie3.find('a')['href']
        movies_list.append(movies_details)
        movies_details = {}
    return movies_list


def get_movie(query):
    movie_details = {}
    s1 = "7movierulz"
    s2 = "bolly4u"
    movie_page_link = BeautifulSoup(requests.get(f"{url_list[query]}").text, "html.parser")
    chekcurl = url_list[query]
    if s1 in chekcurl:
        if movie_page_link:
            title = movie_page_link.find("div", {'class': 'title'}).h2.text
            movie_details["title"] = title
            im = movie_page_link.find("div", {'class': 'entry-content'})
            img = im.find("img")['src']
            movie_details["img"] = img
            links = movie_page_link.find_all("a", {'rel': 'nofollow'})
            final_links = {}
            textname = "With Ad Download and Watch (Link- "
            number = 0
            for i in links:
                number = number+1
                dood = "dood"
                watchsb = "watchsb"
                filemoon = "filemoon"
                noad = "Without Ad Watch and Download (Link- "
                end = ")"
                if i['href'].startswith('https://'):
                    if dood in i['href']: 
                       final_links[f"{noad + str(number) + end}"] = i['href']
                    elif watchsb in i['href']:   
                       final_links[f"{noad + str(number) + end}"] = i['href']
                    elif filemoon in i['href']:   
                       final_links[f"{noad + str(number) + end}"] = i['href']   
                    else:
                       final_links[f"{textname+ str(number) + end}"] = i['href']
            movie_details["links"] = final_links
    elif s2 in chekcurl:
        if movie_page_link:
            tit = movie_page_link.find("span", {'class': 'w-full'}).text
            title = tit.replace("\n", "")
            movie_details["title"] = title
            im = movie_page_link.find("div", {'class': 'post-body'})
            img = im.find("img")['src']
            movie_details["img"] = img
            links = movie_page_link.find_all("a", {'rel': 'nofollow'})
            final_links = {}
            textname = "(Link- "
            number = 0
            for i in links:
                number += 1
                re = "replytocom"
                end = ")"
                if i['href'].startswith('https://'):
                    if re in i['href']: 
                       url = "0"
                    else:
                       final_links[f"{i.text}"] = i['href'] 
            movie_details["links"] = final_links         
    return movie_details
