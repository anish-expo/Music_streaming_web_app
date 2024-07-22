from application import db,create_app
from application.model import Role

app = create_app()
def create_role():
    admin_role = Role(name='Admin')
    creater = Role(name="Creator")
    user_role = Role(name='User')
    db.session.add(admin_role)
    db.session.add(user_role)
    db.session.add(creater)
    db.session.commit()



if __name__ == '__main__':
    with app.app_context():
       create_role()
    