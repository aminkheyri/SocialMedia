from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Vote
from .forms import AddPostForm, EditPostForm, AddCommentForm, AddReplyForm
from django.contrib import messages
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required


def all_posts(request):
    posts = Post.objects.all()
    return render(request, 'posts/all_posts.html', {'posts': posts})


def post_detail(request, year, month, day, slug):
    posts = get_object_or_404(Post, created__year=year, created__month=month, created__day=day, slug=slug )
    comments = Comment.objects.filter(post=posts, is_reply=False)
    reply_form = AddReplyForm()
    can_like = False
    if request.user.is_authenticated:
        if posts.user_can_like(request.user):
            can_like = True
    if request.method == "POST":
        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment_form = form.save(commit=False)
            comment_form.post = posts
            comment_form.user = request.user
            comment_form.save()
            messages.success(request, 'your comment submitted successfully')
    else:
        form = AddCommentForm()
    return render(request, 'posts/post_detail.html', {'posts': posts, 'comments': comments, 'form': form,
                                                      'reply': reply_form, 'can_like': can_like})


@login_required
def add_post(request, user_id):
    if request.user.id == user_id:
        if request.method == 'POST':
            form = AddPostForm(request.POST)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.user = request.user
                new_post.slug = slugify(form.cleaned_data['body'][:30], allow_unicode=True)
                new_post.save()
                messages.success(request, 'Your Post submitted', 'success')
                redirect('account:dashboard', user_id)
        else:
            form = AddPostForm()
        return render(request, 'posts/add_post.html', {'form': form})
    else:
        return redirect('posts:all_posts')


@login_required
def post_delete(request, user_id, post_id):
    if user_id == request.user.id:
        Post.objects.filter(pk=post_id).delete()
        messages.success(request, 'Your Post Deleted Successfully', 'success')
        return redirect('account:dashboard', user_id)
    else:
        return redirect('posts:all_posts')


@login_required
def post_edit(request, user_id, post_id):
    if request.user.id == user_id:
        post = get_object_or_404(Post, pk=post_id)
        if request.method == "POST":
            form = EditPostForm(request.POST, instance=post)
            if form.is_valid():
                edit_post = form.save(commit=False)
                edit_post.slug = slugify(form.cleaned_data['body'][:30])
                edit_post.save()
                messages.success(request, 'Your Post Edited', 'success')
                return redirect('account:dashboard', user_id)
        else:
            form = EditPostForm(instance=post)
        return render(request, 'posts/edit_post.html', {'form': form})
    else:
        return redirect('posts:all_posts')


@login_required
def add_reply(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == "POST":
        form = AddReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request, 'your reply submitted successfully', 'success')
    return redirect('posts:post_detail', post.created.year, post.created.month, post.created.day, post.slug)


def post_like(request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like = Vote(post=post, user=request.user)
        like.save()
        messages.success(request, 'post liked', 'success')
        return redirect('posts:post_detail', post.created.year, post.created.month, post.created.day, post.slug)
