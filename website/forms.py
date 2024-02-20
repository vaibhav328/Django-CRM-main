from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))


	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	




# Create Add Record Form
class AddRecordForm(forms.ModelForm):
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"First Name", "class":"form-control"}), label="")
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Last Name", "class":"form-control"}), label="")
    email = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Email", "class":"form-control"}), label="")
    phone = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Phone", "class":"form-control"}), label="")
    address = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Address", "class":"form-control"}), label="")
    city = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"City", "class":"form-control"}), label="")
    state = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"State", "class":"form-control"}), label="")
    zipcode = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Zipcode", "class":"form-control"}), label="")

    class Meta:
        model = Record
        exclude = ("user",)

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        # Basic phone number validation
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")

        # Add more phone number validation logic if needed

        return phone

class addcategoryform(forms.ModelForm):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={"placeholder": "Category Name", "class": "form-control"}), label="")
    description = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Description", "class": "form-control"}), label="")
    is_active = forms.BooleanField(initial=True, required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"}), label="Is Active")

    class Meta:
        model = ProductCategory
        fields = ['name', 'description', 'is_active']
    
    def clean_name(self):
        name = self.cleaned_data.get('name')

        if(name.isdigit==True):
             raise forms.ValidationError("category cannot contain digits")
        

    # Basic name validation
        if len(name) < 3:
            raise forms.ValidationError("Category name must be at least 3 characters long.")
        return name

    def clean_description(self):    
        description = self.cleaned_data.get('description')

    # Basic description validation
        if len(description) < 10:
            raise forms.ValidationError("Description must be at least 10 characters long.")
        return description

# class addproductform(forms.ModelForm):
# 	class Meta:
# 		model = Product
# 		fields = ['category', 'dealer', 'name', 'description', 'cost', 'color', 'gender']


        
class adddealerform(forms.ModelForm):
    fname = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "First Name", "class": "form-control"}), label="")
    lname = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Last Name", "class": "form-control"}), label="")
    email = forms.EmailField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Email", "class": "form-control"}), label="")
    contact = forms.IntegerField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Contact", "class": "form-control"}), label="")
    address = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Address", "class": "form-control"}), label="")
    business_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Business Name", "class": "form-control"}), label="")
    business_gstin = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Business GSTIN", "class": "form-control"}), label="")
    
    # Assuming product_categories is a ForeignKey to ProductCategory
    product_categories = forms.ModelChoiceField(queryset=ProductCategory.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), label="Product Category")

    class Meta:
        model = Dealer
        fields = ['fname', 'lname', 'email', 'contact', 'address', 'business_name', 'business_gstin', 'product_categories']
    
    def clean_fname(self):
        fname = self.cleaned_data.get('fname')
        # lname = self.cleaned_data.get('lname')



        if any(char.isdigit() for char in fname):
            raise forms.ValidationError("First name cannot contain digits.")


        # Add more validation logic if needed

        return fname
    def clean_lname(self):
        # fname = self.cleaned_data.get('fname')
        lname = self.cleaned_data.get('lname')

        if not lname:
            raise forms.ValidationError("last name cannot be empty.")

        if any(char.isdigit() for char in lname):
            raise forms.ValidationError("First name cannot contain digits.")


        # Add more validation logic if needed

        return lname
    



        

