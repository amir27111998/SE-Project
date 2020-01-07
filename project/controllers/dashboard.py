from project import db
from project.models import Peoples
import time
def gettingTheUseage(id):
    logs=db.engine.execute("select count(*) as 'count' ,DAYNAME(use_at) as 'day' from logs where userID={} and month(use_at)=month(LOCALTIMESTAMP) and year(use_at)=year(LOCALTIMESTAMP)  group by Day(use_at) limit 7".format(id))
    log=[];
    for k in logs:
        log.append([k.day,k.count])
    return {'log':log}

def gettingPopullation(id):
    logs=db.engine.execute("select count(*) as 'count' ,Month(use_at) as 'month' from logs where userID={} group by Month(use_at) order by Month(use_at) limit 5".format(id))
    log={}
    for k in logs:
        log[k.month]=[k.count]
    return log