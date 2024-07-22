from application import db,create_app
from application.model import Role,User

app = create_app()
def create_admin_user():
    with app.app_context():
        admin_role = Role.query.filter_by(name='Admin').first()
        if admin_role:
            admin_user = User(name = 'Anish',username='anish', role=admin_role)
            admin_user.set_password('1234')  # Set the admin user's password
            db.session.add(admin_user)
            db.session.commit()



if __name__ == '__main__':
    create_admin_user()