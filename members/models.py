import uuid
from django.db import models

# Create your models here.
def generate_unique_code():
    return str(uuid.uuid4())[:8]

class Member(models.Model):
    name = models.CharField(max_length=50, unique=True, default=generate_unique_code)
    email = models.EmailField(unique=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class MemberAlias(models.Model):
    name = models.CharField(max_length=100, unique=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return self.name