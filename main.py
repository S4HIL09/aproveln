from flask import Flask, request, redirect, url_for, render_template
import hashlib
import os
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/approval-request')
def approval_request():
    unique_key = hashlib.sha256((str(os.getuid()) + os.getlogin()).encode()).hexdigest()
    return '''
    <h1>Approval Request</h1>
    <p>Your unique key is: <code>{}</code></p>
    <form action="/check-permission" method="post">
        <input type="hidden" name="unique_key" value="{}">
        <input type="submit" value="Check Permission">
    </form>
    '''.format(unique_key, unique_key)

@app.route('/check-permission', methods=['POST'])
def check_permission():
    unique_key = request.form['unique_key']
    response = requests.get("https://pastebin.com/raw/E3FLmRKx")
    approved_tokens = [token.strip() for token in response.text.splitlines() if token.strip()]
    if unique_key in approved_tokens:
        return redirect(url_for('approved'))
    else:
        return redirect(url_for('not_approved'))

@app.route('/approved')
def approved():
    return '''
    <h1>Approved!</h1>
    <p>You have been granted permission to proceed.</p>
    <script>window.location.href = "/next-step";</script>
    '''

@app.route('/not-approved')
def not_approved():
    return '''
    <h1>Not Approved</h1>
    <p>Sorry, you don't have permission to run this script.</p>
    '''

@app.route('/next-step')
def next_step():
    return '''
    <h1>Next Step</h1>
    <p>You have reached the next step.</p>
    '''

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5724, debug=True)
