from django.shortcuts import render,get_object_or_404
from .models import Post
from .forms import AddPostForm


def all_posts(request):
    posts = Post.objects.all()
    return render(request, 'posts/all_posts.html', {'posts': posts})


def post_detail(request, year, month, day, slug):
    posts = get_object_or_404(Post, created__year=year, created__month=month, created__day=day, slug=slug )
    return render(request, 'posts/post_detail.html', {'posts': posts})


def add_post(request, user_id):
    if request.method == 'POST':
        pass
    else:
        form = AddPostForm()
    return render(request, 'posts/add_post.html', {'form': form})