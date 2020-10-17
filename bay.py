import requests
import json
from bs4 import BeautifulSoup as bs
from datetime import datetime, timezone
from Models.statement import Statement


class BAY(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.session()
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
        self.content_type = 'application/x-www-form-urlencoded'
        self.url = 'https://www.krungsribizonline.com'

    def get_statement_lst(self):
        data = self.__nav_login()
        referer = self.__login(data)
        href = self.__getMainMenu(referer)
        referer2 = self.__nav_pageCase(referer, href)
        statement_lst = self.__get_statement_lst(referer2)

        return statement_lst

    def __nav_login(self):
        HEADER = {
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.krungsribizonline.com',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': self.user_agent
        }

        soup = bs(self.session.get(
            self.url+'/BAY.KOL.Corp.WebSite/Common/Login.aspx', headers=HEADER).content, 'html.parser')

        __LASTFOCUS = soup.find("input", {"name": "__LASTFOCUS"}).get('value')
        __VIEWSTATE = soup.find("input", {"name": "__VIEWSTATE"}).get('value')
        __EVENTARGUMENT = soup.find(
            "input", {"name": "__EVENTARGUMENT"}).get('value')
        __VIEWSTATEGENERATOR = soup.find(
            "input", {"name": "__VIEWSTATEGENERATOR"}).get('value')
        __VIEWSTATEENCRYPTED = soup.find(
            "input", {"name": "__VIEWSTATEENCRYPTED"}).get('value')
        __PREVIOUSPAGE = soup.find(
            "input", {"name": "__PREVIOUSPAGE"}).get('value')
        __EVENTVALIDATION = soup.find(
            "input", {"name": "__EVENTVALIDATION"}).get('value')

        return {
            '__LASTFOCUS': __LASTFOCUS,
            '__VIEWSTATE': __VIEWSTATE,
            '__EVENTARGUMENT': __EVENTARGUMENT,
            '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
            '__VIEWSTATEENCRYPTED': __VIEWSTATEENCRYPTED,
            '__PREVIOUSPAGE': __PREVIOUSPAGE,
            '__EVENTVALIDATION': __EVENTVALIDATION
        }

    def __login(self, data):
        HEADER = {
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': self.content_type,
            'Host': 'www.krungsribizonline.com',
            'Origin': self.url,
            'Referer': self.url+'/BAY.KOL.Corp.WebSite/Common/Login.aspx',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': self.user_agent
        }

        payload = {
            '__LASTFOCUS': data['__LASTFOCUS'],
            '__EVENTTARGET': 'ctl00$cphLoginBox$imgLogin',
            '__EVENTARGUMENT': data['__EVENTARGUMENT'],
            '__VIEWSTATE': data['__VIEWSTATE'],
            '__VIEWSTATEGENERATOR': data['__VIEWSTATEGENERATOR'],
            '__VIEWSTATEENCRYPTED': data['__VIEWSTATEENCRYPTED'],
            '__PREVIOUSPAGE': data['__PREVIOUSPAGE'],
            '__EVENTVALIDATION': data['__EVENTVALIDATION'],
            'ctl00$cphLoginBox$hddLanguage': 'TH',
            'ctl00$cphLoginBox$txtUsernameSME': self.username,
            'ctl00$cphLoginBox$hdPassword': self.password
        }

        res = self.session.post(
            self.url+'/BAY.KOL.Corp.WebSite/Common/Login.aspx', headers=HEADER, data=payload)
        referer = res.url

        return referer

    def __getMainMenu(self, referer):
        HEADER = {
            'Connection': 'keep-alive',
            'Content-Type': 'application/json; charset=UTF-8',
            'Host': 'www.krungsribizonline.com',
            'Origin': self.url,
            'Referer': referer,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': self.user_agent,
            'X-Requested-With': 'XMLHttpRequest'
        }

        res = self.session.post(
            self.url+'/BAY.KOL.Corp.WebSite/Common/Service/CustomerService.aspx/GetMainMenu', headers=HEADER, json={})
        text = res.json()['d']
        soup = bs(text, 'html.parser')
        href = soup.find_all("a", {"class": "menu_link_progress"})[
            4].get('href')

        return href

    def __nav_pageCase(self, referer, href):
        HEADER = {
            'Connection': 'keep-alive',
            'Host': 'www.krungsribizonline.com',
            'Referer': referer,
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': self.user_agent
        }

        res = self.session.get(self.url+href, headers=HEADER)
        referer = res.url

        return referer

    def __get_statement_lst(self, referer):
        HEADER = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,th-TH;q=0.8,th;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json; charset=UTF-8',
            'Host': 'www.krungsribizonline.com',
            'Origin': self.url,
            'Referer': referer,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': self.user_agent,
            'X-Requested-With': 'XMLHttpRequest'
        }

        payload = {'pageIndex': 1}

        res = self.session.post(
            self.url+'/BAY.KOL.Corp.WebSite/Pages/MyAccount.aspx/GetStatementToday', headers=HEADER, json=payload)
        json_text = res.json()['d']
        statement = json.loads(json_text)['Statement']
        qry_statement = filter(lambda st: st['AmountType'] == 1, statement)

        statement_lst = []

        for st in qry_statement:
            date_string = str(st['TranDateTime'])
            date = datetime.strptime(
                date_string, "%Y-%m-%dT%H:%M:%S").astimezone(timezone.utc)

            amount = st['TranAmount']
            number = st['TranDetailTH'].split()[1]

            statement = Statement(date, amount, number)
            statement_lst.append(statement.__dict__)

        return statement_lst
