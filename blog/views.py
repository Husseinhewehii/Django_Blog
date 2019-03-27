
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import (
	ListView, DetailView, CreateView, UpdateView, DeleteView
	)
from . models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
#from django.http import HttpResponse
#zqkvsadpfgtyaskc

def home(request):
	""" display posts in home page """
	context = {
	'posts':	Post.objects.all()
	}
	return render (request,'blog/home.html',context)

class PostListView(ListView):
	""" represent all posts """
	model = Post
	template_name = 'blog/home.html'#<app>/<model>_<viewtype>.html
	context_object_name = 'posts'   # <--- default name by django of that variable "object_list"
	ordering = ['-date_posted']
	paginate_by = 5

class UserPostListView(ListView):
	""" represent all posts per user """
	model = Post
	template_name = 'blog/user_posts.html'#<app>/<model>_<viewtype>.html
	context_object_name = 'posts'   # <--- default name by django of that variable "object_list"
	paginate_by = 5

	def get_queryset(self):
		""" overriding the get_queryset method to display posts related to current user's author"""
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
	model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title','content']

	def form_valid(self,form):
		""" overriding the form_valid method """
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title','content']

	def form_valid(self,form):
		""" overriding the form_valid method """
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		""" usertextmixin provides this function to check if post updated by its author """
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class PostDeleteView(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
	""" send user to home page after post is deleted """
	model = Post
	success_url = '/'

	def test_func(self):
		""" usertextmixin provides this function to check if post deleted by its author """
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

def about(request):
	""" go to about page"""
	return render(request,'blog/about.html',{'title':'über'})
