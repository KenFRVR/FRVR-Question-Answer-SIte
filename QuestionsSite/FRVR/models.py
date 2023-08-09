from django.contrib.auth.models import User
from django.db import models


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=False)
    text = models.TextField(blank=True)
    publication_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_questions")
    too_long = False

    def summary(self, n=250):
        if len(self.text) > n:
            self.too_long = True
            return self.text[:n] + '...'
        return self.text

    def __str__(self):
        return self.title


class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField(blank=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_answers")
    publication_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'id: {self.id}, question: {self.question}'


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='This is my bio')
    banner = models.ImageField(default='FRVR/static/images/banner.jpg')
    pic = models.ImageField(default='FRVR/static/images/profile_picture.png')

    def __str__(self):
        return f'id: {self.id}, user: {self.user.username}'
