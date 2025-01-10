from django.shortcuts import render,redirect,get_object_or_404
from.forms import CustomUserCreationForm,UserLoginForm
from django.contrib.auth import login,logout 
from .models import CustomUser
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.cache import never_cache 

# Create your views here.

def home(request):
    return render(request,'home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('userlogin') 
    else:
        form = CustomUserCreationForm()
    return render(request,'register.html', {'form': form})

def user_login(request):
    if 'admin_email' in request.session:
        return redirect('adminhome')
    if 'user_email' in request.session:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            try:
                user = CustomUser.objects.get(email=email)
                if user is not None:
                    if check_password(password,user.password):
                        if user.is_admin:
                            request.session['admin_email'] = email     
                            return redirect('adminhome')
                        else:
                            request.session['user_email'] = email
                            return redirect('dashboard')
                    else:
                        msg = "Invalid input"
                else:
                    msg = 'Email not found' 
            except CustomUser.DoesNotExist:
                msg = 'Invalid input'
                return render(request,'login.html',{'form':form,'msg':msg})
    else:
        form = UserLoginForm()
        return render(request,'login.html',{'form':form})

# @login_required(login_url='userlogin')
def dashboard(request):
    if 'user_email' not in request.session:
        return redirect('userlogin')
    user = CustomUser.objects.get(email=request.session['user_email'])
    return render(request, 'dashboard.html', {'user': user})

def user_logout(request):
    if 'user_email' in request.session:
        del request.session['user_email']
    if 'admin_email' in request.session:
        del request.session['admin_email']
    return redirect('userlogin')

def admin_home(request):
    if 'admin_email' not in request.session:
        return redirect('userlogin')
    if request.method == 'GET':
        users = CustomUser.objects.all()
        return render(request,'adminhome.html',{'users':users})
    return redirect('adminlogin')

def admin_logout(request):
    if 'admin_email' in request.session:
        request.session.flush()
    return redirect('userlogin')

def user_add(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminhome') 
        else:
            form = CustomUserCreationForm()
            return render(request,'useradd.html', {'form': form})
    return render(request,'useradd.html')

def user_search(request):
    search_query = request.GET.get('search')
    users = CustomUser.objects.filter(username__icontains=search_query) if search_query else CustomUser.objects.all()
    return render(request, 'adminhome.html', {'users': users, 'search_query': search_query})

def delete_user(request, user_id):
    if request.method == 'POST':  
        try:
            user = get_object_or_404(CustomUser, id=user_id)
            user.delete()
            return redirect('adminhome') 
        except CustomUser.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User does not exist'})
    return redirect('adminhome')

def edit(request,user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('adminhome')
        else:
            form = CustomUserCreationForm(instance=user)
    else:
        form = CustomUserCreationForm(instance=user)        
    return render(request, 'edit.html', {'form': form, 'user': user})










  





