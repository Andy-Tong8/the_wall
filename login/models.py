from django.db import models
import datetime, re
import bcrypt


coppacheck=datetime.datetime.now().date()-datetime.timedelta(days=4748)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


    
class LoginManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['reg_email'] = "Invalid email address!"
        elif User.objects.filter(email=postData['email']):
                errors['reg_email'] = "Email address already registered to a user"
        #check if date is in the valid format i.e if someone typed 20000-10-10
        try:
            datetime.datetime.strptime(postData['birthday'], '%Y-%m-%d')
            if datetime.datetime.strptime(postData['birthday'],'%Y-%m-%d').date() > coppacheck:
                errors["birthday"] = "You need to be at least 13 years old to register"
        except ValueError:
            errors["birthday"] = "Invalid Birthday"
        if postData['password']!=postData['confirm_pw']:
            errors["confirm_pw"] = "Passwords need to match"
        elif len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        return errors
    
    
    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email=postData['email'])
        if user:
            logged_user = user[0]
            if not bcrypt.checkpw(postData['password'].encode(), logged_user.password.encode()):
                errors["log_pw"] = "The password you entered is incorrect, please try again"
        else:
            errors["log_email"] = "No account with that e-mail address found"
        return errors
    

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = LoginManager()