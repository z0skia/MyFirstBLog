#Blog & Crud
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post

#USER SISTEM
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from .forms import PostForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required


#Index
def index(request):
    return render(request, 'blog/index.html')
#About
def about(request):
    return render(request, 'blog/about.html')
# CRUD-----------------------------------
#Read all postS    
def dash(request):
    posts = Post.objects.filter
    return render(request, 'blog/dash.html', {'posts':posts})
    
#Read post
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
#Create post
@login_required
def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/new_post.html', {'form': form,})

#Edit post
@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/edit_post.html', {'form': form})
    

#Delete Post
@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    
    return render(request, 'blog/delete_post.html')
    
#USER SYSTEM---------------------------------

#LOGIN
def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            usuario=form.cleaned_data.get('username')
            clave=form.cleaned_data.get('password')
            user=authenticate(username=usuario, password=clave)

            if user is not None:
                login(request, user)
                return render(request, 'blog/index.html', {'usuario':usuario, 'mensaje':'Bienvenido al sistema'})
            else:
                return render(request, 'blog/login.html', {'form':form, 'mensaje':'USUARIO INCORRECTO, VUELVA A LOGUEAR'})
        else:
            return render(request, 'blog/login.html', {'form':form, 'mensaje':'FORMULARIO INVALIDO, VUELVA A LOGUEAR'})
    
    else:
        form=AuthenticationForm()
        return render(request, 'blog/login.html', {'form':form})

#REGISTER
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            form.save()
            return render(request, 'blog/registerok.html', {'message':f'USUARIO: {username} CREADO EXITOSAMENTE'})
        else:
            return render(request, 'blog/register.html', {'message':'NO SE PUDO CREAR EL USUARIO', 'form':form})
    else:
        form = UserRegistrationForm()
        return render(request, 'blog/register.html', {'form':form})
    

