import requests

res = requests.get('https://api.anti-captcha.com/getBalance', json = {'clientKey': 'c48332383108b5f0f661d3015c972cab'}).json()

res.update({'eq':45})
print(res)

