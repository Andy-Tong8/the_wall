from django.urls import path
from . import views


urlpatterns = [
    path('',views.index),
    path('logout/',views.logout),
    path('post_message/',views.post_message),
    path('post_comment/<int:userid>/<int:msgid>/',views.post_comment),
    # path('logout',views.logout),
    # path('success',views.success),
]