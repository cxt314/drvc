from django.shortcuts import render
from django.views import generic
from .models import Member

# Create your views here.
class MemberListView(generic.ListView):
    model = Member
    template_name = "members/member_list.html"

class MemberDetailView(generic.DetailView):
    model = Member
    template_name = "members/detail.html"