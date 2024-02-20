from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('', views.landing, name='landingpage'),
    path('website/', views.home, name='home'),
    
    
    path('customersignup', views.consumer_signup_view,name='consumer-signup'),
    #path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('record/<int:pk>', views.customer_record, name='record'),
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    path('add_record/', views.add_record, name='add_record'),
    path('update_record/<int:pk>', views.update_record, name='update_record'),
    path('update_category/<str:pk>', views.update_category, name='update-category'),
    path('update_product/<int:pk>', views.update_product, name='update-product'),
    path('update_dealer/<str:pk>', views.update_dealer, name='update-dealer'),
    path('update_consumer/<str:pk>', views.update_consumer, name='update-consumer'),
    path('update_order/<int:pk>', views.update_consumer, name='update-order'),
    path('delete_category/<str:pk>', views.delete_category, name='delete-category'),
    path('add_category/', views.add_category, name='add_category'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_dealer/', views.add_dealer, name='add_dealer'),
    path('add_order/', views.add_order, name='add_order'),
    path('add_consumer/', views.add_consumer, name='add_consumer'),
    path('dashboard/', views.AdminDashboardView, name='admin-dashboard'),
    path('product-categories/', views.ProductCategoryListView, name='product-category-list'),
    path('ProductListView/', views.ProductListView, name='product-list'),
    path('DealerListView/', views.DealerListView, name='dealer-list'),   
    path('OrderListView/', views.OrderListView, name='order-list'), 
    path('ConsumerListView/', views.ConsumerListView, name='consumer-list'), 
    # path('filter_by_color/', views.filter_by_color, name='filter_by_color'),
    path('filter_by_color_dealer/', views.filter_by_color_dealer, name='filter_by_color_dealer'),
    path('filter_by_gender/', views.filter_by_gender, name='filter_by_gender'),
    path('plot_3d/', views.plot_3d, name='plot_3d'),
    path('gothere/', views.gothere, name='gothere'),
    path('simple_upload/', views.simple_upload, name='simple_upload'),

    
path('my-order', views.my_order_view,name='my-order'),

        path('normal_user_landing/', views.normal_user_landing, name='normal-user'),
        # path('is_customer/', views.is_customer, name='is_customer'),
        path('afterlogin/', views.afterlogin_view, name="afterlogin"),
        path('customerlogin/', LoginView.as_view(template_name='platform/customerlogin.html'),name='customerlogin'),

path('customer-home', views.customer_home_view,name='customer-home'),
# path('payment-success', views.payment_success_view,name='payment-success'),
path('customer-address', views.customer_address_view,name='customer-address'),

path('add-to-cart/<int:pk>', views.add_to_cart_view,name='add-to-cart'),
path('cart', views.cart_view,name='cart'),
path('remove-from-cart/<int:pk>', views.remove_from_cart_view,name='remove-from-cart'),

path('search', views.search_view,name='search'),

path('product_image/<int:pk>/', views.view_product_image, name='view-product-image'),



# *************************************************
    #     path('admin-view-booking', views.admin_view_booking_view,name='admin-view-booking'),
    #     path('delete-order/<int:pk>', views.delete_order_view,name='delete-order'),
    # path('update-order/<int:pk>', views.update_order_view,name='update-order'),


    # path('customersignup', views.customer_signup_view),
    # path('customerlogin', LoginView.as_view(template_name='ecom/customerlogin.html'),name='customerlogin'),
    # path('customer-home', views.customer_home_view,name='customer-home'),
    # path('my-order', views.my_order_view,name='my-order'),
    # path('my-order', views.my_order_view2,name='my-order'),
    # # path('my-profile', views.my_profile_view,name='my-profile'),
    # path('edit-profile', views.edit_profile_view,name='edit-profile'),
    # path('download-invoice/<int:orderID>/<int:productID>', views.download_invoice_view,name='download-invoice'),


    # path('add-to-cart/<int:pk>', views.add_to_cart_view,name='add-to-cart'),
    # path('cart', views.cart_view,name='cart'),
    # path('remove-from-cart/<int:pk>', views.remove_from_cart_view,name='remove-from-cart'),
    # path('customer-address', views.customer_address_view,name='customer-address'),
    # path('payment-success', views.payment_success_view,name='payment-success'),






]

