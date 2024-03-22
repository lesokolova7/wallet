from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="login"),
    path("signup", views.sign_up, name="signup"),
    path("home", views.home, name="home"),
    path("delete_wallet/<int:wallet_id>/", views.delete_wallet, name="delete_wallet"),
    path("create_wallet", views.create_wallet, name="create_wallet"),
    path("transaction", views.make_transaction, name="make_transaction"),
    path('make_transaction/<str:sender_wallet_name>/', views.make_transaction, name='make_transaction'),
    path('transaction_success/', views.transaction_success, name='transaction_success'),
    path('transaction_failed/', views.transaction_failed, name='transaction_failed')
]
