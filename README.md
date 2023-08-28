
# Django IPN Coinpayment


Package for payment handling via https://www.coinpayments.net







![image](https://github.com/SHMasoudi/Coinpayment_Gateway/assets/60820666/b30b7b0e-d7a1-4ae2-afa0-9d936d843bc1)





1)

Introduction
The IPN system will notify your server when you receive a payment and when a payment status changes. This is a easy and useful way to integrate our payments into your software to automate order completion, digital downloads, accounting, or whatever you can think up.
It is implemented by making a standard HTTP POST (application/x-www-form-urlencoded) call over a https:// or http:// URL to a script or CGI program on your server.

2)

IPN Setup
The first step is to go to the My Settings page and set a IPN Secret. Your IPN Secret is a string of your choosing that is used to verify that an IPN was really sent from our servers (recommended to be a random string of letters, numbers, and special characters). Our system will not send any IPNs unless you have an IPN Secret set. See the "Authenticating IPNs" section for more details.


At the same time you can optionally set an IPN URL; this is the URL that will be called when sending you IPN notifications. You can also set an IPN URL in your Buy Now and Cart buttons that will be used instead of this one.

3)
IPN Retries / Duplicate IPNs
If there is an error sending your server an IPN, we will retry up to 10 times. Because of this you are not guaranteed to receive every IPN (if all 10 tries fail) or that your server will receive them in order.
Your IPN handler must always check to see if a payment has already been handled before to avoid double-crediting users, etc. in the case of duplicate IPNs.


4)
Authenticating IPNs
We use your IPN Secret as the HMAC shared secret key to generate an HMAC signature of the raw POST data. The HMAC signature is sent as a HTTP header called HMAC.


more : https://www.coinpayments.net/merchant-tools-ipn








