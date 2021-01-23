from menulisulasan import app, db, api, jwt
from menulisulasan.resources.user import UserRegistration, UserLogin, UserLogout, TokenRefresh


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')

if __name__ == "__main__":
    app.run(port=5000)
