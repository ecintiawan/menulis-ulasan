from flask import jsonify
from menulisulasan import app, db, api, jwt, logger
from menulisulasan.resources.user import(
    User,
    UserRegistration,
    UserLogin,
    UserLogout,
    UserChangePassword,
    TokenRefresh,
    VerifyEmail,
    ResendEmail
)
from werkzeug.exceptions import HTTPException
from blacklist import BLACKLIST


@app.before_first_request
def before_first_request():
    db.create_all()


@app.before_request
def before_request():
    pass


@app.after_request
def after_request(response):
    if 200 <= response.status_code <= 299:
        logger.info(response.data.strip())
    else:
        logger.error(response.data.strip())
    return response


@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(e)
    if isinstance(e, HTTPException):
        return e
    return {"message": "Oops, ada yang salah."}, 500


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {"is_admin": True}
    return {"is_admin": False}


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        "message": "The token has expired.",
        "error": "token_expired"
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(e):
    return jsonify({
        "message": "Signature verification failed.",
        "error": "invalid_token"
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(e):
    return jsonify({
        "description": "Request does not contain an access token.",
        "error": "authorization_required"
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        "description": "The token is not fresh.",
        "error": "fresh_token_required"
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": "The token has been revoked.",
        "error": "token_revoked"
    }), 401


api.add_resource(User, "/user")
api.add_resource(UserRegistration, "/user/register")
api.add_resource(UserLogin, "/user/login")
api.add_resource(UserLogout, "/user/logout")
api.add_resource(UserChangePassword, "/user/change-password")
api.add_resource(TokenRefresh, "/user/refresh-token")
api.add_resource(VerifyEmail, "/user/verify-email")
api.add_resource(ResendEmail, "/user/resend-email")

if __name__ == "__main__":
    app.run(port=5000)
