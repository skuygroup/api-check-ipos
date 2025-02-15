from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from os import environ
import requests

app = Flask(__name__)
CORS(app)

# //////////////
# FUNCTION START
# /////////////
def format_domain(domain):
    """
    Menghilangkan protocol (http:// atau https://) dari domain
    """
    if domain:
        domain = domain.lower()
        if domain.startswith('http://'):
            domain = domain[7:]
        elif domain.startswith('https://'):
            domain = domain[8:]
    return domain

def format_multiple_domains(domains):
    # Format setiap domain dulu
    formatted = [format_domain(domain) for domain in domains]
    # Tambahkan empty string jika kurang dari 5
    formatted = formatted + [''] * (5 - len(formatted))
    
    return f'''{formatted[0]}
{formatted[1]}
{formatted[2]}
{formatted[3]}
{formatted[4]}'''

def check_domain_trustpositif(domains):
    url = "https://trustpositif.komdigi.go.id/Rest_server/getrecordsname_home"
    data = {
        "csrf_token": "cd026521a59e988d4d1bb0a7da683252",
        "name": domains
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def not_found():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>SKUYGROUP | Trust Positif API Documentation</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="robots" content="noindex, nofollow">
        <style>
            body {
                background: url(https://i.ibb.co.com/RTDGczGp/fuck.jpg);
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }
        </style>
    </head>
    <body>
    </body>
    </html>
    '''

# ////////////
# FUNCTION END
# ///////////

# ///////////
# ROUTE START
#///////////

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>SKUYGROUP | Trust Positif API Documentation</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="robots" content="noindex, nofollow">
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            pre {
                background-color: #f4f4f4;
                padding: 15px;
                border-radius: 5px;
                overflow-x: auto;
            }
            .endpoint {
                margin-bottom: 30px;
            }
            h2 {
                color: #333;
                border-bottom: 2px solid #eee;
                padding-bottom: 10px;
            }
            .footer {
                text-align: center;
            }
        </style>
    </head>
    <body>
        <h1>Trust Positif API Documentation</h1>
        
        <div class="endpoint">
            <h2>Single Domain Check</h2>
            <h3>GET /check/single</h3>
            <p>Check single domain using GET method</p>
            <pre>GET /check/single?domain=example.com</pre>
            <p>Example with CURL</p>
            <pre>curl "http://domain-api.com/check/single?domain=example.com"</pre>
            
            <h3>POST /check/single</h3>
            <p>Check single domain using POST method</p>
            <pre>POST /check/single
Content-Type: application/x-www-form-urlencoded

domain=example.com</pre>
            <p>Example with CURL</p>
            <pre>curl -X POST "http://domain-api.com/check/single" -d "domain=example.com"</pre>
        </div>

        <div class="endpoint">
            <h2>Multiple Domains Check (MAX 5 DOMAIN)</h2>
            <h3>GET /check/multiple</h3>
            <p>Check multiple domains (max 5) using GET method</p>
            <pre>GET /check/multiple?domain1=example.com&domain2=example.com&domain3=example.com&domain4=example.com&domain5=example.com</pre>
            <p>Example with CURL</p>
            <pre>curl "https://domain-api.com/check/multiple?domain1=example.com&domain2=example.com&domain3=example.com&domain4=example.com&domain5=example.com"</pre>
            
            <h3>POST /check/multiple</h3>
            <p>Check multiple domains (max 5) using POST method</p>
            <pre>POST /check/multiple
Content-Type: application/x-www-form-urlencoded

domain1=example1.com&domain2=example2.com</pre>
            <p>Example with CURL</p>
            <pre>curl -X POST "http://domain-api.com/check/multiple" -d "domain1=example.com" -d "domain2=example.com" -d "domain3=example.com" -d "domain4=example.com" -d "domain5=example.com"</pre>
        </div>

        <div class="endpoint">
            <h2>Notes</h2>
            <ul>
                <li>Supports both HTTP and HTTPS protocols (will be automatically removed)</li>
                <li>Maximum 5 domains for multiple check</li>
                <li>All domains will be converted to lowercase</li>
                <li>Returns JSON response with original and formatted domains</li>
            </ul>
        </div>

        <div class="footer">
            <span>Created By : <strong><a href="https://skuygroup.com/">SKUYGROUP</a></strong></span>
        </div>
    </body>
    </html>
    '''

@app.route('/check')
def check():
    return not_found()

@app.route('/cek')
def cek():
    return not_found()

@app.route('/chec')
def chec():
    return not_found()

@app.route('/chek')
def chek():
    return not_found()

@app.route('/check/single', methods=['GET', 'POST'])
def check_single_domain():
    try:
        if request.method == 'POST':
            domain = request.form.get('domain')  # Untuk POST form data
        else:
            domain = request.args.get('domain')  # Untuk GET query parameters
    
        if not domain:
            return jsonify({
                "status": 400,
                "error": "Bad Request",
                "message": "Parameter 'domain' tidak ditemukan"
            }), 400
            
        # Format domain
        formatted_domain = format_domain(domain)
        result = check_domain_trustpositif(formatted_domain)
        
        return jsonify({
            "status": 200,
            "domain": {
                "original": domain,
                "formatted": formatted_domain
            },
            "result": result
        })
    except Exception as e:
        return jsonify({
            "status": 500,
            "error": "Internal Server Error",
            "message": str(e)
        }), 500

@app.route('/check/multiple', methods=['GET', 'POST'])
def check_multiple_domains():
    try:
        domains = []
        original_domains = []
        if request.method == 'POST':
            for i in range(1, 7):
                domain = request.form.get(f'domain{i}', '')
                if domain:
                    original_domains.append(domain)
                    domains.append(format_domain(domain))
        else:
            for i in range(1, 7):
                domain = request.args.get(f'domain{i}', '')
                if domain:
                    original_domains.append(domain)
                    domains.append(format_domain(domain))
        
        if len(domains) > 5:
            return jsonify({
                "status": 400,
                "error": "Bad Request",
                "message": "Maksimal 5 domain yang dapat dicek sekaligus"
            }), 400

        if not domains:
            return jsonify({
                "status": 400,
                "error": "Bad Request",
                "message": "Minimal satu domain harus diisi"
            }), 400
        
        formatted_domains = format_multiple_domains(domains)
        
        print("Formatted domains:", formatted_domains)
        
        result = check_domain_trustpositif(formatted_domains)
        
        return jsonify({
            "status": 200,
            "domains": {
                "original": original_domains,
                "formatted": domains
            },
            "formatted_request": formatted_domains,
            "result": result
        })
    except Exception as e:
        return jsonify({
            "status": 500,
            "error": "Internal Server Error",
            "message": str(e)
        }), 500

# //////////
# ROUTE END
#//////////

# /////////////
# START RUNNING
#//////////////

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
