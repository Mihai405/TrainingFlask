from application import db
from application.friends.models import Friends
from application.users.models import Users

db.create_all()
u=Users(email="mihai@yahoo.com",password="mihai",first_name="mihai",last_name="mihai")
u2=Users(email="mihai2@yahoo.com",password="mihai2",first_name="mihai2",last_name="mihai2")
f=Friends(first_name="mihai",last_name="mihai",number="0234567891",user=u)
f2=Friends(first_name="mihai2",last_name="mihai2",number="1234567891",user=u2)
db.session.add(u)
db.session.add(u2)
db.session.commit()