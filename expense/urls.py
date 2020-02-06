from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('new-account/',
         views.create_account,
         name='create-account'),
    path('account-detail/<int:a_id>/',
         views.account_detail,
         name='account-detail'),
    path('account-detail/<int:a_id>/more/',
         views.account_detail_divided,
         name='account-detail-divided'),
    path('delete-account/<int:a_id>/',
         views.delete_account,
         name='delete-account'),

    path('account-detail/<int:a_id>/new-income/',
         views.create_income,
         name='create-income'),
    path('update-income/<int:a_id>/<int:i_id>/',
         views.update_income,
         name='update-income'),
    path('delete-income/<int:a_id>/<int:i_id>/',
         views.delete_income,
         name='delete-income'),

    path('account-detail/<int:a_id>/new-spending/',
         views.create_spending,
         name='create-spending'),
    path('update-spending/<int:a_id>/<int:s_id>/',
         views.update_spending,
         name='update-spending'),
    path('delete-spending/<int:a_id>/<int:s_id>/',
         views.delete_spending,
         name='delete-spending'),
]
