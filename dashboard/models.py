from django.db import models

# Create your models here.

#Model For a user
class User(models.Model):
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=200)
    #salt=models.CharField(max_length)
    def __str__(self):
        return "User %s"%(self.username)
    def isPasswordCorrect(self, hashedpassword):
        return (hashedpassword == self.password)
    maxapp=models.IntegerField(default=0)
#Model for each installed app
#Explainations of each will be given when used
class InstalledApp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app_id = models.IntegerField(auto_created=True)
    app_tile_id = models.CharField(max_length=500)
    app_page_id = models.CharField(max_length=500)
    app_x_width = models.IntegerField(default=1)
    app_y_width = models.IntegerField(default=1)
    app_x_weight = models.IntegerField(default=1)
    app_y_weight = models.IntegerField(default=1)
    
    def __str__(self):
        return "App %d At %s"%(self.app_id, self.app_page_id)

