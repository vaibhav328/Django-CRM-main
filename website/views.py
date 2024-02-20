from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import plotly
from .forms import SignUpForm, AddRecordForm , addcategoryform, addproductform, adddealerform, addorderform,addconsumerform
from .models import *
from django.views import View
from django.template.loader import render_to_string
from django.db.models import Q
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.decorators.cache import cache_control
from django.http import JsonResponse
from .resources import *
from tablib import Dataset



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
	records = Record.objects.all()
	# Check to see if logging in
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		# Authenticate
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			request.session.set_expiry(0)
			messages.success(request, "You Have Been Logged In!")
			return redirect('home')
		else:
			messages.success(request, "There Was An Error Logging In, Please Try Again...")
			return redirect('home')
	else:
		return render(request, 'home.html', {'records':records})


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def logout_user(request):
	logout(request)
	request.session.flush()
	messages.success(request, "You Have Been Logged Out...")
	return redirect('landingpage')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			request.session.set_expiry(0)
			messages.success(request, "You Have Successfully Registered! Welcome!")
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'register.html', {'form':form})

	return render(request, 'register.html', {'form':form})



def customer_record(request, pk):
	if request.user.is_authenticated:
		# Look Up Records
		customer_record = Record.objects.get(id=pk)
		return render(request, 'record.html', {'customer_record':customer_record})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')

def category_rec(request, pk):
	if request.user.is_authenticated:
		# Look Up Records
		category_rec = Record.objects.get(name=pk)
		return render(request, 'product_categories.html', {'category_rec':category_rec})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')



def delete_record(request, pk):
	if request.user.is_authenticated:
		delete_it = Record.objects.get(id=pk)
		delete_it.delete()
		messages.success(request, "Record Deleted Successfully...")
		return redirect('home')
	else:
		messages.success(request, "You Must Be Logged In To Do That...")
		return redirect('home')


def add_record(request):
	form = AddRecordForm(request.POST or None)
	if request.user.is_authenticated:
		if request.method == "POST":
			if form.is_valid():
				add_record = form.save()
				messages.success(request, "Record Added...")
				return redirect('home')
		return render(request, 'add_record.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')



def update_record(request, pk):
	if request.user.is_authenticated:
		current_record = Record.objects.get(id=pk)
		form = AddRecordForm(request.POST or None, instance=current_record)
		if form.is_valid():
			form.save()
			messages.success(request, "Record Has Been Updated!")
			return redirect('home')
		return render(request, 'update_record.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')
	



	
def AdminDashboardView(request):
	if request.user.is_authenticated:
		total_orders = Order.objects.count()
		total_consumers = Consumer.objects.count()
		total_categories= ProductCategory.objects.count()
		total_products=Product.objects.count()
		return render(request, 'dashboard.html', {'total_orders': total_orders, 'total_consumers': total_consumers,'total_categories':total_categories,'total_products':total_products})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')
	


# category related views
def ProductCategoryListView(request):
	if request.user.is_authenticated:
		product_categories = ProductCategory.objects.all()
		return render(request, 'product_categories.html', {'product_categories': product_categories})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')	

def delete_category(request, pk):
    if request.user.is_authenticated:
        category = ProductCategory.objects.get(pk=pk)
        if request.method == "POST":
            category.delete()
            messages.success(request, "Category has been deleted!")
            return redirect('product-category-list')
        return render(request, 'product_categories.html', {'category': category})
    else:
        messages.success(request, "You must be logged in to perform this action.")
        return redirect('home')


def update_category(request, pk):
    if request.user.is_authenticated:
        current_category = ProductCategory.objects.get(name=pk)
        form = addcategoryform(request.POST or None, instance=current_category)
        
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Record Has Been Updated!")
                return redirect('product-category-list')

        return render(request, 'update_category.html', {'form': form, 'categories': [current_category]})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')


def gothere(request):
	if request.user.is_authenticated:
		return redirect('update-category')
	
