from __future__ import print_function
from bs4 import BeautifulSoup
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from jwxt import jwxt

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']
HTML_FILE = 'class.html'


def check():
    comfirm = input('确认导入？(y/n)')
    if comfirm == 'n' or comfirm == 'N' or comfirm == 'No':
        return False
    elif comfirm != 'y' and comfirm != 'Y' and comfirm != 'Yes':
        return check()
    else:
        return True


def insert(summary, location, descripton, start_time, end_time):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    time = service.freebusy().query(body={
        "timeMin": start_time,
        "timeMax": end_time,
        "items": [
            {
                "id": "primary"
            }
        ]
    }).execute()
    for i in time['calendars']['primary']['busy']:
        start = datetime.datetime.strptime(i['start'],'%Y-%m-%dT%H:%M:%S%z')
        end = datetime.datetime.strptime(i['end'],'%Y-%m-%dT%H:%M:%S%z')
        start_ = datetime.datetime.strptime(start_time,'%Y-%m-%dT%H:%M:%S%z')
        end_ = datetime.datetime.strptime(end_time,'%Y-%m-%dT%H:%M:%S%z')
        if (start - start_ < datetime.timedelta(minutes=1) and end - end_ < datetime.timedelta(minutes=1)):
            print('此事件已被创建！')
            return

    service.events().insert(calendarId='primary', body={
        "end": {
            "dateTime": end_time
        },
        "start": {
            "dateTime": start_time
        },
        "description": descripton,
        "summary": summary,
        "location": location,
        "colorId": get_color_from_name(summary),
        "reminders": {
            "overrides": [
                {
                    "minutes": 10,
                    "method": "popup"
                }
            ],
            "useDefault": False
        }
    }).execute()


def return_week(s):
    week = []
    index = 0
    flag = 0

    def getnumber(index):
        temp = index
        while temp < len(s) and s[temp].isdigit():
            temp += 1
        num = int(s[index:temp])
        index = temp
        return num, index

    if s[index] == '单':
        index += 3
        flag = 1
    elif s[index] == '双':
        index += 3
        flag = 2
    elif s[index] == '实':
        index += 5
    while len(s) > index and s[index].isdigit():
        start, index = getnumber(index)
        end = start
        if index < len(s):
            if s[index] == '-':
                index += 1
                end, index = getnumber(index)
                index += 1
            elif s[index] == '、':
                index += 1
            else:
                raise "invaild str"
        week += list(range(start, end+1))

    if flag == 2:
        for i in week:
            if i % 2 != 0:
                week.remove(i)
    elif flag == 1:
        for i in week:
            if i % 2 == 0:
                week.remove(i)
    return week


def get_color_from_name(s: str):
    if s.find('数学') != -1:
        return "10"
    elif s.find('计算') != -1:
        return "6"
    elif s.find('电子') != -1:
        return "7"
    elif s.find('物理') != -1:
        return "5"
    elif s.find('应用') != -1:
        return "3"
    else:
        return "8"


if __name__ == "__main__":
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # username = input('请输入用户名：')
    # password = input('请输入密码：')
    # jw = jwxt(username, password)
    # r = jw.session.get('http://10.3.255.178:9001/xkAction.do?actionType=6')
    # soup = BeautifulSoup(r.text, 'lxml')

    with open(HTML_FILE, 'r') as schedule:
        text = schedule.read()
        soup = BeautifulSoup(text, 'lxml')

    name = ''
    teacher = ''
    location = ''
    for tr in soup.findAll('tr', class_='odd'):
        time_ = datetime.datetime.strptime(
            '2019-02-25 08:00:00+0800', '%Y-%m-%d %H:%M:%S%z')  # 开学第一天
        tds = tr.findAll('td')
        try:
            if len(tds) == 18:
                name = tds[2].get_text(strip=True)
                teacher = tds[7].get_text(strip=True)
                weeks = tds[11].get_text(strip=True)
                weekday = int(tds[12].get_text(strip=True))
                session = int(tds[13].get_text(strip=True))
                number = int(tds[14].get_text(strip=True))
                location = tds[17].get_text(strip=True)
            else:
                weeks = tds[0].get_text(strip=True)
                weekday = int(tds[1].get_text(strip=True))
                session = int(tds[2].get_text(strip=True))
                number = int(tds[3].get_text(strip=True))
                location = tds[6].get_text(strip=True)
            print('-----------------------')
            print('课程名：', name)
            print('任课教师：', teacher)
            print('上课周数：', return_week(weeks))
            print('上课星期：', weekday)
            print('上课节次：', session)
            print('上课节数：', number)
            print('上课地点：', location)
        except:
            pass
        if not check():
            continue
        for week in return_week(weeks):
            start_time = time_ + \
                datetime.timedelta(days=weekday-1, weeks=week-1)
            if(session < 5):
                start_time += datetime.timedelta(hours=session-1)
            else:
                start_time += datetime.timedelta(hours=session, minutes=30)
            end_time = start_time + \
                datetime.timedelta(hours=number) - \
                datetime.timedelta(minutes=10)
            insert(name, location, teacher,
                    start_time.isoformat(), end_time.isoformat())
