import uuid
from django.db import models
from django.urls import reverse

# Create your models here.
def generate_unique_code():
    return str(uuid.uuid4())[:8]

class Member(models.Model):
    name = models.CharField(max_length=50, unique=True, default=generate_unique_code)
    email = models.EmailField(unique=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "member"
        verbose_name_plural = "members"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("member_detail", args=[str(self.id)])

class MemberAlias(models.Model):
    name = models.CharField(max_length=100, unique=True)
    member = models.ForeignKey(
        Member, 
        on_delete=models.CASCADE,
        related_name="aliases",
        related_query_name="alias",
    )

    class Meta:
        verbose_name = "member alias"
        verbose_name_plural = "member aliases"
        
    def __str__(self):
        return self.name