def add_category(request):
	form =addcategoryform(request.POST)
	if request.method == "POST":
		if form.is_valid():
			add_category = form.save()
			messages.success(request, "Record Added...")
			return redirect('product-category-list')
	return render(request, 'add_category.html', {'form': form})

# product related views

	
def ProductListView(request):
	if request.user.is_authenticated:
		# Look Up Records
		products = Product.objects.all()
		colors = Product.objects.values_list('color', flat=True).distinct()
		dealer_name=Product.objects.values_list('dealer', flat=True).distinct()
		# costs=Product.objects.values_list('cost',flat=True)
		genders=Product.objects.values_list('gender',flat=True).distinct()
		categories=Product.objects.values_list('category',flat=True).distinct()
		context = {
            'products': products,
            'colors': colors,
			'dealer_name':dealer_name,
			'genders': genders,
			'categories':categories,
        }
		return render(request, 'products1.html',  context)
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')
	

	
def product_record(request, pk):
	if request.user.is_authenticated:
		# Look Up Records
		product_record = Product.objects.get(id=pk)
		return render(request, 'products1.html', {'product_record':product_record})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')
	
# def update_product(request, pk):
#     if request.user.is_authenticated:
#         current_product = Product.objects.get(pk=pk)
#         form = addproductform(request.POST or None, instance=current_product)
        
#         if request.method == "POST":
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, "Product Has Been Updated!")
#                 return redirect('product-list')

#         return render(request, 'update_product.html', {'form': form, 'products': [current_product]})
#     else:
#         messages.success(request, "You Must Be Logged In...")
#         return redirect('home')

def update_product(request, pk):
    if request.user.is_authenticated:
        current_product = Product.objects.get(pk=pk)

        if request.method == "POST":
            form = addproductform(request.POST, request.FILES, instance=current_product)
            if form.is_valid():
                form.save()
                messages.success(request, "Product Has Been Updated!")
                return redirect('product-list')
        else:
            form = addproductform(instance=current_product)

        return render(request, 'update_product.html', {'form': form, 'products': [current_product]})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')

	



# def filter_by_color(request):
# 	if request.user.is_authenticated:
# 		selected_color = request.GET.get('color', None)
		
# 		if selected_color:
# 			filtered_products = Product.objects.filter(color=selected_color)
# 		else:
# 			filtered_products = Product.objects.all()

# 		data = render_to_string('products1.html', {'products': filtered_products})
# 		return JsonResponse({'data': data})
	
def filter_by_color_dealer(request):
	if request.user.is_authenticated:
     
			filters = {}

			selected_color = request.GET.get('color', None)
			selected_dealer = request.GET.get('dealer', None)
			selected_gender = request.GET.get('gender', None)
			selected_category = request.GET.get('category', None)

			if selected_color:
				filters['color'] = selected_color
			if selected_dealer:
				filters['dealer'] = selected_dealer
			if selected_gender:
				filters['gender'] = selected_gender
			if selected_category:
				filters['category'] = selected_category

			filtered_products = Product.objects.filter(**filters)

			data = render_to_string('products.html', {'products': filtered_products})
			return JsonResponse({'data': data})
	else:
		return JsonResponse({'error': 'User is not authenticated'})

# def add_product(request):
# 	form = addproductform(request.POST or None)
# 	if request.user.is_authenticated:
# 		if request.method == "POST":
# 			if form.is_valid():
# 				add_product = form.save()
# 				messages.success(request, "Record Added...")
# 				return redirect('product-list')
# 		return render(request, 'add_product.html', {'form':form})
# 	else:
# 		messages.success(request, "You Must Be Logged In...")
# 		return redirect('home')

def add_product(request):
    if request.method == 'POST':
        form = addproductform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirect to a success page or another view
            return redirect('product-list')
    else:
        form = addproductform()

    return render(request, 'add_product.html', {'form': form})
	






	



# dealer realted views
def DealerListView(request):
	if request.user.is_authenticated:
		# Look Up Records
		dealers = Dealer.objects.all()
		return render(request, 'dealers.html', {'dealers':dealers})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')
	
