from django.shortcuts import render, HttpResponse,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from blog.templatetags import extras
from .models import Category
from django.shortcuts import get_object_or_404



def blogHome(request):
    posts=None
    categories = Category.get_all_categories()
    categorYID = request.GET.get('category')
    if categorYID:
        posts = BlogPost.get_all_post_by_categoriesId(categorYID)
    else:
        posts = BlogPost.get_all_post()
    data = {}
    data['posts'] = posts
    data['categories'] = categories
    return render(request, "blog/bloghome.html",data)


# allPosts = BlogPost.objects.all()
# context = {'allPosts': allPosts}
# return render(request, "blog/blogHome.html", context)

# def blogPost(request, slug):
#     post=BlogPost.objects.filter(slug=slug).first()
#     comments= BlogComment.objects.filter(post=post)
#     context={'post':post, 'comments': comments, 'user': request.user}
#     return render(request, "blog/blogPost.html", context)


def blogPost(request, slug):
    post=BlogPost.objects.filter(slug=slug).first()
    comments= BlogComment.objects.filter(post=post, parent=None)
    replies= BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)

    context={'post':post, 'comments': comments, 'user': request.user, 'replyDict': replyDict}
    return render(request, "blog/blogPost.html", context)


def blogComment(request):
    if request.method == "POST":
        comment=request.POST.get('comment')
        user=request.user
        postSno = request.POST.get('postSno')
        post = BlogPost.objects.get(sno=postSno)
        parentSno = request.POST.get('parentSno')
        # print("PARENT SNO ", parentSno)
        if parentSno=="":
            comment=BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent= BlogComment.objects.get(sno=parentSno)
            comment=BlogComment(comment= comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")

    return redirect(f"/blog/{post.slug}")