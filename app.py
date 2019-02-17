from re import template
from urllib import request

from flask import Flask, render_template, jsonify, request
import paypalrestsdk
import requests

app = Flask(__name__)


paypalrestsdk.configure({
  "mode": "live", # sandbox or live
  "client_id": "AcpdQ-5Rmx-3i8_hGsRSscx118tez2hnN7DG9glGv_SQyLbrHkAbnSEyb8AewVuCiZKZozLCrkN8RES_",
  "client_secret": "EKqL0w1JfOuqO8TZ4dYE-qCZQPTY6q1wUjVYy0CaiZl_daq46vADOAQ7Mzcpwyx6xVgC49KuLoYmPMSo" })





@app.route('/')
def index():
    return render_template('index.html')


@app.route('/payment', methods=['POST'])
def payment():

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:3000/payment/execute", #https://flaskwebprojekt.azurewebsites.net/payment/execute
            "cancel_url": "http://localhost:3000/"},            #https://flaskwebprojekt.azurewebsites.net
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "za web",
                    "sku": "12345",
                    "price": "10.00",
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": "10.00",
                "currency": "USD"},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        print('Payment success!')
    else:
        print(payment.error)

    return jsonify({'paymentID' : payment.id})

@app.route('/execute', methods=['POST'])
def execute():
    success = False

    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id' : request.form['payerID']}):
        print('Execute success!')
        success = True
    else:
        print(payment.error)

    return jsonify({'success' : success})



@app.errorhandler(404)
def not_found(e):
       return render_template("404err.html")


@app.errorhandler(500)
def internal_error(error):

    return render_template("500err.html")











if __name__ == '__main__':
    app.run(debug=True)
