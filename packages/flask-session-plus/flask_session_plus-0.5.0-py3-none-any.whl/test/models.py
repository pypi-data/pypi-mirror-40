import logging
from flask_login import UserMixin
from google.cloud import firestore

db = firestore.Client()
from google.cloud.exceptions import NotFound
from werkzeug.security import check_password_hash, generate_password_hash

log = logging.getLogger(__name__)


class User(UserMixin):

    def __init__(self, user_id, user_data):
        self.user_id = user_id
        self.user_ref = db.collection('users').document(user_id)
        self.auth_ids = user_data.pop('auth_ids', {})
        self.email = user_data.pop('email', '')
        self.password = user_data.pop('password', '')
        self.active = user_data.pop('active', False)
        self.temp = user_data.pop('temp', False)

        self.name = user_data.pop('name', '')
        self.country = user_data.pop('country', '')
        self.language = user_data.pop('language', '')
        self.timezone = user_data.pop('timezone', '')
        self.clients = user_data.pop('clients', {})

        self.extra_data = user_data

    def __repr__(self):
        return f'name: {self.name} ({self.user_id})'

    def get_id(self):
        return self.user_id

    @property
    def is_active(self):
        return self.active and not self.temp

    @classmethod
    def create_user(cls):
        pass

    @classmethod
    def get_user_by_id(cls, user_id):
        user_ref = db.collection('users').document(user_id)
        try:
            user = user_ref.get()
            user = cls(user_id=user_id, user_data=user.to_dict()) if user.exists else None
        except NotFound:
            user = None
        return user

    @classmethod
    def get_user_by_auth_id(cls, auth_id):
        user_ref = db.collection('users').where(f'auth_ids.{auth_id}', '==', True).limit(1)
        try:
            user_ref.get()
            user = list(user_ref.get())  # a query returns an iterator
            user = user[0] if user else None
        except Exception as e:
            log.error(f'Error while getting username by auth_id ({auth_id}): {e}')
            user = None

        if user:
            return cls(user.id, user.to_dict())
        else:
            return None

    @classmethod
    def get_user_by_email(cls, email):
        user_ref = db.collection('users').where('email', '==', email).limit(1)
        try:
            user_ref.get()
            user = list(user_ref.get())  # a query returns an iterator
            user = user[0] if user else None
        except Exception as e:
            log.error(f'Error while getting username by email ({email}): {e}')
            user = None

        if user:
            return cls(user.id, user.to_dict())
        else:
            return None

    def set_password(self, password):
        new_password = generate_password_hash(password)
        try:
            self.user_ref.update({'password': new_password})
            self.password = new_password
        except Exception as e:
            log.error(f'Error while setting password on User ({self.user_id}): {e}')
            return False
        return True

    def check_password(self, password):
        return check_password_hash(self.password, password)

    # def get_reset_password_token(self, expires_in=600):
    #     return jwt.encode(
    #         {'reset_password': self.user_id, 'exp': time() + expires_in},
    #         current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    # @classmethod
    # def get_user_by_token(cls, token):
    #     user_id = cls.verify_reset_password_token(token)
    #     return cls.get_user_by_id(user_id) if user_id else None

    # @classmethod
    # def verify_reset_password_token(cls, token):
    #     try:
    #         user_id = jwt.decode(token, current_app.config['SECRET_KEY'],
    #                              algorithms=['HS256'])['reset_password']
    #         return user_id
    #     except jwt.ExpiredSignatureError as e:
    #         log.debug('JWT has expired')
    #         return None
    #     except Exception as e:
    #         log.error(f'Error while decoding JWT: {e}')
    #         return None

    @classmethod
    def get_user_from_session(cls, session):
        if 'user_id' in session:
            return cls(session['user_id'], session.get('user_data', {}))
        else:
            return None
