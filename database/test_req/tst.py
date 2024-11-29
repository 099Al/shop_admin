from database.connect import DataBase
from database.models.models import Admin
from database.requests.req_login import ReqAdmins

if __name__ == '__main__':


    db = DataBase()
    req = ReqAdmins(db)
    res: Admin = req.check_login('123')
    print(res.role)
