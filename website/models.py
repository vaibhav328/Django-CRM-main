from django.db import models

# **********************************************************************************************************************
#  these models are related to admin panel
# ---------------------------------------------------------------------------------------------------------
class Record(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	first_name = models.CharField(max_length=50)
	last_name =  models.CharField(max_length=50)
	email =  models.CharField(max_length=100)
	phone = models.CharField(max_length=15)
	address =  models.CharField(max_length=100)
	city =  models.CharField(max_length=50)
	state =  models.CharField(max_length=50)
	zipcode =  models.CharField(max_length=20)

	def __str__(self):
		return(f"{self.first_name} {self.last_name}")
    

class ProductCategory(models.Model):
    name = models.CharField(max_length=255,primary_key=True)
    description = models.TextField(default='large')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Dealer(models.Model):
    fname=models.CharField(max_length=20)
    lname=models.CharField(max_length=20)
    email=models.EmailField(primary_key=True)
    contact=models.IntegerField()
    address=models.CharField(max_length=400)
    business_name = models.CharField(max_length=255)
    business_gstin = models.CharField(max_length=15)
    product_categories = models.ForeignKey(ProductCategory,on_delete=models.CASCADE, to_field='name')


    def __str__(self):
        return self.fname

class Consumer(models.Model):
    fname=models.CharField(max_length=20)
    lname=models.CharField(max_length=20)
    email=models.EmailField(primary_key=True)
    contact=models.IntegerField()
    address=models.CharField(max_length=400)
    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=gender_choices)
    product_categories = models.ForeignKey(ProductCategory,on_delete=models.CASCADE, to_field='name')

    def __str__(self):
        return self.fname
    
class Product(models.Model):
    pid=models.AutoField(primary_key=True)
    category = models.ForeignKey(ProductCategory,on_delete=models.CASCADE, to_field='name')
    product_image= models.ImageField(upload_to='product_image/',null=True,blank=True)
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE,to_field='email',default='Shop4u')
    name = models.CharField(max_length=255)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=Consumer.gender_choices,null=True)
    # product_image= models.ImageField(upload_to='product_image/',null=True,blank=True)

    def __str__(self):
            return self.color
    
class Order(models.Model):
    oid=models.AutoField(primary_key=True)

    product = models.ForeignKey(Product, on_delete=models.CASCADE,to_field='pid')
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE,to_field='email')
    order_status_choices = [
        ('Ordered', 'Ordered'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    payment_type_choices = [
        ('COD', 'COD'),
        ('ONLINE', 'ONLINE'),
    ]
    payment_status_choices = [
        ('Waiting', 'Waiting'),
        ('Done', 'Done'),
    ]
    order_status = models.CharField(max_length=20, choices=order_status_choices)
    payment_type = models.CharField(max_length=10, choices=payment_type_choices)
    payment_status = models.CharField(max_length=20, choices=payment_status_choices)

# ***************************************************************************************************************

# models for e-commerce website
    
from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect


    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=15)
    address = models.TextField()
    is_dealer = models.BooleanField(default=False)
    is_consumer = models.BooleanField(default=False)
    # cart = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.user.get_full_name()
    
class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('admin-dashboard')
        return render(request, self.template_name, {'form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class SignupView(View):
    template_name = 'signup.html'

    def get(self, request):
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(
                user=user,
                contact=request.POST['contact'],
                address=request.POST['address'],
                is_dealer='is_dealer' in request.POST,
                is_consumer='is_consumer' in request.POST
            )
            login(request, user)
            return redirect('admin-dashboard')
        return render(request, self.template_name, {'form': form})
    
class HomePageView(View):
    template_name = 'home.html'

    def get(self, request):
        return render(request, self.template_name)
