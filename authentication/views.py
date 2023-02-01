from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
# this library will be used for displaying messages to the user when the has signed up
from django.contrib import messages
# this library will allow us to redirect the user to the login page after they have registered
from django.shortcuts import redirect, render
# used for authenticating the user by checking the details enterred and comparing them with those in the database
# login and logout is also imported for the login and logout operations
from django.contrib.auth import authenticate, login, logout
# for emails:
from django.core.mail import send_mail, EmailMessage, send_mail
from Revision_web_app import settings
# used for getting the current url of where the site is hosted e.g. localhost
from django.contrib.sites.shortcuts import get_current_site
# for rendering templates inside an email:
from django.template.loader import render_to_string
# for decoding and encoding unique tokens:
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
# for generating tokens:
from .tokens import generate_token


# Create your views here.


def home(request):
    return render(request, "authentication/index.html")


def signup(request):
    if request.method == "POST":
        #username = request.POST.get('username')
        # type the 'name' of the value you want from the signup.html form
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # VALIDATION
        if User.objects.filter(username=username):
            messages.error(
                request, "Username already exists! Please try again")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request, "Email already registered!")
            return redirect('home')

        # length of username = 10 characters
        if len(username) > 10:
            messages.error(request, 'Username must be under 10 characters!')

        # mathcing the 2 passwords (password and confirm password)
        if pass1 != pass2:
            messages.error(request, "Passwords didn't match!")

        # username must be alphanumeric (letter can only contain letter and numbers)
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!")
            return redirect('home')

        # creating a user object
        # this line creates a new user with the 3 important details listed inside the bracket
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname  # passing in the user's first name
        myuser.last_name = lname  # passing in the user's last name
        myuser.is_active = False  # makes sure that the user account is deactivated

        # saving this user in the database
        myuser.save()
        # giving the user a message
        messages.success(
            request, "Your account has been successfully created. We have sent you a confirmation email, please confirm your email in order to activate your account.")

        # SENDING THE WELCOME EMAIL
        subject = "Welcome to Revision Website Login!!"
        message = "Hello " + myuser.first_name + "!! \n Welcome to Revision Website \n Thank you for visiting our website \n We have also sent you a confirmation email, please confirm your email address in order to activate your account. \n\n Thank you \n Arnav"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        # fail_silently prevents our website from crashing if there's an error in sending the email
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Email Address Confirmation Email
        # "current_site" gets the domain of where our website is deployed e.g. localhost
        current_site = get_current_site(request)
        email_subject = "Confirm your email @ Revsision Website Login!!"
        message2 = render_to_string('email_confirmation.html', {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser),
        })
        # creating the email object
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        # if email fails:
        email.fail_silently = True
        email.send()

        # after the user has registerred he/she should be directed to the login page
        return redirect('signin')

    return render(request, "authentication/signup.html")


def signin(request):

    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        # authenticating this user

        user = authenticate(username=username, password=pass1)

        if user is not None:  # this will return a None response if the user is not authenticated and
            # a non None response if the user has enterred the right credentials
            # if the user's credentials are already in our database then we will login
            login(request, user)
            fname = user.first_name  # defining fname
            # a dictionary (context) is also passed in the line below and it contains the firstname of the user
            return render(request, "authentication/index.html", {'fname': fname})

        # what happens if the user's unsuccessful in login
        else:
            messages.error(request, "Bad credentials!")
            return redirect('home')

    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')

# making a function to activate the account of the user:


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request, 'activation_failed.html')
