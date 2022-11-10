from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.conf import settings




def logout_required(function=None, logout_url=settings.LOGOUT_URL):
    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated,
        login_url=logout_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


@login_required(login_url="/",)
def index(request):
    contacts = Contact.objects.all()

    search_input = request.GET.get('search-area')

    if search_input:
        contacts = Contact.objects.filter(full_name__icontains=search_input)
    else:
        contacts = Contact.objects.all()
        search_input = ''

    paginator = Paginator(contacts, 20)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    context = {
        'contacts': contacts,
        'search_input': search_input,
        'page': page
    }
    return render(request, 'index.html', context)


@login_required(login_url="/")
def addContact(request):

    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            contacts = form.save(commit=False)
            contacts.save()
            return redirect('/contact')
    else:
        form = ContactForm()

    context = {'form': form}
    return render(request, 'new.html', context)


@login_required(login_url="/")
def contactProfile(request, pk):
    # contact = Contact.objects.get(id=pk)
    contact = get_object_or_404(Contact, id = pk)
    return render(request, 'templates/contact-profile.html', {"contact": contact})


@user_passes_test(lambda u: u.is_superuser, '/contact')
def editContact(request, pk):
    post = get_object_or_404(Contact, id = pk)
    form = ContactForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('/profile/' + str(post.id))
    return render(request, 'templates/edit.html', {'post': post, 'form': form})



    # contacts = Contact.objects.get(id=pk)
    # if request.method == 'POST':
    #     contacts.full_name = request.POST['fullname']
    #     contacts.relationship = request.POST['relationship']
    #     contacts.phone_number = request.POST['phone-number']
    #     contacts.email = request.POST['e-mail']
    #     contacts.image = request.FILES['image']
    #     contacts.address = request.POST['address']
    #     contacts.save()
    #
    #     return redirect('/profile/' + str(contacts.id))
    # return render(request, 'templates/edit.html', {'contacts': contacts})


@user_passes_test(lambda u: u.is_superuser, '/contact')
def deleteContact(request, pk):
    contacts = Contact.objects.get(id=pk)
    if request.method == 'POST':
        contacts.delete()
        return redirect('/contact')
    return render(request, 'delete.html', {'contact': contacts})


@logout_required(logout_url='/contact')
def user_login(request):

    if request.method == "POST" :

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.success(request, ("خطا در ورود لطفا دوباره تلاش کنید!"))
            return redirect('login')
    else:
        return render(request, 'registration/login.html')




    # if request.method == "POST":
    #     form = LoginForm(request.POST)
    #     if form.is_valid():
    #         username = form.cleaned_data.get('username')
    #         password = form.cleaned_data.get('password')
    #
    #         if username or password:
    #             user = authenticate(username=username, password=password)
    #             if not user.check_password(password):
    #                 raise forms.ValidationError("این رمز اشتباه است !")
    #             login(request, user)
    #             return redirect('/contact')
    #
    # else:
    #     form = LoginForm()
    # return render(request, 'registration/login.html', {'form': form})


@login_required(login_url='/')
def user_logout(request):
    logout(request)
    return redirect('/')


@login_required(login_url="/contact")
def PasswordChangeView(request):
    if request.method == "POST":

        user = request.user

        myuser = User.objects.get(id=user.id)

        form = ChangePasswordForm(request.POST,user=request.user)
        if form.is_valid():
            # form.clean_old_password(request.user)
            cd = form.cleaned_data
            old_password = cd['old_password']
            new_password1 = cd['new_password1']
            new_password2 = cd['new_password2']

            if not myuser.check_password(old_password):
                raise forms.ValidationError('رمز قدیمی شما اشتباه وارد شده است!')

            if new_password1 != new_password2:
                raise forms.ValidationError('تایید رمز شما اشتباه است!')


            myuser.set_password(new_password1)
            login(request, myuser)
            myuser.save()

            return redirect('/contact')
    else:
        form = ChangePasswordForm(user=request.user)
    return render(request, 'registration/change_password.html', {'form': form})

# register user
@logout_required(logout_url='/contact')
def register_user(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username = username, password = password)
            login(request,user)
            return redirect('index')

    else:
        form = NewUserForm()
    return render(request, 'templates/registration/register.html', {'form':form})




def error_404_view(request, exception):
    return render(request, 'not-found.html')

def error_500(request):
    return render(request, '500.html')