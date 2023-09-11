from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import users, errors

#Quelle: Miguel Grinnberg. The Flask Mega-Tutorial Part XXIII: Application Programming Interfaces (APIs).