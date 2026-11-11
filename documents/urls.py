from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home,name='home'),
    path('add-document/',views.add_document,name='add_document'),
    path('edit/<int:document_id>/', views.edit_document, name='edit_document'),
    path('delete/<int:document_id>/', views.delete_document, name='delete_document'),
    path('all-documents/', views.all_documents, name='all_documents'),

    path('register/',views.register_view, name='register'),
    path('login/',views.login_view, name='login'),
    path('logout/',views.logout_view, name='logout'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='documents/password_reset.html',  email_template_name='documents/password_reset_email.html', subject_template_name='documents/password_reset_subject.txt', success_url='/password-reset/done/'),name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='documents/password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='documents/password_reset_confirm.html', success_url='/reset/done/'),name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='documents/password_reset_complete.html'),name='password_reset_complete'),
]