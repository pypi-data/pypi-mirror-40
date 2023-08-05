import configparser

import click
import os

from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, form
from flask_admin.contrib.sqla import ModelView
from flask_babelex import Babel


# Setup config info 
config = configparser.ConfigParser()
config.read('../kunteksto.conf')
print("\n\nKunteksto version: " + config['SYSTEM']['version'] + " using S3Model RM: " + config['SYSTEM']['rmversion'] + "\n\n")

# create XML catalog if it doesn't exist
if not os.path.exists("../catalogs/Kunteksto_catalog.xml"):
    make_catalog()

# env var used by lxml
os.environ['XML_CATALOG_FILES'] = '../catalogs/Kunteksto_catalog.xml'

app = Flask(__name__)
babel = Babel(app)

# set optional bootswatch theme https://bootswatch.com/3/yeti/
app.config['FLASK_ADMIN_SWATCH'] = config['KUNTEKSTO']['theme']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kunteksto.db'
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

@babel.localeselector
def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'en')


db = SQLAlchemy(app)


def make_catalog():
    """
    Create an XML Catalog based on the installation location.    
    """
    catdir = os.join(Path().resolve().parent, 'catalogs')
    dmlib = os.join(Path().resolve().parent, 'dmlib')
    
    
    xmlcat = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xmlcat += '<!DOCTYPE catalog PUBLIC "-//OASIS//DTD XML Catalogs V1.1//EN" "http://www.oasis-open.org/committees/entity/release/1.1/catalog.dtd">'
    xmlcat += '<catalog xmlns="urn:oasis:names:tc:entity:xmlns:xml:catalog">\n'
    xmlcat += '  <!-- S3Model RM Schema -->\n'
    xmlcat += '    <uri name="https://www.s3model.com/ns/s3m/s3model_' + RMVERSION + '.xsd" uri="../s3model/s3model_' + RMVERSION + '.xsd"/>\n'    
    xmlcat += '  <!-- S3Model DMs -->\n'    
    xmlcat += '    <rewriteSystem systemIdStartString="https://s3model.com/dmlib/" rewritePrefix="file:///' + dmlib + '/"/>\n'    
    xmlcat += '</catalog>\n'    
    
    if not os.path.exists(dmlib):
        os.makedirs(dmlib)    
    if not os.path.exists(catdir):
        os.makedirs(catdir)
        
    with open(catdir + '/Kunteksto_catalog.xml', 'w') as f:
        f.write(xmlcat)

    return
