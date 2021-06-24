from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, User as U
from django.forms import ModelForm
import datetime
from django.utils import timezone

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

	#u1 = User.objects.get(id=2)
	email = models.EmailField(max_length=40)
	firstName = models.CharField(max_length=20)
	lastName = models.CharField(max_length=20)
	weight = models.IntegerField()
	points = models.IntegerField(default = 0)

	def __str__(self):
		return self.firstName + ' ' + self.lastName + ' ' + str(self.weight) + ' '

class Workout(models.Model):
	user = models.ForeignKey(U, on_delete=models.CASCADE)

	#users can have workout partners -- stored as text (just their username); will later use this to display on
	# both their page and workout creator's page
	partner_username = models.CharField(max_length=200)
	workout_type = models.CharField(max_length=40)

	#in minutes
	duration = models.DurationField()
	date = models.DateTimeField(auto_now_add=True, blank=False)
	note = models.CharField(max_length=1000)
	is_private = models.BooleanField(blank=True, default=False)

class Favorite(models.Model):
	#current_user = models.CharField(max_length=40)

	user = models.CharField(max_length=100, unique=False)
	id = models.CharField(max_length=200, default='0', primary_key=True)
	current_user = models.ForeignKey(U, on_delete=models.CASCADE, default=None, unique=False)



# Create your models here.

class Nutrition(models.Model):
	user = models.ForeignKey(U, on_delete=models.CASCADE, default=None)
	title = models.CharField(max_length=100, default='', blank=False)
	text = models.TextField(max_length=1000, default='', blank=False)
	date = models.DateTimeField(auto_now_add=True, blank=False)
	def __str__(self):
		return self.title
	def published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.date <= now
		published_recently.admin_order_field = 'date'
		published_recently.boolean = True
		published_recently.short_description = 'published recently'

class NutriForm(ModelForm):
    class Meta:
    	model = Nutrition
    	fields = ['title', 'text']

class PublicPost(models.Model):
	user = models.ForeignKey(U, on_delete=models.CASCADE)
	title = models.CharField(max_length=200, default = "Default Title")
	content = models.CharField(max_length=2000, default = "Default Content")
	date = models.DateTimeField('date of posting')
	is_highlighted = models.BooleanField(blank=True, default=False)

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Recommended(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    # def __str__(self):
    #     return self.title


	
