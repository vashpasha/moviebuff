from django.urls import path
from .views import (
    RegisterView,
    LogOutView,
    UserMeDetailView,
    UserDetailView,
    UserListView,
    UserEditView,
    ChangePasswordView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name="sign_up"),
    path('logout/', LogOutView.as_view(), name="logout"),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('changepass/', ChangePasswordView.as_view(), name='changepass'),

    path('users/self/', UserMeDetailView.as_view(), name='self'),
    path('users/<int:id>/', UserDetailView.as_view(), name='deatail'),
    path('users/', UserListView.as_view(), name=''),
    path('users/self/edit/', UserEditView.as_view(), name=''),
]