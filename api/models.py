from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError('Users must have a username')

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            paid_fee=True
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, username, password, email, first_name, last_name):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, email, first_name='', last_name=''):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

    def update_user(self, username, email, first_name, last_name, password, acft_results=[], paid_fee=True):
        """
        Updates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError('Users must have a valid username')

        if not email:
            raise ValueError('Users must have a valid email address')

        user = User.objects.get_by_natural_key(username=username)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.paid_fee = paid_fee
        user.acft_results.set(acft_results)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(
        verbose_name='Username',
        max_length=30,
        unique=True
    )
    email = models.CharField(
        verbose_name='Email',
        max_length=50,
        unique=True,
        default=''
    )
    staff = models.BooleanField(default=False)  # an admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser

    first_name = models.CharField(
        verbose_name='First Name',
        max_length=30,
        unique=False
    )
    last_name = models.CharField(
        verbose_name='Last Name',
        max_length=30,
        unique=False
    )

    paid_fee = models.BooleanField(default=False, blank=True)

    def get_full_name(self):
        return self.first_name + self.last_name

    def get_short_name(self):
        return self.first_name

    # notice the absence of a "Password field", that is built in.
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']  # Username & Password are required by default.

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    objects = UserManager()


class ACFTResult(models.Model):
    month = models.IntegerField(default=1, blank=True)
    day = models.IntegerField(default=1, blank=True)
    year = models.IntegerField(default=2022, blank=True)
    gender = models.CharField(default='F', max_length=1, blank=True)
    age = models.IntegerField(default=0, blank=True)
    deadlift_raw = models.IntegerField(default=0, blank=True)
    deadlift_score = models.IntegerField(default=0, blank=True)
    spt_raw = models.FloatField(default=0, blank=True)
    spt_score = models.IntegerField(default=0, blank=True)
    pushups_raw = models.IntegerField(default=0, blank=True)
    pushups_score = models.IntegerField(default=0, blank=True)
    sdc_raw = models.IntegerField(default=0, blank=True)
    sdc_score = models.IntegerField(default=0, blank=True)
    plank_raw = models.IntegerField(default=0, blank=True)
    plank_score = models.IntegerField(default=0, blank=True)
    tmr_raw = models.IntegerField(default=0, blank=True)
    tmr_score = models.IntegerField(default=0, blank=True)
    total_score = models.IntegerField(default=0, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='acft_results')


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
