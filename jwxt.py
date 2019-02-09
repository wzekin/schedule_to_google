from login import auth
import pandas as pd
from bs4 import BeautifulSoup


QBURL = 'http://10.3.255.178:9001/gradeLnAllAction.do?type=ln&oper=qb'
BJGURL = 'http://10.3.255.178:9001/gradeLnAllAction.do?type=ln&oper=bjg'


class jwxt(auth):
    def __init__(self, username, password):
        auth.__init__(self,username,password)
        r = self.session.get('http://10.3.255.178:9001/caslogin.jsp')

    def QBList(self):
        r = self.session.get(QBURL)
        soup = BeautifulSoup(r.text, 'lxml')
        data = []
        for i in soup.select('a[href^="gradeLnAllAction.do?type=ln&oper=qbinfo"]'):
            data.append('http://10.3.255.178:9001/' + i.attrs['href'])
        return data

    def QB(self, url):
        r = self.session.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        data = pd.DataFrame([],
                            columns=['code', 'last', 'name',
                                     'E_name', 'grade', 'type', 'score'],
                            dtype=int)
        for i in soup.findAll("tr", class_='odd'):
            strings = i.stripped_strings
            # cla = i.findAll("td")
            try:
                data = data.append({
                    'code': next(strings),
                    'last': next(strings),
                    'name': next(strings),
                    'E_name': next(strings),
                    'grade': float(next(strings)),
                    'type': next(strings),
                    'score': float(next(strings))
                }, ignore_index=True)
            except:
                pass

        return data
