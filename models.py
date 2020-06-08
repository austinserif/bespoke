from sqlalchemy import desc
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import EmailType
from flask_bcrypt import Bcrypt
import datetime

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """connect app to db"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User model class"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(EmailType, nullable=False, unique=True)
    password = db.Column(db.String(100))

    # ******** flask-login required attributes and methods ********
    authenticated = db.Column(db.Boolean, default=False)

    def __repr__(self):
        """return repr string with id name and email"""
        return f'<User {self.id} {self.first_name} {self.email}>'

    def is_active(self):
        """return active"""
        if self.first_name and self.last_name and self.password and self.email:
            return True
        else:
            return False

    def get_id(self):
        """Return unique, user-facing key (email)."""
        return self.id

    def is_authenticated(self):
        """Return True if authenticated."""
        return self.authenticated

    def is_annonymous(self):
        """Return False by definition."""
        return False

    def searches(self):
        """return list of active search items for user"""
        return SearchItem.query.filter(SearchItem.user_id==self.id).\
            filter(SearchItem.display==True).order_by(desc(SearchItem.date)).all()
    
    def active_tags(self):
        """return list of active tags"""
        return Tag.query.filter(Tag.user_id==self.id).\
            filter(Tag.display==True).order_by(desc(Tag.add_date)).all()

    @classmethod
    def get_started(cls, email):
        """take email and create new user object and commit to db, then return object"""
        user = User(email=email)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def sign_up(cls, user_obj):
        """take user_obj populated from form, hash and store password, commit to database"""
        hashed_pwd = bcrypt.generate_password_hash(user_obj.password).decode('UTF-8')
        user_obj.password = hashed_pwd
        db.session.add(user_obj)
        db.session.commit()

    @classmethod
    def authenticate(cls, user_obj, password):
        """check typed password hash against stored password hash, if user authentic
        update attrs and add to db session, return true, otherwise false"""
        if bcrypt.check_password_hash(user_obj.password, password):
            user_obj.authenticated = True
            db.session.add(user_obj)
            db.session.commit()
            return True
        else:
            return False
    
    @classmethod
    def get_inactive_users(cls):
        """return list of all inactive users, meaning that they entered their email but didn't complete sign up"""
        return User.query.filter(User.password==None).all()

    @classmethod
    def add_tag(cls, tag_name, user_id):
        """add new tag and return if doesn't exist yet, otherwise return False"""
        user = User.query.get(user_id)
        if len(Tag.query.filter(Tag.name==tag_name).filter(Tag.user_id==user_id).filter(Tag.display==True).all()) == 0:
            tag = Tag(name=tag_name, user_id=user_id)
            db.session.add(tag)
            db.session.commit()
            return tag
        else:
            return False

    @classmethod
    def add_search(cls, term, user_id):
        """add search term to database for given term and user_id"""
        item = SearchItem(term=term, user_id=user_id)
        db.session.add(item)
        db.session.commit()
        return item
    
    @classmethod
    def remove_search(cls, item_id):
        """set display column to False on search item of given id"""
        item = SearchItem.query.get(item_id)
        item.display = False
        db.session.commit()

class Tag(db.Model):
    """tag model class"""
    
    __tablename__ = "tags"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    add_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    delete_date = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)
    display = db.Column(db.Boolean, nullable=False, default=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship("User", backref="tags")

    @classmethod
    def remove_tag(cls, tag_id):
        """set display property on selected tag to False,
        this should trigger onupdate property for delete_date column, return tag object"""
        tag = Tag.query.get(tag_id)
        tag.display = False
        db.session.commit()
        return tag

class SearchItem(db.Model):
    """search_items model class"""
    
    __tablename__ = "search_items"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    term = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    display = db.Column(db.Boolean, nullable=False, default=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    user = db.relationship("User", backref="search_items")