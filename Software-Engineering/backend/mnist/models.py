from django.db import models

# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=32, help_text='Username')
    password = models.CharField(max_length=32, help_text='Password')

    def __str__(self):
        return self.username


class Images(models.Model):
    image = models.ImageField(upload_to='images/')
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=64, help_text='Image name')  # User give
    label = models.CharField(max_length=4, help_text='Image label')  # User give
    pred = models.CharField(max_length=4, help_text='Predict label')  # Predicted by mlp
    prob = models.CharField(max_length=8, help_text='Predict probability')  # Predict probability
    result = models.BooleanField(help_text='Predict result')  # Diff between real label and predict result

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.label, self.image.url