class addorderform(forms.ModelForm):
    
    product = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), label="Product",to_field_name='pid')


    consumer = forms.ModelChoiceField(queryset=Consumer.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), label="Consumer")

    order_status_choices = [
        ('Ordered', 'Ordered'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    order_status = forms.ChoiceField(choices=order_status_choices, widget=forms.Select(attrs={"class": "form-control"}), label="Order Status")

    payment_type_choices = [
        ('COD', 'COD'),
        ('ONLINE', 'ONLINE'),
    ]
    payment_type = forms.ChoiceField(choices=payment_type_choices, widget=forms.Select(attrs={"class": "form-control"}), label="Payment Type")

    payment_status_choices = [
        ('Waiting', 'Waiting'),
        ('Done', 'Done'),
    ]
    payment_status = forms.ChoiceField(choices=payment_status_choices, widget=forms.Select(attrs={"class": "form-control"}), label="Payment Status")

    class Meta:
        model = Order
        fields = ['product', 'consumer', 'order_status', 'payment_type', 'payment_status']
        

class addconsumerform(forms.ModelForm):
    fname = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "First Name", "class": "form-control"}), label="")
    lname = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Last Name", "class": "form-control"}), label="")
    email = forms.EmailField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Email", "class": "form-control"}), label="")
    contact = forms.IntegerField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Contact", "class": "form-control"}), label="")
    address = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Address", "class": "form-control"}), label="")

    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = forms.ChoiceField(choices=gender_choices, widget=forms.Select(attrs={"class": "form-control"}), label="Gender")

    # Assuming product_categories is a ForeignKey to ProductCategory
    product_categories = forms.ModelChoiceField(queryset=ProductCategory.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), label="Product Category")

    class Meta:
        model = Consumer
        fields = ['fname', 'lname', 'email', 'contact', 'address', 'gender', 'product_categories']

    def clean_fname(self):
        fname = self.cleaned_data.get('fname')
        # lname = self.cleaned_data.get('lname')



        if any(char.isdigit() for char in fname):
            raise forms.ValidationError("First name cannot contain digits.")


        # Add more validation logic if needed

        return fname
    def clean_lname(self):
        # fname = self.cleaned_data.get('fname')
        lname = self.cleaned_data.get('lname')

        if not lname:
            raise forms.ValidationError("last name cannot be empty.")

        if any(char.isdigit() for char in lname):
            raise forms.ValidationError("First name cannot contain digits.")


        # Add more validation logic if needed

        return lname
    

        

class addproductform(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=ProductCategory.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), label="Category")
    dealer = forms.ModelChoiceField(queryset=Dealer.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), label="Dealer")
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={"placeholder": "Product Name", "class": "form-control"}), label="Name")
    description = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Product Description", "class": "form-control"}), label="Description")
    cost = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={"placeholder": "Product Cost", "class": "form-control"}), label="Cost")
    color = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"placeholder": "Product Color", "class": "form-control"}), label="Color")
    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = forms.ChoiceField(choices=gender_choices, widget=forms.Select(attrs={"class": "form-control"}), label="Gender")
    product_image = forms.ImageField(widget=forms.FileInput(attrs={"class": "form-control"}), label="Product Image")

    class Meta:
        model = Product
        fields = ['category', 'dealer', 'name', 'description', 'cost', 'color', 'gender', 'product_image']
    
    def clean_color(self):
        color = self.cleaned_data.get('color')

        if any(char.isdigit() for char in color):
            raise forms.ValidationError("Color cannot contain digits.")
        color = color.lower()

        return color

        

    # Basic name validation







class CustomerUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class CustomerForm(forms.ModelForm):
    
    fname = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"placeholder": "First name", "class": "form-control"}), label="First Name")
    lname = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"placeholder": "Last name", "class": "form-control"}), label="Last Name")
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email", "class": "form-control"}), label="Email")
    contact = forms.IntegerField(widget=forms.NumberInput(attrs={"placeholder": "Contact", "class": "form-control"}), label="Contact")
    address = forms.CharField(max_length=400, widget=forms.TextInput(attrs={"placeholder": "Address", "class": "form-control"}), label="Address")

    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = forms.ChoiceField(choices=gender_choices, widget=forms.Select(attrs={"class": "form-control"}), label="Gender")

    product_categories = forms.ModelChoiceField(queryset=ProductCategory.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), label="Product Category")

    class Meta:
        model=Consumer
        fields=['fname','lname','email','contact','address','gender','product_categories']
        
    def clean_fname(self):
        fname = self.cleaned_data.get('fname')
        # lname = self.cleaned_data.get('lname')



        if any(char.isdigit() for char in fname):
            raise forms.ValidationError("First name cannot contain digits.")


        # Add more validation logic if needed

        return fname
    def clean_email(self):
        email = self.cleaned_data['email']
        if Consumer.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('contact')

        # Basic phone number validation
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")

        # Add more phone number validation logic if needed

        return phone
    
    
    
    def clean_lname(self):
        # fname = self.cleaned_data.get('fname')
        lname = self.cleaned_data.get('lname')

        if not lname:
            raise forms.ValidationError("last name cannot be empty.")

        if any(char.isdigit() for char in lname):
            raise forms.ValidationError("First name cannot contain digits.")


        # Add more validation logic if needed

        return lname
        
        
        
class AddressForm(forms.Form):
    Email = forms.EmailField()
    Mobile= forms.IntegerField()
    Address = forms.CharField(max_length=500)