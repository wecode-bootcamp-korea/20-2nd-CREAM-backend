from django.db import models

class User(models.Model):
    social_login_id = models.CharField(max_length=200, unique=True)
    nickname        = models.CharField(max_length=45, null=True)
    email           = models.EmailField(max_length=200, null=True)
    point           = models.IntegerField(default=0)
    create_at       = models.DateTimeField(auto_now_add=True)
    update_at       = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email