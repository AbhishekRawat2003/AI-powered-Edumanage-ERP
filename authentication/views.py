from django.http import HttpResponse
import json
import requests
from django.contrib import messages
# NEW AUTHENTICATION VIEWS

from django.shortcuts import render, redirect,reverse
from .backends import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def login_page(request):
    if request.user.is_authenticated:
        if request.user.user_type == 1:
            return redirect(reverse("faculty:admin_home"))  # HOD
        elif request.user.user_type == 2:
            return redirect(reverse("faculty:faculty_home"))  # Staff
        else:
            return redirect(reverse("student:student_home"))  # Student
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(f"username is {username} and password is {password}")
        print(user)
        if user is not None:
            login(request, user)
            print(f"Authenticated user: {user.email}, user_type: {user.user_type}")
            if user.user_type == 1:
                return redirect(reverse("faculty:admin_home"))
            elif user.user_type == 2:
                return redirect(reverse("faculty:faculty_home"))
            else:
                return redirect(reverse("student:student_home"))  # Ensure this matches the defined URL
        else:
            return render(request, 'authentication/login.html', {'error': 'Invalid username or password'})
    return render(request, 'authentication/login.html')





def doLogin(request,**kwargs):
    if request.method !='POST':
        return HttpResponse("<h4>Denied<H4>")
    else:
        #google Recaptcha
        captcha_token = request.POST.get('g-recaptcha-response')
        captcha_url = "https://www.google.com/recaptcha/api/siteverify"
        captcha_key = "6LfswtgZAAAAABX9gbLqe-d97qE2g1JP8oUYritJ"
        data = {
            'secret': captcha_key,
            'response': captcha_token
        }
        try:
            captcha_server = requests.post(url=captcha_url,data=data)
            response= json.loads(captcha_server.text)
            if response['sucess']==False:
                messages.error(request,'Invalid Captcha. Try Again')
                return redirect("/")
        except:
            messages.error(request, 'Captcha could not be verified. Try Again')
            return redirect('/')

        #Authenticate
        user = EmailBackend.authenticate(requests,username=requests.POST.get('email'),password=requests.POST.get('password'))

        if user !=None:
            login(requests,user)
            if user.user_type =='1':
                return redirect(reverse("faculty:admin_home"))
            elif request.user.user_type == '2':
                return redirect(reverse("faculty: faculty_home"))
            else:
                return redirect(reverse("student :student_home"))
        else:
            messages.error(request,"invalid details")
            return redirect("/")

@login_required 
def logout_user(request):
    logout(request)  # This will log out the user
    return redirect('/') 


def showFirebaseJS(request):
    data = """
    // Give the service worker access to Firebase Messaging.
// Note that you can only use Firebase Messaging here, other Firebase libraries
// are not available in the service worker.
importScripts('https://www.gstatic.com/firebasejs/7.22.1/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/7.22.1/firebase-messaging.js');

// Initialize the Firebase app in the service worker by passing in
// your app's Firebase config object.
// https://firebase.google.com/docs/web/setup#config-object
firebase.initializeApp({
    apiKey: "AIzaSyBarDWWHTfTMSrtc5Lj3Cdw5dEvjAkFwtM",
    authDomain: "sms-with-django.firebaseapp.com",
    databaseURL: "https://sms-with-django.firebaseio.com",
    projectId: "sms-with-django",
    storageBucket: "sms-with-django.appspot.com",
    messagingSenderId: "945324593139",
    appId: "1:945324593139:web:03fa99a8854bbd38420c86",
    measurementId: "G-2F2RXTL9GT"
});

// Retrieve an instance of Firebase Messaging so that it can handle background
// messages.
const messaging = firebase.messaging();
messaging.setBackgroundMessageHandler(function (payload) {
    const notification = JSON.parse(payload);
    const notificationOption = {
        body: notification.body,
        icon: notification.icon
    }
    return self.registration.showNotification(payload.notification.title, notificationOption);
});
    """
    return HttpResponse(data, content_type='application/javascript')