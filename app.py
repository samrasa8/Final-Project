from flask import Flask, render_template, request
import requests
import html

app = Flask(__name__)

API_KEY = 'Obwlo1C_7gtc0ShH4criW7r0EaTX9ocaONUpDRvA93FDI2NaurwkMjacorjpvNHzYVX9yBbg4uyJyJvE1th31p7wApvLTE6MNbF85GxRuXbvTde48QuVcnFAz7USZHYx'
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    businesses = []
    location = request.form.get('location', 'Seattle')
    price = request.form.get('price', '1,2,3,4')
    radius = request.form.get('radius', '4000')
    rating = request.form.get('rating', '1.0')
    hot_and_new = request.form.get('hot_and_new', False)
    outdoor_seating = request.form.get('outdoor_seating', False)
    wifi_free = request.form.get('wifi_free', False)
    coffee = request.form.get('coffee', True)
    categories = ''
    if hot_and_new:
        categories += 'hot_new,'
    if outdoor_seating:
        categories += 'outdoor_seating,'
    if wifi_free:
        categories += 'wifi_free,'
    if coffee:
        categories += 'coffee,'
    categories = categories.rstrip(',')
    headers = {'Authorization': 'Bearer %s' % API_KEY}
    url_params = {
        'location': location.replace(' ', '+'),
        'price': price,
        'radius': radius,
        'rating': rating,
        'categories': categories,
        'limit': 50  
    }
    url = API_HOST + SEARCH_PATH
    businesses = []
    for offset in range(0, 200, 50): 
        url_params['offset'] = offset
        response = requests.get(url, headers=headers, params=url_params)
        results = response.json()
        for business in results['businesses']:
            businesses.append({
                'name': html.escape(business['name']),
                'address': html.escape(business['location']['address1']),
                'rating': html.escape(str(business['rating']))
            })
    return render_template('results.html', businesses=businesses)
