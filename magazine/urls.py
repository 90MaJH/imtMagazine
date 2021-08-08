from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.conf.urls import url

from . import views

urlpatterns = [
    # intro
    path('', views.qnas_list, name='qnas_list'),

    # accounts
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('activate/<str:uid64>/<str:token>/', views.activate, name='activate'),
    path('signout/', views.signout, name='signout'),
    path('password_reset/', views.UserPasswordResetView.as_view(), name="password_reset"),
    path('password_reset_done/', views.UserPasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password_reset_complete/', views.UserPasswordResetCompleteView, name="password_reset_complete"),
    path('check_notification/<int:notificationId>', views.check_notification, name='check_notification'),
    path('delete_notification/', views.delete_notification, name='delete_notification'),
    path('myinfo/', views.myinfo, name='myinfo'),
    path('nickname_change/', views.nicknameChange, name='nickname_change'),
    path('message_header/', views.messageHeader, name='message_header'),
    path('message_detail/<int:msg_header_id>/<int:opponent>', views.messageDetail, name='message_detail'),
    path('message_delete/', views.message_delete, name='message_delete'),

    # qnas
    path('imtBoards_write/', views.imtBoards_write, name='imtBoards_write'),
    path('imtBoards_list/', views.imtBoards_list, name='imtBoards_list'),
    path('imtBoards_view/<int:pk>/', views.imtBoards_view, name='imtBoards_view'),
    path('imtBoards_notice_view/<int:pk>/', views.imtBoards_notice_view, name='imtBoards_notice_view'),
    path('imtBoards_modify/<int:postId>', views.imtBoards_modify, name='imtBoards_modify'),

    # qnas
    path('qnas_write/', views.qnas_write, name='qnas_write'),
    path('qnas_list/', views.qnas_list, name='qnas_list'),
    path('qnas_view/<int:pk>/', views.qnas_view, name='qnas_view'),
    path('qnas_notice_view/<int:pk>/', views.qnas_notice_view, name='qnas_notice_view'),
    path('qnas_modify/<int:postId>', views.qnas_modify, name='qnas_modify'),

    # magazines
    path('magazines_list/', views.magazines_list, name='magazines_list'),
    path('magazines_view/<int:pk>/', views.magazines_view, name='magazines_view'),

    # imtsofts
    path('imtsofts_list/', views.imtsofts_list, name='imtsofts_list'),

    # common
    path('checkPassword/', views.checkPassword, name='checkPassword'),
    path('deletePost/', views.deletePost, name='deletePost'),
    path('deleteReply/', views.deleteReply, name='deleteReply'),
    path('summernote/', include('django_summernote.urls')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
