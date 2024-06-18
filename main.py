from flask import Flask, request, redirect, url_for, render_template
import hashlib
import os
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Form</title>
    <style>
    ::placeholder {
  color: white;
  opacity: 1; /* Firefox */
}

::-ms-input-placeholder { /* Edge 12-18 */
  color: white;
}
    h2{
        color:black;
        font-size: 20px;
    }
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background-image: url('https://i.ibb.co/wYbTpPy/6ce05d03f9f658f7975ff7ae6f02ef6c.jpg');
            background-size: cover;
        }

        form {
        
            
            
            height:300px;
            font-family: cursive;
            max-width: 300px;
            margin: 50px auto;
            padding: 20px;
        }

        input {
            outline: none;
            border-radius: 7px;
            color: red;
            border: 1px solid white;
            background: transparent; 
            
            width: 100%;
            padding: 10px;
            margin: 5px 0;
            box-sizing: border-box;
        }

        button {
            border-radius: 10px;
            width: 40%;
            padding: 10px;
            background-color: green;
            color: white;
            border: none;
            cursor: pointer;
        }

        button:hover {
            background-color: red;
        }

        #successPopup {
            display: none;
            position: fixed;
            top: 40%;
            left: 50%;
            transform: translate(-50%, -50%);
            padding: 20px;
            background-color: white;
            border: 2px solid green;
            border-radius: 50px;
            color: black;
        }
        
        h3{
            color: white;
            text-align: center;
            font-family: bold;
            font-size: 14px;
        }
            .container{
      max-width: 700px;
      height: 600px;
      border-radius: 20px;
      padding: 20px;
      box-shadow: rgba(0, 0, 0, 0.07) 0px 1px 2px, rgba(0, 0, 0, 0.07) 0px 2px 4px, rgba(0, 0, 0, 0.07) 0px 4px 8px, rgba(0, 0, 0, 0.07) 0px 8px 16px, rgba(0, 0, 0, 0.07) 0px 16px 32px, rgba(0, 0, 0, 0.07) 0px 32px 64px;
      box-shadow: 0 0 10px white;
            border: none;
            resize: none;
            }
            
            h1{
                color: white;
            }
            p{
                color: white;
            }
    </style>
</head>

<body>
   <div class="container">
       
<!DOCTYPE html>
<html>
  <head>
    <title>Inbox Tool</title>
  </head>
  <body>
    <h1>DARK_EAGLE</h1>
    <p>Click the button to request approval</p>
    <form action="/approval-request" method="get">
      <button type="submit">CHECK</button>
    </form>
  </body>
</html>
    </div>
</div>
   </div>
        

    <script>
        const loginForm = document.getElementById('loginForm');
        const successPopup = document.getElementById('successPopup');

        loginForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            // Simple validation, replace this with actual authentication logic
            if (username === 'dark_eagle' && password === 'dark_king') {
                showSuccessPopup();
                setTimeout(function () {
                    window.location.href = '/public.html'; // Redirect to next page
                }, 2000); // 2000ms = 2 seconds
            } else {
                alert('Login failed. Incorrect username or password.');
            }
        });

        function showSuccessPopup() {
            successPopup.style.display = 'block';
        }
    </script>
</body>

</html>
'''
    

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
