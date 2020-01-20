from project import db
from project.models import Peoples,User,Logs
from datetime import datetime
def gettingTheUseage(id):
    logs=db.engine.execute("select count(*) as 'count' ,DAYNAME(use_at) as 'day' from logs where userID={} and month(use_at)=month(LOCALTIMESTAMP) and year(use_at)=year(LOCALTIMESTAMP) group by Day(use_at) order by Day(use_at) desc limit 7".format(id))
    log=[];
    for k in logs:
        log.append([k.day,k.count])
    log.reverse()
    return {'log':log}

def getALLUsers(id):
    users=[]
    for u in User.query.filter(User.id.notin_([id])).all():
        users.append(u)
    return users

def getOneDayTraffic():
    today=datetime(datetime.today().year,datetime.today().month,datetime.today().day)
    logs=Logs.query.filter(Logs.use_at>=today).all()
    return len(logs)

def gettingSystemGrowth(id):
    sys=db.engine.execute("SELECT MonthName(created_at) as 'month',COUNT(*) as 'count' FROM `peoples` group by Month(created_at) order by Date(created_at) limit 6".format(id))
    sysUsers=[]
    for k in sys:
        sysUsers.append([k.month,k.count])
    return {'growth':sysUsers}