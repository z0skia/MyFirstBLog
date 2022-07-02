#Blog & Crud
from urllib import request
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Avatar

#USER SISTEM
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .forms import AvatarForm, PostForm, UserRegistrationForm, UserEditForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.contrib.auth.models import User



#Index
def index(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/index.html', {'posts':posts})



#About
def about(request):
    return render(request, 'blog/about.html')
# CRUD-----------------------------------
#Read all postS    
def dash(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
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
    
#USER PROFILE

#Profile detail
@login_required
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    avatar=Avatar.objects.filter(user=request.user.id) 
    return render(request, 'blog/user_detail.html', {'user':user, 'url':avatar[0].avatar.url})


#Edit profile

@login_required
def edit_profile(request):
    usuario=request.user

    if request.method == 'POST':
        form=UserEditForm(request.POST, instance=usuario)
        if form.is_valid():
            informacion=form.cleaned_data
            usuario.email=informacion['email']
            usuario.password1=informacion['password1']
            usuario.password2=informacion['password2']
            usuario.save()

            return render(request, 'blog/user_detail.html', {'usuario':usuario, 'message':'PERFIL EDITADO EXITOSAMENTE'})
    else:
        form=UserEditForm(instance=usuario)
    return render(request, 'blog/edit_profile.html', {'form':form, 'usuario':usuario.username})

def user_profiles(request):
    users = User.objects.filter
    return render(request, 'blog/user_profiles.html', {'users':users})

class user_page(DetailView):
    model = User
    template_name = "blog/user_page.html"
    


@login_required
def add_avatar(request):
    user=User.objects.get(username=request.user)
    if request.method == 'POST':
        form=AvatarForm(request.POST, request.FILES)
        if form.is_valid():

            previousAvatar=Avatar.objects.get(user=request.user)
            if(previousAvatar.avatar):
                previousAvatar.delete()
            avatar=Avatar(user=user, avatar=form.cleaned_data['avatar'])
            avatar.save()
        
        return render(request, 'blog/user_detail.html', {'usuario':user, 'mensaje':'AVATAR AGREGADO EXITOSAMENTE'})

    else:
        form=AvatarForm()
    return render(request, 'blog/add_avatar.html', {'form':form, 'usuario':user})
