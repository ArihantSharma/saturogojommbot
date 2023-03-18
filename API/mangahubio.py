import requests
from bs4 import BeautifulSoup


class mangahubio:
    def __init__(self, query, mangaid, chapternum):
        self.query = query
        self.mangaid = mangaid
        self.chapternum = chapternum

    # returns list of tuples cotaining name of manga and its id [(name1, id1), (name2, id2)]
    def get_search_results(query):
        try:
            url = f"http://mangahub.io/search?q={query}"
            response = requests.get(url)
            response_html = response.text
            soup = BeautifulSoup(response_html, "lxml")
            mangas = soup.findAll("div", class_="media-manga media")
            res_search_list = []
            for manga in mangas:
                manganame = manga.a("a")
                link = manga.a["href"]
                split = link.split("/")
                split2 = split[-1].split("?")
                mangaid = split2[0]
                result = (manganame, mangaid)
                res_search_list.append(result)
            if not res_search_list:
                return "Nothing Found"
            return res_search_list
        except requests.exceptions.ConnectionError:
            return "Check the host's network Connection"

    # returns list of [Name of manga, Display-image link, list of genres, latest chapter number]
    def get_manga_details(mangaid):
        try:
            url = f"http://mangahub.io/manga/{mangaid}"
            response = requests.get(url)
            response_html = response.text
            soup = BeautifulSoup(response_html, "lxml")
            manga_title = soup.find("img", class_="img-responsive manga-thumb", alt=True)
            image = soup.find("img", class_="img-responsive manga-thumb")
            image_link = image["src"]
            genre_list = []
            genres = soup.find("p", class_="_3Czbn").findAll("a")
            for genre in genres:
                genre_list.append(genre.text)
            latest_chap = soup.find("div", class_="_2wcqV").find("a")
            latest_chapter = latest_chap.text
            latest_chapter_split = latest_chapter.split(" ")
            last_chapter = latest_chapter_split[-1]
            return [manga_title.text, image_link, genre_list[:-2], last_chapter]
        except AttributeError:
            return "Invalid Mangaid"
        except requests.exceptions.ConnectionError:
            return "Check the host's network Connection"

    # returns list of image links of pages of full chapter [imglink1, imglink2, full chapter]
    def get_manga_chapter(mangaid, chapternum):
        try:
            url = f"https://mangahub.io/{mangaid}/chapter-{chapternum}"
            response = requests.get(url)
            response_html = response.text
            soup = BeautifulSoup(response_html, "lxml")
            chapter_pages = soup.find_all("img", id="PB0mN")
            pages = chapter_pages.split('src')
            return pages
        except AttributeError:
            return "Invalid Mangaid or chapter number"
        except requests.exceptions.ConnectionError:
            return "Check the host's network Connection"
