from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    # TODO: 
    pass

class Like(models.Model):
    # TODO:
    pass

class Follower(models.Model):
    # TODO:
    pass