def add_dealer(request):
	form = adddealerform(request.POST or None)
	if request.user.is_authenticated:
		if request.method == "POST":
			if form.is_valid():
				add_dealer = form.save()
				messages.success(request, "Record Added...")
				return redirect('home')
		return render(request, 'add_dealer.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')
	
def dealer_record(request, pk):
	if request.user.is_authenticated:
		# Look Up Records
		dealer_record = Dealer.objects.get(id=pk)
		return render(request, 'dealers.html', {'dealer_record':dealer_record})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')
	
def update_dealer(request, pk):
    if request.user.is_authenticated:
        current_dealer = Dealer.objects.get(pk=pk)
        form = adddealerform(request.POST or None, instance=current_dealer)
        
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Dealer Has Been Updated!")
                return redirect('dealer-list')

        return render(request, 'update_dealer.html', {'form': form, 'dealers': [current_dealer]})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')




	
# orders related views
def order_record(request, pk):
	if request.user.is_authenticated:
		# Look Up Records
		order_record = Order.objects.get(oid=pk)
		return render(request, 'orders.html', {'order_record':order_record})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')





def OrderListView(request):
	if request.user.is_authenticated:
		# Look Up Records
		orders = Order.objects.all()
		return render(request, 'orders.html', {'orders':orders})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")

def add_order(request):
	form = addorderform(request.POST or None)
	if request.user.is_authenticated:
		if request.method == "POST":
			if form.is_valid():
				add_order = form.save()
				messages.success(request, "Record Added...")
				return redirect('home')
		return render(request, 'add_order.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')
	
def update_order(request, pk):
    if request.user.is_authenticated:
        current_order = Order.objects.get(pk=pk)
        form = addorderform(request.POST or None, instance=current_order)
        
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Order Has Been Updated!")
                return redirect('order-list')

        return render(request, 'update_order.html', {'form': form, 'orders': [current_order]})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')





# consumer related views

def consumer_record(request, pk):
	if request.user.is_authenticated:
		# Look Up Records
		consumer_record = Consumer.objects.get(id=pk)
		return render(request, 'consumers.html', {'consumer_record':consumer_record})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')
	


def add_consumer(request):
	form = addconsumerform(request.POST or None)
	if request.user.is_authenticated:
		if request.method == "POST":
			if form.is_valid():
				add_consumer = form.save()
				messages.success(request, "Record Added...")
				return redirect('home')
		return render(request, 'add_consumer.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')
	
def ConsumerListView(request):
	if request.user.is_authenticated:
		# Look Up Records
		consumers = Consumer.objects.all()

		genders=Consumer.objects.values_list('gender',flat=True).distinct()

		context = {
            'consumers': consumers,
			'genders': genders,
        }
		return render(request, 'consumers.html',  context)
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')


def filter_by_gender(request):
	if request.user.is_authenticated:
			filters = {}


			selected_gender = request.GET.get('gender', None)

			if selected_gender:
				filters['gender'] = selected_gender

			filtered_consumers = Consumer.objects.filter(**filters)

			data = render_to_string('consumers1.html', {'consumers': filtered_consumers})
			return JsonResponse({'data': data})
	else:
		return JsonResponse({'error': 'User is not authenticated'})
	

def update_consumer(request, pk):
    if request.user.is_authenticated:
        current_consumer = Consumer.objects.get(pk=pk)
        form = addconsumerform(request.POST or None, instance=current_consumer)
        
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Consumer Has Been Updated!")
                return redirect('consumer-list')

        return render(request, 'update_consumer.html', {'form': form, 'consumers': [current_consumer]})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')

	


def plot_3d(request):

    x_data = [1, 2, 3, 4, 5]
    y_data = [10, 11, 12, 13, 14]
    z_data = [20, 21, 22, 23, 24]

  
    fig = go.Figure(data=[go.Scatter3d(x=x_data, y=y_data, z=z_data, mode='markers')])

 
    plot_html = fig.to_html(full_html=False)

    return render(request, 'dashboard.html', {'plot_html': plot_html})

