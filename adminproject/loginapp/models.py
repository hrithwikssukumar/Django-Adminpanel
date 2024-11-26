from django.db import models

class CustomUser(models.Model):

    username = models.CharField(max_length=50, unique=True,null=True,blank=True)
    phone = models.CharField(max_length=20,unique=True,null=True,blank=True) 
    email = models.EmailField(unique=True,null=True,blank=True)
    password = models.CharField(max_length=128,null=True,blank=True)
    is_admin= models.BooleanField(default=False,null=True,blank=True)

    # USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['email']
    class Meta:
        db_table = 'loginuser'

    def __str__(self):
        return self.username
    


    

