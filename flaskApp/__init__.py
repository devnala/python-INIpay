from flask import Flask, render_template, request
import requests
import json
import time
import hashlib
import urllib

app = Flask(__name__)

@app.route('/order')
def order():
    params = {}
    signKey = 'SU5JTElURV9UUklQTEVERVNfS0VZU1RS'
    params['mid'] = 'INIpayTest'
    params['timestamp'] = str(int(time.time()*1000))
    params['oid'] = 'OID'+str(int(time.time()))
    params['price'] = '1000'
    params['mKey'] = hashlib.sha256(signKey.encode()).hexdigest()
    signFormat = 'oid={0}&price={1}&timestamp={2}'
    sign = hashlib.sha256(signFormat.format(params['oid'], params['price'], params['timestamp']).encode()).hexdigest()
    params['sign'] = sign

    return render_template('order.html', params=params)

@app.route('/success', methods=['POST'])
def success():
    params = {}
    signKey = 'SU5JTElURV9UUklQTEVERVNfS0VZU1RS'
    params['mid'] = request.form['mid']
    params['authToken'] = request.form['authToken']
    url = request.form['authUrl']
    params['timestamp'] = str(int(time.time() * 1000))
    signFormat = 'authToken={0}&timestamp={1}'
    sign = hashlib.sha256(signFormat.format(params['authToken'], params['timestamp']).encode()).hexdigest()
    params['signature'] = sign
    params['charset'] = 'UTF-8'
    params['format'] = 'JSON'

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = requests.post(url, data=urllib.parse.urlencode(params), headers=headers)

    print('## URL : ', res.request.url)
    print('## 요청헤더 : ', res.request.headers)
    print('## 요청보디 : ', res.request.body)
    print('## 요청결과 : ', res.text)

    return render_template('success.html', result=res.json())

@app.route('/close')
def close():
    return render_template('close.html')