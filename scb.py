import requests
import random
from bs4 import BeautifulSoup as bs
from datetime import datetime, timezone
from Models.statement import Statement


class SCB():
    def __init__(self):
        self.session = requests.session()
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
        self.content_type = 'application/x-www-form-urlencoded'
        self.url = 'https://www.scbeasy.com/'
        self.header = {
            'User-Agent': self.user_agent,
            'Content-Type': self.content_type,
            'Origin': self.url
        }

    def get_statement_lst(self, username, password):
        SESSIONEASY = self.__login(username, password)
        SESSIONEASY = self.__firstpage(SESSIONEASY)
        SESSIONEASY = self.__cust_csent(SESSIONEASY)
        SESSIONEASY = self.__firstpage_2(SESSIONEASY)
        VIEWSTATE, VIEWSTATEGENERATOR = self.__acc_mpg(SESSIONEASY)
        SESSIONEASY = self.__acc_mpg_2(
            SESSIONEASY, VIEWSTATE, VIEWSTATEGENERATOR)
        VIEWSTATE, ctl00, VIEWSTATEGENERATOR = self.__acc_bnk_bln(SESSIONEASY)
        SESSIONEASY = self.__acc_bnk_bln_2(
            SESSIONEASY, VIEWSTATE, ctl00, VIEWSTATEGENERATOR)
        statement_lst = self.__get_statement_lst(SESSIONEASY)

        return statement_lst

    def __login(self, username, password):
        self.header['Referer'] = self.url + 'v1.4/site/presignon/index.asp'
        x = random.randint(10, 50)
        y = random.randint(10, 50)
        payload = {
            'LANG': 'T',
            'LOGIN': username,
            'PASSWD': password,
            'lgin.x': x,
            'lgin.y': y
        }
        res = self.session.post(
            self.url + 'online/easynet/page/lgn/login.aspx', headers=self.header, data=payload)
        soup = bs(res.content, 'html.parser')
        SESSIONEASY = soup.find("input", {"name": "SESSIONEASY"}).get('value')

        return SESSIONEASY

    def __firstpage(self, SESSIONEASY):
        self.header['Referer'] = self.url + \
            'online/easynet/page/lgn/login.aspx'
        payload = {
            'SESSIONEASY': SESSIONEASY
        }
        res = self.session.post(
            self.url + 'online/easynet/page/firstpage.aspx', headers=self.header, data=payload)
        soup = bs(res.content, 'html.parser')
        SESSIONEASY = soup.find("input", {"name": "SESSIONEASY"}).get('value')

        return SESSIONEASY

    def __cust_csent(self, SESSIONEASY):
        self.header['Referer'] = self.url + \
            'online/easynet/page/firstpage.aspx'
        payload = {
            'SESSIONEASY': SESSIONEASY
        }
        res = self.session.post(
            self.url + 'online/easynet/page/cust_csent.aspx', headers=self.header, data=payload)
        soup = bs(res.content, 'html.parser')
        SESSIONEASY = soup.find("input", {"name": "SESSIONEASY"}).get('value')

        return SESSIONEASY

    def __firstpage_2(self, SESSIONEASY):
        self.header['Referer'] = self.url + \
            'online/easynet/page/cust_csent.aspx'
        payload = {
            'SESSIONEASY': SESSIONEASY
        }
        res = self.session.post(
            self.url + 'online/easynet/page/firstpage.aspx', headers=self.header, data=payload)
        soup = bs(res.content, 'html.parser')
        word = str(soup.find_all('script')[3].contents)
        SESSIONEASY = word.split("new Array(\\\'")[2].split("\\\')")[0]

        return SESSIONEASY

    def __acc_mpg(self, SESSIONEASY):
        self.header['Referer'] = self.url + \
            'online/easynet/page/firstpage.aspx'
        payload = {
            'SESSIONEASY': SESSIONEASY,
            'undefined': 'undefined'
        }
        res = self.session.post(
            self.url + 'online/easynet/page/acc/acc_mpg.aspx', headers=self.header, data=payload)
        soup = bs(res.content, 'html.parser')
        VIEWSTATE = soup.find("input", {"name": "__VIEWSTATE"}).get('value')
        VIEWSTATEGENERATOR = soup.find(
            "input", {"name": "__VIEWSTATEGENERATOR"}).get('value')

        return (VIEWSTATE, VIEWSTATEGENERATOR)

    def __acc_mpg_2(self, SESSIONEASY, VIEWSTATE, VIEWSTATEGENERATOR):
        self.header['Referer'] = self.url + \
            'online/easynet/page/acc/acc_mpg.aspx'
        payload = {
            '__EVENTTARGET': 'ctl00$DataProcess$SaCaGridView$ctl02$SaCa_LinkButton',
            '__VIEWSTATE': VIEWSTATE,
            'SESSIONEASY': SESSIONEASY,
            '__VIEWSTATEGENERATOR': VIEWSTATEGENERATOR
        }
        res = self.session.post(
            self.url + 'online/easynet/page/acc/acc_mpg.aspx', headers=self.header, data=payload)
        soup = bs(res.content, 'html.parser')
        SESSIONEASY = soup.find("input", {"name": "SESSIONEASY"}).get('value')

        return SESSIONEASY

    def __acc_bnk_bln(self, SESSIONEASY):
        self.header['Referer'] = self.url + \
            'online/easynet/page/acc/acc_mpg.aspx'
        payload = {
            'SESSIONEASY': SESSIONEASY
        }
        res = self.session.post(
            self.url + 'online/easynet/page/acc/acc_bnk_bln.aspx', headers=self.header, data=payload)
        soup = bs(res.content, 'html.parser')
        VIEWSTATE = soup.find("input", {"name": "__VIEWSTATE"}).get('value')
        ctl00 = soup.find(
            "select", {"name": "ctl00$DataProcess$DDLAcctNo"}).get('value')
        VIEWSTATEGENERATOR = soup.find(
            "input", {"name": "__VIEWSTATEGENERATOR"}).get('value')

        return (VIEWSTATE, ctl00, VIEWSTATEGENERATOR)

    def __acc_bnk_bln_2(self, SESSIONEASY, VIEWSTATE, ctl00, VIEWSTATEGENERATOR):
        self.header['Referer'] = self.url + \
            'online/easynet/page/acc/acc_bnk_bln.aspx'
        payload = {
            '__EVENTTARGET': 'ctl00$DataProcess$Link2',
            '__VIEWSTATE': VIEWSTATE,
            'ctl00$DataProcess$DDLAcctNo': ctl00,
            'SESSIONEASY': SESSIONEASY,
            '__VIEWSTATEGENERATOR': VIEWSTATEGENERATOR
        }
        res = self.session.post(
            self.url + 'online/easynet/page/acc/acc_bnk_bln.aspx', headers=self.header, data=payload)
        soup = bs(res.content, 'html.parser')
        word = str(soup.find_all('script')[6].contents)
        SESSIONEASY = word.split("new Array(\\\'")[2].split("\\\')")[0]

        return SESSIONEASY

    def __get_statement_lst(self, SESSIONEASY):
        self.header['Referer'] = self.url + \
            'online/easynet/page/acc/acc_bnk_bln.aspx'
        payload = {
            'SESSIONEASY': SESSIONEASY,
        }
        res = self.session.post(
            self.url + 'online/easynet/page/acc/acc_bnk_tst.aspx', headers=self.header, data=payload)
        soup = bs(res.content, 'html.parser')
        qry = soup.find(
            "table", {"id": "DataProcess_GridView"})

        statement_lst = []

        if qry:
            trans = qry.find_all("tr")[1:len(qry)-1]
            for tst in trans:
                data = tst.find_all("td")
                date_text = f'{data[0].text} {data[1].text}'
                amount_text = data[5].text
                if 'รวม' not in date_text and amount_text.startswith('+'):
                    date = datetime.strptime(
                        date_text, "%d/%m/%Y %H:%M").astimezone(timezone.utc)
                    amount = float(amount_text[1:])
                    number = data[6].text.split()[2]
                    statement = Statement(date, amount, number)
                    statement_lst.append(statement.__dict__)

        return statement_lst
