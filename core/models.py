from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
            Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email , **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None , **extra_fields ):
        extra_fields.setdefault('is_superuser' , False)
        return self._create_user(email, password , **extra_fields)

    def create_superuser(self , email, password , **extra_fields):
        extra_fields.setdefault('is_superuser' , True)
        extra_fields.setdefault('is_staff' , True)
        return self._create_user(email,password,**extra_fields)


class User(AbstractBaseUser , PermissionsMixin):

    USER_TYPES = (
        ('Administrator','Administrator'),
        ('Employee','Employee'),
        ('Accountant','Accountant')
    )

    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30 , db_index=True , unique=True)
    email = models.EmailField(unique=True , db_index=True)
    phone = models.CharField(max_length=30)
    address = models.TextField()
    role = models.CharField(choices=USER_TYPES , max_length=13)
    branch = models.ForeignKey('Branch' , on_delete=models.CASCADE , null=True)
    photo = models.ImageField(upload_to='users_images')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True , blank=True)
    updated_at = models.DateTimeField(auto_now=True , blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','role']

    objects = UserManager()

    def __str__(self):
        return "{}".format(self.username)



class Branch(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.name)


class Tag(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.name)


class Item(models.Model):
    name = models.CharField(max_length=50)
    branch = models.ForeignKey(Branch , on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    photo = models.ImageField(upload_to='items_images')
    total_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return "{}".format(self.name)
