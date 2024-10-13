from django.shortcuts import render,redirect,get_object_or_404
from .models import*
from django.shortcuts import render, redirect
from .models import Todo  
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
@login_required(login_url="/login")
def homepage(request):
  return render(request,'index.html')
@login_required(login_url="/login")
def task(request):
    if request.method == "POST":
        data = request.POST
        title = data.get('title')
        description = data.get('description')
        deadline = data.get('deadline')

        # Ensure user is logged in and create a new task associated with the user
        if request.user.is_authenticated:
            Todo.objects.create(
                user=request.user,  # Associate task with logged-in user
                title=title,
                description=description,
                deadline=deadline
            )
        return redirect('/task/')
    
    # Handle sorting
    sort_by = request.GET.get('sort', 'date_uploaded')  # Default to sorting by date_uploaded

    # Filter tasks for the logged-in user and apply sorting
    if request.user.is_authenticated:
        if sort_by == 'deadline':
            queryset = Todo.objects.filter(user=request.user).order_by('deadline')  # Sort by deadline
        else:
            queryset = Todo.objects.filter(user=request.user).order_by('-date_uploaded')  # Sort by date_uploaded (most recent first)
    else:
        queryset = Todo.objects.none()  # Return an empty queryset if user is not authenticated

    context = {
        'work': queryset,
        'sort_by': sort_by,
    }

    return render(request, 'task.html', context)


def delete(request, id):
    todo_item = get_object_or_404(Todo, id=id)  # Fetches the Todo item or raises 404 if not found
    todo_item.delete()                            # Deletes the Todo item
    return redirect('/task/')   
def update(request, id):
  todo = Todo.objects.get(id=id)
  if request.method == "POST":
      data=request.POST
      title=data.get('title')
      description=data.get('description')
      deadline=data.get('deadline')
      if title:
       todo.title=title
      if description:
       todo.description=description
      if deadline:
       todo.deadline=deadline
      todo.save()
      return redirect('/task/')
  return render(request, 'update.html', {'Todo': todo})
def completed(request,id):
  queryset=get_object_or_404(Todo,id=id)
  queryset.complete=True
  queryset.save()
  return redirect('/task/')
def incompleted(request,id):
  queryset=get_object_or_404(Todo,id=id)
  queryset.complete=False
  queryset.save()
  return redirect('/task/')
def register_page(request):
    
     if request.method=="POST":
         first_name=request.POST.get('first_name')
         last_name=request.POST.get('last_name')
         username=request.POST.get('username')
         password=request.POST.get('password')
         
         user=User.objects.filter(username=username)
         
         if user.exists():
             messages.info(request,'Username already taken ')
             return redirect('/register/')
         
         user= User.objects.create(
             first_name=first_name,
             last_name=last_name,
             username= username,
             
          )
         
         user.set_password(password)
         user.save()
         
         messages.info(request,'Account created.')
         
         return redirect('/login/')
     return render(request,'register.html')
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid username')
            return redirect('/login/')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, 'Invalid password')
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/home/')  # Adjust to your desired redirect URL

    return render(request, 'login.html')  # Make sure this template exists

def logout_page(request):
    logout(request)
    return redirect('/login/')

