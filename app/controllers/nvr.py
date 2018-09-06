from flask import Blueprint, render_template

nvr = Blueprint('nvr', __name__)

@nvr.route('/a', methods=['GET', 'POST'])
def insert():
    return 'a'