# import plotly.express as px
from plotly.offline import plot
import plotly.graph_objects as go

from . import forms
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect,HttpResponse
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def consumer_signup_view(request):
    userForm = forms.CustomerUserForm()
    customerForm = forms.CustomerForm()
    mydict = {'userForm': userForm, 'customerForm': customerForm}
    
    if request.method == 'POST':
        userForm = forms.CustomerUserForm(request.POST)
        customerForm = forms.CustomerForm(request.POST, request.FILES)
        
        if userForm.is_valid() and customerForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            
            customer = customerForm.save(commit=False)
            customer.user = user
            customer.save()
            
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
            
            return HttpResponseRedirect('customerlogin')  # Provide the correct URL for the redirect

    return render(request, 'platform/customersignup.html', context=mydict)


# def landing(request):
#     return render(request,'homepage.html')

def normal_user_landing(request):
    return render(request,'platform/customer_home.html')

def is_customer(user):
	return User(username='USERNAME')





@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def afterlogin_view(request):
    if request.user.is_authenticated:
        username=request.user.username
        request.session.set_expiry(0)
        return redirect('customer-home')
    # if is_customer(request.user):
    #     return redirect('customer-home')
    else:
        return redirect('consumer-signup')
    
    
    

    # if request.method == 'POST':
    #     email = request.POST['email']
    #     password = request.POST['password']

    #     user = authenticate(request, email=email, password=password)
    #     print(user)
    #     if user:
    #         login(request,user)
    #         # request.session.set_expiry(settings.SESSION_EXPIRE_AT_BROWSER_CLOSE)
    #         request.session.set_expiry(0)
    #         return redirect('customer-home')
    #     else:
    #         error_message = 'Wrong email or password entered!'
    #         print(error_message)

    # return render(request, 'consumer-signup.html', {'error': error_message})
    
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
def landing(request):
    products=Product.objects.all()
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'platform/index.html',{'products':products,'product_count_in_cart':product_count_in_cart})
    


#for showing login button for admin
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')






@login_required(login_url='customerlogin')
def add_to_cart_view(request, pk):
	products = Product.objects.all()

	# Retrieve or initialize the cart from the session
	cart = request.session.get('cart', [])

	# Add the product id to the cart
	cart.append(pk)

	# Remove duplicates by converting to a set and back to a list
	cart = list(set(cart))

	# Save the updated cart to the session
	request.session['cart'] = cart

	# Get the count of unique products in the cart
	product_count_in_cart = len(cart)
	return render(request, 'platform/index.html', {'products': products, 'product_count_in_cart': product_count_in_cart})

    # product=Product.objects.get(pid=pk)
    # messages.info(request, product.name + ' added to cart successfully!')

    # return response

@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
def cart_view(request):
    # Retrieve or initialize the cart from the session
    cart = request.session.get('cart', [])

    # Get the count of unique products in the cart
    product_count_in_cart = len(cart)

    # Fetch product details from the database whose id is present in the cart
    products = None
    total = 0

    if cart:
        # Fetch products based on the product ids in the cart
        products = Product.objects.filter(pid__in=cart)

        # Calculate total price shown in the cart
        total = sum(product.cost for product in products)

    return render(request, 'platform/cart.html', {'products': products, 'total': total, 'product_count_in_cart': product_count_in_cart})

def remove_from_cart_view(request, pk):
    # Retrieve or initialize the cart from the session
    cart = request.session.get('cart', [])

    # Get the count of unique products in the cart
    product_count_in_cart = len(cart)

    # Removing product id from the cart
    if pk in cart:
        cart.remove(pk)

    # Fetch product details from the database whose id is present in the cart
    products = None
    total = 0

    if cart:
        # Fetch products based on the product ids in the cart
        products = Product.objects.filter(pid__in=cart)

        # Calculate total price shown in the cart
        total = sum(product.cost for product in products)

    # Save the updated cart to the session
    request.session['cart'] = cart

    return render(request, 'platform/cart.html', {'products': products, 'total': total, 'product_count_in_cart': product_count_in_cart})
    
