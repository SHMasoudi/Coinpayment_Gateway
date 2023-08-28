import hashlib
import hmac
import random
import requests
from django.conf import settings
from django.http import HttpResponse
from account.models import UserExtra
from courses.models import Course
from peyment.models import CourseTransactions


#Coinpayment API

Mainurl = "https://www.coinpayments.net/api.php"
url="https://www.coinpayments.net/index.php"
key=settings.COINPAYMENTS_PUBLIC_KEY
secretkey = settings.COINPAYMENTS_PRIVATE_KEY
ipn_secret_key = settings.COINPAYMENTS_IPN_SECRET
merchant_id = settings.COINPAYMENTS_MERCHANT_ID




def calculate_hmac(message,key):
        """
        Calculate the HMAC based on the secret and url encoded params
        """
        key = bytes(key,'utf-8')
        message = bytes(message,'utf-8')
        hmac_gen = hmac.new(key,message,hashlib.sha512)
        return hmac_gen.hexdigest()


def coinpayment_ipn(request):
    
    
    crsSlug =request.GET.get('crs')
    userToken = request.GET.get('tkn')
    if request.method == 'POST':
        # Get the POST data from CoinPayment
        data = request.POST  

        # Create hmac signature
        paramJoin = '&'.join([f'{key}={value}' for key, value in sorted(data.items())]).replace('@', '%40')
        message = paramJoin.replace(' ', '+').replace(',', '%2C')
        signature = calculate_hmac(message=message, key=ipn_secret_key)
        #-----------------------------------------------------
        # Get data from request
        http_hmac = request.META.get('HTTP_HMAC')
        merchant = data['merchant']
        trxID = data['txn_id']
        ipn_mode = data['ipn_mode']
        ipn_id = data['ipn_id']
        statusCode=data['status']
        
        reqIP = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[0].strip()
        
        # Verify the IPN signature
        if merchant is None:
            return HttpResponse ("No merchant ID")
        elif merchant != merchant_id:
            return HttpResponse ("Invalid merchant ID")
        elif ipn_mode is None:
            return HttpResponse ("No ipn_mode")
        elif ipn_mode != 'hmac':
            return HttpResponse ("Invalid ipn_mode")
        elif http_hmac is None:
            return HttpResponse ("No HTTP HMAC") 
        elif http_hmac != signature:
            return HttpResponse ("Invalid HTTP HMAC") 
        else:
                userExtra = UserExtra.objects.get(Token=userToken)
                course = Course.objects.get(Slug=crsSlug, Status='a', PriceStatus='p')
                if statusCode == '100':
                    CoinTrans=CourseTransactions()
                    CoinTrans.User=userExtra.User
                    CoinTrans.Course=course
                    CoinTrans.Amount=course.Price
                    CoinTrans.TypeC='p'
                    CoinTrans.Status='p'
                    CoinTrans.TransCode = trxID
                    CoinTrans.InvoiceNo=" "
                    CoinTrans.IP="123"
                    CoinTrans.CoinpaymentStatus=statusCode
                    
                    CoinTrans.save()

                return HttpResponse('IPN processed successfully',status=200)

      


