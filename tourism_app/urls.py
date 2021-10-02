from django.urls import path
from django.conf import settings
from django.conf.urls import url, include
from database import views as database_views
from user import views as user_views
from customer import views as customer_views
from admin import views as admin_views

urlpatterns = [

    # CUSTOMER
    url(r'^user_sign_in/', customer_views.customerSignin, name="user_sign_in"),
    url(r'^add_user/', customer_views.customerSignup, name="add_user"),

    # ADMIN
    url(r'^admin_sign_in/', admin_views.adminSignin, name="admin_sign_in"),

    # Database
    url(r'^database_commit/', database_views.database_commit, name="database_commit"),


    #Other
    url(r'^test/', user_views.testCall, name="test"),
    url(r'^load_test_server/', user_views.loadTestServer, name="load_test_server"),
    url(r'^server/', user_views.server, name="server"),
    url(r'^table_name/', user_views.getDatabaseTableList, name="table_name"),
]
