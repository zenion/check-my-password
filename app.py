import sys, hashlib, logging
from flask import Flask, request, render_template

app = Flask(__name__)

with open('static/rockyou.txt', 'r', encoding="latin-1") as f:
    rockyou_content = f.read().splitlines()

with open('static/linkedin_hashes.txt', 'r', encoding="latin-1") as f:
    linkedin_content = f.read().splitlines()


def lookup_rockyou(password):
    if password in rockyou_content:
        return "FOUND"
    return "NOT FOUND"


def lookup_linkedin(password):
    hexed_password = hashlib.sha1(password.encode('utf-8')).hexdigest()
    hexed_password_short = '00000' + hexed_password[5:]
    response = []
    if hexed_password in linkedin_content:
        response.append("FOUND ")
    if hexed_password_short in linkedin_content:
        response.append("FOUND and CRACKED")
    if response:
        return response
    else:
        return "NOT FOUND"


@app.route('/')
def form():
    return render_template('form.html')


@app.route('/lookup_password', methods=['POST'])
def lookup_password():
    user_pass = str(request.form['user_password'])
    rockyou_output = lookup_rockyou(user_pass)
    linkedin_output = lookup_linkedin(user_pass)
    linkedin_output_string = ""
    if isinstance(linkedin_output, list):
        for i in linkedin_output:
            linkedin_output_string += str(i + ' ')
    else:
        linkedin_output_string = linkedin_output

    return render_template('form_results.html', rockyou_output=rockyou_output, linkedin_output=linkedin_output_string)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
