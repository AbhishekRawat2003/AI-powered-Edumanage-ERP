# from django.contrib.auth.backends import ModelBackend
# from django.contrib.auth import get_user_model

# class EmailBackend(ModelBackend):
#     def authenticate(self,email =None,
#                      password = None,**kwargs):
#         userModel = get_user_model()
#         try:
#             user = userModel.objects.get(email = email)
#         except userModel.DoesNotExist:
#             return None

#         if user.check_password(password):
#                 return user
#         return None

#     def get_user(self, user_id):
#         UserModel = get_user_model()
#         try:
#             return UserModel.objects.get(pk=user_id)
#         except UserModel.DoesNotExist:
#             return None


from django.contrib.auth.backends import ModelBackend
from .models import CustomUser

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(email=username)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None
