
import base64
from io import BytesIO

import pyotp
import qrcode
from flask import Blueprint, flash, g, redirect, render_template, request

import libmfa

mod_mfa = Blueprint('mod_mfa', __name__, template_folder='templates')


@mod_mfa.route('/', methods=['GET'])
def do_mfa_view():

    if 'username' not in g.session:
        return redirect('/user/login')

    if libmfa.mfa_is_enabled(g.session['username']):
        return render_template('mfa.disable.html')
    else:
        libmfa.mfa_reset_secret(g.session['username'])
        secret = libmfa.mfa_get_secret(g.session['username'])
        secret_url = pyotp.totp.TOTP(secret).provisioning_uri(g.session['username'], issuer_name="vul_app")
        img = qrcode.make(secret_url)

        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        return render_template('mfa.enable.html', secret_url=secret_url, img_str=img_str)


@mod_mfa.route('/', methods=['POST'])
def do_mfa_enable():

    if 'username' not in g.session:
        return redirect('/user/login')

    secret = libmfa.mfa_get_secret(g.session['username'])

    otp = request.form.get('otp')

    totp = pyotp.TOTP(secret)

    if totp.verify(otp):
        libmfa.mfa_enable(g.session['username'])
        return redirect('/mfa/')
    else:
        flash("The OTP was incorrect")
        return redirect('/mfa/')

    return render_template('mfa.enable.html')


@mod_mfa.route('/disable', methods=['GET'])
def do_mfa_disable():

    if 'username' not in g.session:
        return redirect('/user/login')

    libmfa.mfa_disable(g.session['username'])
    return redirect('/mfa/')
