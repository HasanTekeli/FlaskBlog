from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[
        DataRequired(),
        Length(min=2, max=20)
    ])
    email = StringField('E-posta', validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField('Şifre', validators=[
        DataRequired()
    ])
    confirm_password = PasswordField('Şifreyi tekrar girin', validators=[
        DataRequired(),
        EqualTo('password')
    ])
    submit = SubmitField('Kayıt ol')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Seçtiğiniz kullanıcı adı alınmış. Lütfen başka bir kullanıcı adı seçin.')
    
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Bu e-posta hesabı ile daha önce kayıt olunmuş. Giriş yapmayı deneyin.')

class LoginForm(FlaskForm):
    email = StringField('E-posta', validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField('Şifre', validators=[
        DataRequired()
    ])
    remember = BooleanField('Beni hatırla')
    submit = SubmitField('Giriş yap')

class UpdateAccountForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[
        DataRequired(),
        Length(min=2, max=20)
    ])
    email = StringField('E-posta', validators=[
        DataRequired(),
        Email()
    ])
    picture = FileField('Profil Fotoğrafını Güncelle', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Güncelle')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Seçtiğiniz kullanıcı adı alınmış. Lütfen başka bir kullanıcı adı seçin.')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('Bu e-posta hesabı ile daha önce kayıt olunmuş. Giriş yapmayı deneyin.')

class RequestResetForm(FlaskForm):
    email = StringField('E-posta', validators=[
        DataRequired(),
        Email()
    ])
    submit = SubmitField('Şifre yenileme linki iste')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email is None:
                raise ValidationError('Bu e-posta adresi ile ilişkilendirilmiş bir hesap bulunamadı.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Şifre', validators=[
        DataRequired()
    ])
    confirm_password = PasswordField('Şifreyi onayla', validators=[
        DataRequired(),
        EqualTo('password')
    ])
    submit = SubmitField('Şifreyi yenile')