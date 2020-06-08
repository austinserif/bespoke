from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, StringField
from wtforms.validators import DataRequired, Length, Email
from wtforms_alchemy import model_form_factory, Unique
from models import User, db, Tag

BaseModelForm = model_form_factory(FlaskForm)

class ModelForm(BaseModelForm):
    """Model Form class"""
    @classmethod
    def get_session(self):
        return db.session
    
class UserSignUpForm(ModelForm):
    """UserSignUpForm class"""
    class Meta:
        model = User
        only = ['email', 'first_name', 'last_name', 'password']

    email = StringField("email", validators=[DataRequired(), Length(min=5, max=100)])
    first_name = StringField("first name", validators=[DataRequired(), Length(min=1, max=100)])
    last_name = StringField("last name", validators=[DataRequired(), Length(min=1, max=100)])
    password = PasswordField("password", validators=[DataRequired(), Length(min=6, max=100)])

class GetStartedForm(ModelForm):
    """get started form model class"""
    class Meta:
        model = User
        only = ['email']

    email = StringField("email", validators=[DataRequired(), Unique(User.email, message="A user is already registered to this email."), Length(min=5, max=100)])

class UserLoginForm(ModelForm):
    """UserLoginForm class"""
    class Meta:
        model = User
        only = ['email', 'password']

    email = StringField("email", validators=[DataRequired(), Length(min=5, max=100)])
    password = PasswordField("password", validators=[DataRequired(), Length(min=6, max=100)])

class NewTagForm(ModelForm):
    """NewTagForm class"""
    class Meta:
        model = Tag
        only = ['name']

    name = StringField("tag", validators=[DataRequired(), Length(min=1, max=100)])
