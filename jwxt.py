from login import auth
from bs4 import BeautifulSoup


QBURL = 'http://10.3.255.178:9001/gradeLnAllAction.do?type=ln&oper=qb'
BJGURL = 'http://10.3.255.178:9001/gradeLnAllAction.do?type=ln&oper=bjg'


class jwxt(auth):
    def __init__(self, username, password):
        auth.__init__(self,username,password)
        r = self.session.get('https://jwxt.bupt.edu.cn/caslogin.jsp')

