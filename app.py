from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Home route to render the form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle currency conversion
@app.route('/convert', methods=['POST'])
def convert_currency():
    # Retrieve form data and convert to uppercase
    from_currency = request.form.get("from_currency").upper()
    to_currency = request.form.get("to_currency").upper()
    try:
        amount = float(request.form.get("amount"))
    except ValueError:
        return "Invalid amount. Please enter a valid number.", 400

    # Construct the API URL
    url = f'https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&amount={amount}'

    # API request
    response = requests.get(url)

    # Check if response is valid
    if response.status_code == 200:
        data = response.json()
        if data.get('result') is not None:
            converted_amount = data['result']
            return render_template(
                'result.html',
                from_currency=from_currency,
                to_currency=to_currency,
                amount=amount,
                converted_amount=converted_amount
            )
        else:
            return "Invalid currency code. Please try again.", 400
    else:
        return "Error fetching conversion data. Please try again later.", 500

if __name__ == '__main__':
    app.run(debug=True)
