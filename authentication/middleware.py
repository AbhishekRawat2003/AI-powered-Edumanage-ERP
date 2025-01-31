from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.shortcuts import redirect

class LoginCheckMiddleWare(MiddlewareMixin):
    def process_view(self,request,view_func,view_args,view_kwargs):
        modulename = view_func.__module__
        user = request.user
        if user.is_activated():
            if user .user_type=='1': #HOD/ADMIN
                if modulename =='stduentViews': #edit this
                    return redirect(reverse('admin+home')) #edit this
                elif user.user_type =='2': #faculty
                    if modulename == 'student views' or modulename =='hod_views' : # edit this
                        return redirect(reverse('staff_home'))
                elif user.user_type =='3':
                    if modulename == 'hod_views' or modulename == 'staff_views': #edit this
                        return redirect(reverse('studet_home')) #edit this
                else :# None of the aforementioned ? Please take the user to login page
                    return redirect(reverse('login_page'))
        else:
            if request.path == reverse('login page') or modulename == 'django.contrib.auth.views' or request.path ==reverse('user_login'): #edit this,If the path is login or has anything to do with authentication, pass
                pass
            else:
                return(redirect('login_page'))