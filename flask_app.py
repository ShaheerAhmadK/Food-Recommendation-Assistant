from flask import Flask, request, jsonify
import json

app = Flask(__name__)


def filter_restaurants_by_cuisine_and_price(data, cuisine, min_price=0, max_price=1e5):
    filtered_restaurants = []
    for restaurant in data:
        filtered_menu = []
        for item in restaurant['Menu']:
            if item['Cuisine'] == cuisine:
                filtered_sizes = [size for size in item['Size'] if min_price <= size['Price'] <= max_price]
                if filtered_sizes:
                    filtered_item = item.copy()
                    filtered_item['Size'] = filtered_sizes
                    filtered_menu.append(filtered_item)
        if filtered_menu:
            filtered_restaurants.append({
                'restaurant': restaurant['restaurant'],
                'Location': restaurant['Location'],
                'Menu': filtered_menu
            })
    return filtered_restaurants

with open('/home/shaheerahmedk/mysite/dummy_restaurants.json', 'r') as f:
    data = json.load(f)

@app.route('/filter', methods=['GET'])
def filter_restaurants():
    cuisine = request.args.get('cuisine')
    if not cuisine:
        return jsonify({"error": "Cuisine parameter is required"}), 400
    min_price = float(request.args.get('min_price', 0))
    max_price = float(request.args.get('max_price', 1e5))
    filtered_restaurants = filter_restaurants_by_cuisine_and_price(data, cuisine, min_price, max_price)
    return jsonify(filtered_restaurants)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
