from app import app
from flask import jsonify
from flask import request, url_for, redirect
from werkzeug.http import HTTP_STATUS_CODES


# API-test GET Method
@app.route('/test-api', methods=['GET'])
def test_get():
    data = [
        {'test-api': 'API Test Success.'}
    ]
    return jsonify(data)


# Fault-Injection Method
@app.route('/fault-inject', method=['POST'])
def fault_injection():
    pass
