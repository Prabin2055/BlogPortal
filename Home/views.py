from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from blog .models import *
from django.contrib.auth import authenticate,  login, logout
from blog.models import BlogPost
from Home.models import *

def home(request):
    posts = None
    categories = Category.get_all_categories()
    categorYID = request.GET.get('category')
    if categorYID:
        posts = FeaturePost.get_all_post_by_catrgoriesid(categorYID)
    else:
        posts = FeaturePost.get_all_post()
    data = {}
    data['posts'] = posts
    data['categories'] = categories
    return render(request, "home/home.html", data)
    # posts = FeaturePost.objects.all()
    # content = {'posts':posts}
    # return render(request,'home/home.html',content)

def featurepost(request,slug):
    post = FeaturePost.objects.filter(slug=slug).first()
    context={'post':post}
    return render(request, "home/homePost.html", context)



def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if len(name) < 2 or len(email) < 3 or len(phone) < 10 or len(content) < 4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message has been successfully sent")
    return render(request,'home/contact.html')

def about(request):
    return render(request,'home/about.html')






def search(request):
    query = request.GET['query']
    if len(query)>78:
        allPosts = BlogPost.objects.none()
    else:
        allPostsTitle = BlogPost.objects.filter(title__icontains=query)
        allPostsAuthor = BlogPost.objects.filter(author__icontains=query)
        allPostsContent = BlogPost.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent, allPostsAuthor)
    if allPosts.count()==0:
        messages.warning(request, "No search results found. Please refine your query.")
    params = {'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)






def handleSignUp(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # check for errorneous input
        if len(username) < 10:
            messages.error(request, " Your user name must be under 10 characters")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('home')
        if (pass1 != pass2):
            messages.error(request, " Passwords do not match")
            return redirect('home')

        # Create the user
        myuser = User.objects.create_user(username, email, pass1,pass2)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, " you have been successfully created new users")
        return redirect('home')

    else:
        return HttpResponse("404 - Not found")


def handeLogin(request):
    if request.method == "POST":
        # Get the post parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("home")

    return HttpResponse("404- Not found")

    return HttpResponse("login")

def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')