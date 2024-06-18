from flask import Flask, request, redirect, url_for, render_template
import hashlib
import os
import requests
import platform
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/approval-request')
def approval_request():
    unique_key = hashlib.sha256((str(os.getuid()) + os.getlogin()).encode()).hexdigest()
    return render_template('approval_request.html', unique_key=unique_key)

@app.route('/check-permission', methods=['POST'])
def check_permission():
    unique_key = request.form['unique_key']
    response = requests.get("https://pastebin.com/raw/E3FLmRKx")
    approved_tokens = [token.strip() for token in response.text.splitlines() if token.strip()]
    if unique_key in approved_tokens:
        print("Permission granted. You can proceed with the script.")
        print("\n===========================")
        return redirect(url_for('approved'))
    else:
        print("Sorry, you don't have permission to run this script.")
        return redirect(url_for('not_approved'))

@app.route('/approved')
def approved():
    return render_template('approved.html')

@app.route('/not-approved')
def not_approved():
    return render_template('not_approved.html')

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000, debug=True)
