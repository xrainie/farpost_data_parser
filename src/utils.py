import requests
import bs4
from urllib.parse import urljoin

BASE_URL = 'https://www.farpost.ru'

class PromoData():
    def __init__(self) -> None:
        self.data = {}
        self.URL = 'https://www.farpost.ru/vladivostok/service/construction/guard/+/Системы+видеонаблюдения/'

    def load(self) -> dict:
        r = requests.get(self.URL, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'})
        data = self._get_main_page_data(request=r)
        return data

    def _get_main_page_data(self, request):
        """Загрузить все данные с главной страницы"""
        promo_urls = self._get_promo_urls(request=request)
        views = self._get_views(request=request)
        for url in promo_urls:
            title, author = self._get_promo_info(url=url)
            self.data[title] = {}
            self.data[title]['title'] = title
            self.data[title]['author'] = author
            self.data[title]['views'] = views.pop(0)
        return self.data

    def _get_views(self, request) -> list:
        """Взять первые 10 показателей просмотров с сайта"""
        views_data = []
        soup = bs4.BeautifulSoup(request.text, 'lxml')
        views = soup.find_all('span', class_='views')[:10]
        for view in views:
            views_data.append(view.text)
        return views_data

    def _get_promo_urls(self, request) -> list:
        urls = []
        content = request.text
        soup = bs4.BeautifulSoup(content, 'lxml')
        headlines = soup.find_all('a', class_='bulletinLink')[:10]
        for link in headlines:
            href = link.get('href')
            if href:
                full_url = urljoin(BASE_URL, href)
                urls.append(full_url)
        return urls

    def _get_promo_info(self, url) -> tuple:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'})
        soup = bs4.BeautifulSoup(r.text, 'lxml')
        title = soup.find('span', class_='inplace').text.strip()
        author = soup.find('span', class_='userNick').text.strip()
        return (title, author)