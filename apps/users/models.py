import bcrypt
import re
from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    email = models.CharField(max_length=20)
    password_plaintext = models.CharField(max_length=32, null=True)
    password = models.CharField(max_length=255, null=False)
    pw_salt = models.CharField(max_length=255)
    is_admin = models.BooleanField()
    description = models.TextField(max_length=500)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name+' '+self.last_name

    def encrypt_pw(self):
        self.pw_salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(self.password_plaintext.encode(), self.pw_salt)
        self.password_plaintext = None

    def login_errors(self):
        db_user = User.objects.filter(email=self.email)
        errors = []
        if len(db_user)==0:
            db_user = self
            errors.append('No user exists with this email address')
        else:
            db_user = db_user[0]
            check_password = bcrypt.hashpw(self.password_plaintext.encode(), db_user.pw_salt.encode()).decode()
            if check_password != db_user.password:
                errors.append('Incorrect password supplied for this user')

        return db_user, errors 

    def registration_errors(self, exists_override=False, pw_override=False):
        errors = []

        db_user = User.objects.filter(email=self.email)
        if not exists_override:
            if len(db_user) > 0:
                errors.append('User already exists with this email')
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
        if not EMAIL_REGEX.match(self.email):
            errors.append('Invalid email format.')

        if not pw_override:
            if len(self.password_plaintext) < 8:
                errors.append('Password must be at least 8 characters')

        return self, errors


class Message(models.Model):
    to_user = models.ForeignKey(User, related_name="messages_received")
    from_user = models.ForeignKey(User, related_name="messages_written")
    content = models.TextField(max_length=400)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
