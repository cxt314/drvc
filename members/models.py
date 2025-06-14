import uuid
from django.db import models
from django.urls import reverse

# --- Helper Function ---
def generate_unique_code():
    return str(uuid.uuid4())[:8]

# --- Member Model ---
class Member(models.Model):
    name = models.CharField(max_length=50, unique=True, default=generate_unique_code, help_text="Unique name or identifier for the member")
    email = models.EmailField(unique=False, help_text="Email address of the member (not necessarily unique)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Member"
        verbose_name_plural = "Members"
        ordering = ['name'] 

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("member_detail", args=[str(self.id)])

# --- Member Alias Model ---
class MemberAlias(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="An alternative name or alias for the member")
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="aliases", 
        related_query_name="alias",
        help_text="The member this alias belongs to"
    )

    class Meta:
        verbose_name = "Member alias"
        verbose_name_plural = "Member aliases"
        ordering = ['name']
        
    def __str__(self):
        return self.name