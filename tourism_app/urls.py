from django.urls import path
from django.conf import settings
from django.conf.urls import url, include
from database import views as database_views
from user import views as user_views
from customer import views as customer_views
from admin import views as admin_views
from recommender import views as recommender_views

urlpatterns = [

    # CUSTOMER
    url(r'^user_sign_in/', customer_views.customerSignin, name="user_sign_in"),
    url(r'^add_user/', customer_views.customerSignup, name="add_user"),

    # ADMIN
    url(r'^admin_sign_in/', admin_views.adminSignin, name="admin_sign_in"),

    # Database
    url(r'^database_commit/', database_views.database_commit, name="database_commit"),

    url(r'^hotel_dashboard/', recommender_views.getHotelDashboard, name='hotel_dashboard'),
    url(r'^hotel_search_country/', recommender_views.getHotelOnCountry, name='hotel_search_country'),
    url(r'^hotel_search_name/', recommender_views.getHotelOnName, name='hotel_search_name'),
    url(r'^get_specific_hotel_reviews/', recommender_views.getHotelReviews, name='get_specific_hotel_reviews'),
    url(r'^set_hotel_recommendations/', recommender_views.setHotelRecommends, name='set_hotel_recommendations'),


    #Other
    # url(r'^test/', user_views.testCall, name="test"),
    # url(r'^load_test_server/', user_views.loadTestServer, name="load_test_server"),
    # url(r'^server/', user_views.server, name="server"),
    # url(r'^table_name/', user_views.getDatabaseTableList, name="table_name"),
]
