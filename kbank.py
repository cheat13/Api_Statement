import requests
import random
from bs4 import BeautifulSoup as bs
from datetime import datetime, timezone
from Models.statement import Statement


class KBank():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.session()
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
        self.content_type = 'application/x-www-form-urlencoded'
        self.url = 'https://online.kasikornbankgroup.com/'
        self.header = {
            'User-Agent': self.user_agent,
            'Content-Type': self.content_type,
            'Origin': self.url
        }

    def get_statement_lst(self):
        token = self.__get_token()
        self.__login(token)
        txtParam = self.__get_txtParam()
        self.__nav_welcome(txtParam)
        data = self.__nav_statement()
        statement_lst = self.__get_statement_lst(
            data['token'], data['action'], data['st'])

        return statement_lst

    def __get_token(self):
        soup = bs(self.session.get(
            self.url+'/K-Online/login.jsp?lang=th&type=').content, 'html.parser')
        token = soup.find("input", {"name": "tokenId"}).get('value') + '0'
        return token

    def __login(self, token):
        self.header['Referer'] = self.url+'/K-Online/login.do'
        payload = {
            'tokenId': token,
            'userName': self.username,
            'password': self.password,
            'cmd': 'authenticate',
            'locale': 'th',
            'app': '0'
        }
        self.session.post(self.url+'/K-Online/login.do',
                          headers=self.header, data=payload)

    def __get_txtParam(self):
        r = str(random.randint(0, 9999))
        soup = bs(self.session.get(
            'https://online.kasikornbankgroup.com/K-Online/ib/redirectToIB.jsp?r='+r).content, 'html.parser')
        txtParam = soup.find("input", {"name": "txtParam"}).get('value')
        return txtParam

    def __nav_welcome(self, txtParam):
        self.header['Referer'] = self.url
        payload2 = {
            'txtParam': txtParam,
        }
        self.session.post(
            'https://ebank.kasikornbankgroup.com/retail/security/Welcome.do', headers=self.header, data=payload2)

    def __nav_statement(self):
        soup = bs(self.session.get(
            'https://ebank.kasikornbankgroup.com/retail/cashmanagement/TodayAccountStatementInquiry.do').content, 'html.parser')
        token = soup.find(
            "input", {"name": "org.apache.struts.taglib.html.TOKEN"}).get('value')
        action = soup.find("input", {"name": "action"}).get('value')
        st = soup.find("input", {"name": "st"}).get('value')
        return {'token': token, 'action': action, 'st': st}

    def __get_statement_lst(self, token, action, st):
        self.header['Referer'] = 'https://ebank.kasikornbankgroup.com/retail/cashmanagement/TodayAccountStatementInquiry.do'
        payload = {
            'org.apache.struts.taglib.html.TOKEN': token,
            'captcha_check': 'null',
            'acctId': '20200723752659',
            'action': action,
            'st': st
        }
        res = self.session.post(
            'https://ebank.kasikornbankgroup.com/retail/cashmanagement/TodayAccountStatementInquiry.do', headers=self.header, data=payload)

        soup = bs(res.content, 'html.parser')
        transaction = soup.find(
            "table", {"id": "trans_detail"}).find_all("tr")[1:]

        statement_lst = []

        for trans in transaction:
            amount_string = trans.find_all(
                "td", {"class": "inner_table_center"})[1].text
            if amount_string:
                qry = trans.find("td", {"class": "inner_table_left"}).text
                date_string = ' '.join(str(qry).split())
                date = datetime.strptime(
                    date_string, "%d/%m/%y %H:%M:%S").astimezone(timezone.utc)

                amount = float(amount_string)

                number = trans.find_all(
                    "td", {"class": "inner_table_center"})[2].text

                statement = Statement(date, amount, number)
                statement_lst.append(statement.__dict__)

        return statement_lst
