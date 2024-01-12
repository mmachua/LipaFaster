from django.shortcuts import render

from django.views.generic import TemplateView
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
#from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Merchant, Paybill, QRCode
# from .forms import MerchantForm, PaybillForm

from django.shortcuts import render
from django.http import HttpResponse
from django_daraja.mpesa.core import MpesaClient

from django.shortcuts import render
from django.http import HttpResponse
#from mpesa_api.core import MpesaClient

def index(request):
    cl = MpesaClient()
    phone_number = '0702297996'
    amount = 1
    account_reference = 'reference'
    transaction_desc = 'Description'
    callback_url = 'https://darajambili.herokuapp.com/express-payment'  # Use your own URL here
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    if response.get('ResponseCode') == '0':
        message = "STK Push was successful!"
    else:
        message = "STK Push failed, please try again."
    return HttpResponse(message)

def stk_push_callback(request):
    cl = MpesaClient()
    phone_number = '0702297996'
    amount = 1
    account_reference = 'reference'
    transaction_desc = 'Description'
    callback_url = 'https://darajambili.herokuapp.com/express-payment'  # Use your own URL here
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    # Handle the Mpesa response here
    # This is where you can update your database or send a notification to the user
    #response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    return HttpResponse(response)

# def stk_push_callback(request):
#         data = request.body
        
#         return HttpResponse("STK Push in Django👋")

# Create your views here.
from django.views.generic import TemplateView
import requests

class MpesaAPI:
    def __init__(self, consumer_key, consumer_secret, environment):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.environment = environment
        self.base_url = 'https://sandbox.safaricom.co.ke/' if self.environment == 'sandbox' else 'https://api.safaricom.co.ke/'

    def generate_access_token(self):
        url = self.base_url + 'oauth/v1/generate?grant_type=client_credentials'
        response = requests.get(url, auth=(self.consumer_key, self.consumer_secret))
        if response.status_code == 200:
            return response.json().get('access_token', '')
        return ''
        
    def stk_push(self, amount, phone_number):
        access_token = self.generate_access_token()
        if not access_token:
            return False

        url = self.base_url + 'mpesa/stkpush/v1/processrequest'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        payload = {
            'BusinessShortCode': 'YOUR_BUSINESS_SHORTCODE',
            'Password': 'YOUR_ENCODED_PASSWORD',
            'Timestamp': 'YYYYMMDDHHMMSS',
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': amount,
            'PartyA': phone_number,
            'PartyB': 'YOUR_BUSINESS_SHORTCODE',
            'PhoneNumber': phone_number,
            'CallBackURL': 'YOUR_CALLBACK_URL',
            'AccountReference': 'YOUR_ACCOUNT_REFERENCE',
            'TransactionDesc': 'YOUR_TRANSACTION_DESCRIPTION'
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return True
        return False


# class HomeView(TemplateView):
#     template_name = 'home/home.html'
#     consumer_key = 'Yizdre8ZT6QJKPOChJzRqaN2PPlgdCZT'
#     consumer_secret = '4sxyASNDxaVpUcsK'
#     environment = 'sandbox'

#     def post(self, request, *args, **kwargs):
#         amount = request.POST.get('amount', '')
#         phone_number = request.POST.get('phone_number', '')
#         mpesa_api = MpesaAPI(self.consumer_key, self.consumer_secret, self.environment)
#         response = mpesa_api.stk_push(amount, phone_number)
#         if response:
#             message = 'M-Pesa payment successful!'
#         else:
#             message = 'M-Pesa payment failed!'
#         return self.render_to_response(self.get_context_data(message=message))

from pdf2image import convert_from_path
from pdf2image import convert_from_bytes
from io import BytesIO
import requests
from PIL import Image
from django.http import HttpResponse
from io import BytesIO
import requests
from PIL import Image
from django.http import HttpResponse
import requests
from io import BytesIO
from PIL import Image
from django.http import HttpResponse
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'home/home.html'

    def post(self, request, *args, **kwargs):
        pdf_file = request.FILES.get('pdf_file')
        if pdf_file:
            # Convert PDF to Image
            response = requests.post('https://pdf.to/image', files={'f': pdf_file})
            if response.ok:
                # Save the Image
                image_bytes = BytesIO(response.content)
                image_format = Image.open(image_bytes).format
                image_path = 'path/to/downloads/file.{}'.format(image_format.lower())
                image_bytes.seek(0)
                with open(image_path, 'wb') as f:
                    f.write(image_bytes.read())
                # Download the Image
                with open(image_path, 'rb') as f:
                    response = HttpResponse(f.read(), content_type='image/jpeg')
                    response['Content-Disposition'] = 'attachment; filename=image.jpg'
                    return response
            else:
                message = 'Unable to convert PDF to Image'
        else:
            message = 'No PDF file selected'
        return self.render_to_response(self.get_context_data(message=message))


@method_decorator(login_required, name='dispatch')
class MerchantView(View):
    def get(self, request):
        merchant = Merchant.objects.get(user=request.user)
        #form = MerchantForm(instance=merchant)
        #context = {'form': form}
        return render(request, 'merchant.html')#, context)

    # def post(self, request):
    #     merchant = Merchant.objects.get(user=request.user)
    #     #form = MerchantForm(request.POST, instance=merchant)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('merchant')
    #     context = {'form': form}
    #     return render(request, 'merchant.html', context)

@method_decorator(login_required, name='dispatch')
class PaybillView(View):
    def get(self, request):
        paybills = Paybill.objects.filter(merchant__user=request.user)
        context = {'paybills': paybills}
        return render(request, 'paybills.html', context)

    # def post(self, request):
    #     form = PaybillForm(request.POST)
    #     if form.is_valid():
    #         paybill = form.save(commit=False)
    #         paybill.merchant = Merchant.objects.get(user=request.user)
    #         paybill.save()
    #         return redirect('paybills')
    #     paybills = Paybill.objects.filter(merchant__user=request.user)
    #     context = {'form': form, 'paybills': paybills}
    #     return render(request, 'paybills.html', context)

@method_decorator(login_required, name='dispatch')
class QRCodeView(View):
    def get(self, request, pk):
        paybill = Paybill.objects.get(pk=pk, merchant__user=request.user)
        qr_code = QRCode.objects.get_or_create(paybill=paybill)[0]
        context = {'qr_code': qr_code}
        return render(request, 'qr_code.html', context)
