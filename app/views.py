# django imports
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as loginUser, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# app imports
from app.forms import TopSecretForm
from app.models import TopSecret

# Send Email imports
from django.core.mail import EmailMessage
from django.conf import settings
import socket

# Encode and decode imports
import base64
import random
import string
from django.contrib import messages

# > Disaply home ONLY when login is done
@login_required(login_url="login")  # decorator
def home(request):
    if request.user.is_authenticated:
        user = request.user
        print(f"ddddduser{user}")
        form = TopSecretForm()
        TopSecrets = TopSecret.objects.filter(user=user)

        user = User.objects.get(username=user)
        last_login = user.last_login
        print("sdfsdf", last_login)

        return render(
            request,
            "index.html",
            context={
                "form": form,
                "TopSecrets": TopSecrets,
                "user": user,
                "last_login": last_login,
            },
        )


# > Login function
def login(request):
    if request.method == "GET":
        form = AuthenticationForm()
        context = {"form": form}
        return render(request, "login.html", context=context)
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user_email = request.POST.get("email")
            print(user_email)
            user = authenticate(username=username, password=password)

            print("USERNAME : ", username)
            print("password", password)

            # get hostname and IP address
            hostname = socket.gethostname()
            IPAddr = socket.gethostbyname(hostname)

            # send an email to  user
            email = EmailMessage(
                " LoggedIn Activity. Was it you?",
                f"User has been logged in by {username}. \n Host Name : {hostname} \n IP Address : {IPAddr} \n Email will be send whenever loggedin to website. It is just a security check. \n 🔒 TopSecrete \n \n Note: Please do not reply to this email as this e-mail is system generated.",
                settings.EMAIL_HOST_USER,
                [user_email],
            )
            email.fail_silently = False
            email.send()

            # For session
            if user is not None:
                loginUser(request, user)
                return redirect("home")
        else:
            context = {"form": form}
            return render(request, "login.html", context=context)


# > Signup function
def signup(request):
    if request.method == "GET":
        form = UserCreationForm()
        context = {"form": form}
        return render(request, "signup.html", context=context)

    else:
        form = UserCreationForm(request.POST)
        context = {"form": form}
        if form.is_valid():
            user = form.save()

            user_email = request.POST.get("email")
            email = EmailMessage(
                "✅ Account created successfully @TopSecrete!",
                f" Thankyou {user} for Trusting TopSecrete. \n\n Note : \n - Email will be send whenever loggedin to website. It is just a security check. \n -   Please do not reply to this email as this e-mail is system generated. \n\n 🔒 TopSecrete",
                settings.EMAIL_HOST_USER,
                [user_email],
            )
            email.fail_silently = False
            email.send()

            if user is not None:
                return redirect("home")
        else:
            return render(request, "signup.html", context=context)


# > Add TopSecret function
# decorator - Only adds TopSecret if login is done
@login_required(login_url="login")
def add_TopSecret(request):
    if request.user.is_authenticated:
        user = request.user
        print(user)
        form = TopSecretForm(request.POST)
        if form.is_valid():

            TopSecret = form.save(commit=False)

            TopSecret_password_field = form.cleaned_data["password"]  # plain password
            TopSecret.user = user

            # -- Password encoding --
            password = TopSecret_password_field.encode("utf-8")

            encoded = base64.b64encode(password)
            x = str(encoded, "UTF8")
            print("encoded", x)

            S = 10
            create_random_string = "".join(
                random.choices(string.ascii_uppercase + string.digits, k=S)
            )
            len_c = len(create_random_string)

            final_encoded_string = f"{create_random_string}{x}{create_random_string}"
            print("Final_encoded_string", final_encoded_string)

            TopSecret.password = final_encoded_string
            TopSecret.save()

            return redirect("home")
        else:
            print("ELSE")
            return render(request, "index.html", context={"form": form})


# > Delete TopSecret
def delete_TopSecret(request, id):
    TopSecret.objects.get(pk=id).delete()
    return redirect("home")


# > Signout function
def signout(request):
    logout(request)
    return redirect("login")


# > Decoding function
def encoded_password(request):
    if request.method == "POST":
        name_encoded_password = request.POST.get("name_plain_password")

        try:
            to_slice = name_encoded_password[10:-10]  # slicing the length

            decoded = base64.b64decode(to_slice)
            final_decoded = str(decoded, "UTF8")
            decoded_message = f"Decrypted Password is : {final_decoded}"
            messages.success(request, decoded_message)
            print("final_decoded", final_decoded)
            return redirect("home")

        except UnicodeDecodeError:
            error_message = "Re-paste correctly!"
            messages.error(request, error_message)
            return redirect("home")
    else:
        return redirect("home")


# details

def details_view(request):
    return render(request, "details.html")
