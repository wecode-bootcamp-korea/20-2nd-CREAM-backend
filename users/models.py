from django.db import models

class User(models.Model):
    nickname  = models.CharField(max_length=45)
    email     = models.CharField(max_length=45, unique=True)
    password  = models.CharField(max_length=200)
    point     = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email