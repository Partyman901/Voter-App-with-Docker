# main.py

from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/vote', methods=['POST'])
def vote():
    return redirect("http://host.docker.internal:8110", code=302)


@main.route('/results', methods=['POST'])
def db():
    return redirect("http://host.docker.internal:8090", code=302)

# IM CHANGED LMAOOOOOOOOOOOOOOO