@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def my_profile_view(request):
    customer=Consumer.objects.get(user_id=request.user.id)
    return render(request,'platform/my_profile.html',{'customer':customer})




@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_home_view(request):
    products=Product.objects.all()
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
    return render(request,'platform/customer_home.html',{'products':products,'product_count_in_cart':product_count_in_cart})


def search_view(request):
    # whatever user write in search box we get in query
    query = request.GET['query']
    products=Product.objects.all().filter(name__icontains=query)
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    # word variable will be shown in html when user click on search button
    word="Searched Result :"

    if request.user.is_authenticated:
        return render(request,'platform/customer_home.html',{'products':products,'word':word,'product_count_in_cart':product_count_in_cart})
    return render(request,'platform/index.html',{'products':products,'word':word,'product_count_in_cart':product_count_in_cart})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def my_order_view(request):
    try:
        # Assuming you have a profile field in your User model
        consumer = Consumer.objects.get(email=request.user.email)
        orders = Order.objects.filter(consumer=consumer)
        ordered_products = []

        for order in orders:
            ordered_product = Product.objects.get(pid=order.product.pid)
            ordered_products.append(ordered_product)

        return render(request, 'platform/my_order.html', {'data': zip(ordered_products, orders)})

    except Consumer.DoesNotExist:
 
        messages.error(request, 'Consumer profile not found for the user.')
        return redirect('some_error_view')  
    
    
@login_required(login_url='customerlogin')
def customer_address_view(request):
    # this is for checking whether product is present in cart or not
    # if there is no product in cart we will not show address form
    product_in_cart=False
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
    if product_ids != "":
            product_in_cart=True
    #for counter in cart
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    addressForm = forms.AddressForm()
    if request.method == 'POST':
        addressForm = forms.AddressForm(request.POST)
        if addressForm.is_valid():
            # here we are taking address, email, mobile at time of order placement
            # we are not taking it from customer account table because
            # these thing can be changes
            email = addressForm.cleaned_data['Email']
            mobile=addressForm.cleaned_data['Mobile']
            address = addressForm.cleaned_data['Address']
            #for showing total price on payment page.....accessing id from cookies then fetching  price of product from db
            total=0
            if 'product_ids' in request.COOKIES:
                product_ids = request.COOKIES['product_ids']
                if product_ids != "":
                    product_id_in_cart=product_ids.split('|')
                    products=Product.objects.all().filter(pid__in = product_id_in_cart)
                    for p in products:
                        total=total+p.cost

            response = render(request, 'platform/payment.html',{'total':total})
            response.set_cookie('email',email)
            response.set_cookie('mobile',mobile)
            response.set_cookie('address',address)
            return response
    return render(request,'platform/customer_address.html',{'addressForm':addressForm,'product_in_cart':product_in_cart,'product_count_in_cart':product_count_in_cart})


from django.urls import reverse

def simple_upload(request):
    if request.method == 'POST':
        dataset = Dataset()
        new_category = request.FILES['myfile']

        try:
            imported_data = dataset.load(new_category.read(), format='xlsx')

            for data in imported_data:
             
                value = ProductCategory(
                    data[0],
                    data[1],
                    data[2]
                )
                value.full_clean()
                value.save()

           
            result = ProductCategoryResource().import_data(dataset, dry_run=False)  

            if not result.has_errors():
                return redirect(reverse('product-category-list'))

        except Exception as e:
            
            pass

    return render(request, 'add_category.html')

from django.shortcuts import render, get_object_or_404
def view_product_image(request, pk):
    product = get_object_or_404(Product, pk=pk)
    image_path = product.product_image.path  

    with open(image_path, 'rb') as image_file:
        return HttpResponse(image_file.read(), content_type='image/jpg') 
