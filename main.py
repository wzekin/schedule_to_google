import getpass
from ics import Calendar, Event
from bupt_api.jwxt import Jwxt


def check():
    confirm = input('确认导入？(y/n)')
    if confirm == 'n' or confirm == 'N' or confirm == 'No':
        return False
    elif confirm != 'y' and confirm != 'Y' and confirm != 'Yes':
        return check()
    else:
        return True


if __name__ == "__main__":
    username = input('请输入用户名：')
    password = getpass.getpass('请输入密码：')
    c = Calendar()
    jwxt = Jwxt(username, password)
    classes = jwxt.get_classes()
    for class_ in classes:
        print('---------------------------')
        print('课程名：', class_.name)
        print('任课教师：', class_.teacher)
        print('上课周数', class_.weeks)
        print('上课星期：', class_.weekday)
        print('上课节次：', class_.session)
        print('上课节数：', class_.number)
        print('上课地点：', class_.location)
        if check():
            for time_ in class_.time:
                e = Event()
                e.name = class_.name
                e.begin = time_.start_time.isoformat()
                e.end = time_.end_time.isoformat()
                e.location = class_.location
                e.description = class_.teacher
                c.events.add(e)

    with open('my.ics', 'w') as my_file:
        my_file.writelines(c)
