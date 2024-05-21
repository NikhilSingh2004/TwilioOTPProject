from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from core.forms import UserRegistrationForm, UserAuthenticationForm, OTPValidationForm
from django.contrib import messages
from core.models import User
from django.http import HttpResponseRedirect
import random
from core.mixins import SendSMS

def generate_otp(user):
    otp = random.randint(100000, 999999)
    user.user_otp = otp
    user.save()

    sms = SendSMS(user=user).send_message()

def get_user(user_uuid):
    try:
        return User.objects.get(user_uuid=user_uuid)
    except User.DoesNotExist:
        return False
    except Exception as e:
        print(e.__str__())
        return False

class Home(TemplateView):
    def get(self, request):
        context = {
            'sign_log' : True
        }
        if request.user.is_authenticated:
            context = {
                'sign_log' : False,
                'loged_in' : True
            }
        return render(request, 'core/home.html', context)

class SignUp(TemplateView):
    template_name = 'core/signup.html'

    def get(self, request):
        if request.user.is_authenticated:
            messages.warning(request, "Already Have an Account")
            return render(request, 'core/Home.html')
        context = {
            'form': UserRegistrationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        try:
            form = UserRegistrationForm(data=request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password1'])  # Hash the password
                user.save()
                return HttpResponseRedirect('/login/')  # Change 'login' to the actual name of your login URL
            else:
                messages.error(request, "Form Not Valid")
            return render(request, self.template_name, {'form': form})
        except Exception as e:
            print(e.__str__())
            messages.error(request, "Something Went Wrong")
            return render(request, self.template_name, {'form': form})

class LogIn(TemplateView):

    template_name = 'core/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            messages.warning(request, "Already LogIn")
            return render(request, 'core/Home.html')
        context = {
            'form' : UserAuthenticationForm()
        }
        return render(request, 'core/login.html', context)

    def post(self, request):
        context = {
            'form' : UserAuthenticationForm()
        }
        try:
            print("1")
            form = UserAuthenticationForm(data=request.POST)
            if form.is_valid():
                print("2")
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    generate_otp(user)
                    return HttpResponseRedirect(f'/otp/{user.user_uuid}')
                else:
                    messages.error(request, "Invalid username or password")
            else:
                messages.error(request, "Form not valid")
            return render(request, self.template_name, {'form': form})
        except Exception as e:
            print(e.__str__())
            messages.error(request, "Something Went Wrong!")
            return render(request, self.template_name, context)

class OTP(TemplateView):

    def get(self, request, uid=None):
        context = {
            'form' : OTPValidationForm(),
            'uid' : uid
        }
        return render(request, 'core/otp.html', context)

    def post(self, request, uid=None):
        context = {
            'form' : OTPValidationForm(),
            'uid' : uid
        }
        try:
            form = OTPValidationForm(data=request.POST)
            if form.is_valid():
                otp = form.cleaned_data['otp']
                print(otp)

                user = get_user(user_uuid = uid)
                print(user)

                if user.user_otp == otp:
                    print("True")
                    login(request, user)
                messages.success(request, "OTP LogIn Successful")
                return HttpResponseRedirect('/profile/')

            messages.error(request, "OTP Not Valid")
            return render(request, 'core/otp.html', context)
        except Exception as e:
            print(e.__str__())
            messages.error(request, "Something Went Wrong!")
            return render(request, 'core/otp.html', context)

class UserHome(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'core/profile.html')
        else :
            return HttpResponseRedirect('/login/')