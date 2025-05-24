from django.db import models

# Create your models here.
class Member(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

class MemberAlias(models.Model):
    name = models.CharField(max_length=100, unique=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return self.name