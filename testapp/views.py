from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from testapp.forms import SignUpForm
from django.http import HttpResponseRedirect
from testapp.forms import SignUpForm    
from testapp import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Transaction
from testapp.paytm import generate_checksum, verify_checksum

# Create your views here.

English = {'brand_name':'TechnicalBaba','Exam_name':[{'name':'Java Exams'},{'name':'Python Exams'},{'name':'Aptitude Exams'}],'user_action':[{'name':'Signup'},{'name':'Login'},{'name':'Logout'}]}
Hindi = {'brand_name':'तकनीकी बाबा','Exam_name':[{'name':'जावा परीक्षा'},{'name':'पायथन परीक्षा'},{'name':'योग्यता परीक्षा'}],'user_action':[{'name':'साइन अप करें'},{'name':'लॉग इन करें'},{'name':'लॉग आउट'}]}
language = English


def index(request):
    ss=User.objects.filter(id=1)
    print(ss)
    data={'login':True}
    return render(request,'index.html',context=data)
@login_required    
def java(request):
    return render(request,'java.html')    
@login_required
def python(request):
    
    return render(request,'python.html') 
@login_required
def aptitude(request):
    return render(request,'aptitude.html') 

def logout(request):
    return render(request,'logout.html')
    


# def signup(request):
#     form=forms.SignUpForm(request.POST)
#     if request.method=='POST':
#         # username = request.POST['username']
#         # password=request.POST['password']
#         # email=request.POST['email']
#         # first_name= request.POST['first_name']
#         # last_name=request.POST['last_name']
#         user=form.save(commit=True) 
#         user.set_password(user.password)
#         user.save()
        
        
#         form.save()
#         # print(form['password'].value()) 
#         #user=form.save()
#         #print(user) 
#         # user.set_password(user.password)
#         # user.save()
#         #form.save() 

#         return HttpResponseRedirect('/accounts/login')
#     return render(request,'signup.html',{'form':form})


# def signup(request):
#     if request.user.is_superuser:
#         form=SignUpForm()
#      # giving access to superuser only.
    
#     if request.method=='POST':
#         form=SignUpForm(request.POST)
#         if form.is_valid():
#             username=form.cleaned_data.get('username') # obtaining data from fields.
#             password= form.cleaned_data.get('password')
#             email= form.cleaned_data.get('email')
#             first_name=form.cleaned_data.get('first_name')
#             last_name=form.cleaned_data.get('last_name')
#             user=User.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name='last_name') # assigning obtained data to model variables and save user as staff.
#             user.is_staff=True
#             user.save()
#             message = ('%(username)s is added as a staff.') % {'username':username} # flash message for successful registration.
#             messages.success(request, message)
#             return HttpResponseRedirect('/accounts/login')
#     return render(request,'signup.html',{'form':form})


class SignUpView(View):
 def get(self, request):
  form = SignUpForm()
  return render(request,'signup.html',{'form':form})
  
 def post(self, request):
  form = SignUpForm(request.POST)
  if form.is_valid():
   messages.success(request, 'Congratulations!! Registered Successfully.')
   form.save()
  return render(request,'signup.html',{'form':form})


def initiate_payment(request):
    if request.method == "GET":
        return render(request, 'payments/pay.html')
    try:
        username = request.POST['username']
        password = request.POST['password']
        amount = int(request.POST['amount'])
        user = authenticate(request, username=username, password=password)
        if user is None:
            raise ValueError
        auth_login(request=request, user=user)
    except:
        return render(request, 'payments/pay.html', context={'error': 'Wrong Accound Details or amount'})

    transaction = Transaction.objects.create(made_by=user, amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)
    
    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'payments/redirect.html', context=paytm_params)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        paytm_checksum = ''
        print(request.body)
        print(request.POST)
        received_data = dict(request.POST)
        print(received_data)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            print("Checksum Matched")
            received_data['message'] = "Checksum Matched"
        else:
            print("Checksum Mismatched")
            received_data['message'] = "Checksum Mismatched"

        return render(request, 'payments/callback.html', context=received_data)
