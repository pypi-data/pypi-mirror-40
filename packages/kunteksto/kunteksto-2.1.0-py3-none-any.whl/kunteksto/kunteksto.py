"""
Main entry point for the Kunteksto application.
"""
import sys
import os
import functools

import click
import configparser
import sqlite3
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from flask_admin.form.rules import Field
from flask_admin import Admin, form
from flask_admin.form import rules
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm
from flask.cli import with_appcontext

from wtforms import fields, widgets
from sqlalchemy import event
from jinja2 import Markup

from . import app, config
from .models import XMLstore, JSONstore, RDFstore, Datamodel, Component, Validation, db

from .analyze import process
from .generate import make_data, make_model, export_model

# Add Flask Admin setup and administrative views here
admin = Admin(app, name='Kunteksto', template_mode='bootstrap3')

class XMLstoreModelView(ModelView):
    form_base_class = SecureForm
    can_create = True
    edit_modal = True
    can_export = True
    column_list = ('name', 'dbname', 'host', 'id')
    column_labels = {'name':"Name", 'host':"Host", 'port':"Port", 'hostip':'Host IP', 'forests':'Forests', 'dbname':"Database", 'user':"User", 'pw':"Password"}
    form_choices = {'dbtype': [
           ('fs', 'Filesystem'),
           ('ml', 'Marklogic'),
           ('ag', 'Allegrograph'),
           ('bx', 'BaseX'),
       ]}

class JSONstoreModelView(ModelView):
    form_base_class = SecureForm
    can_create = True
    edit_modal = True
    can_export = True
    column_list = ('name', 'dbname', 'host', 'id')
    column_labels = {'name':"Name", 'host':"Host", 'port':"Port", 'hostip':'Host IP', 'forests':'Forests', 'dbname':"Database", 'user':"User", 'pw':"Password"}
    form_choices = {'dbtype': [
           ('fs', 'Filesystem'),
           ('ml', 'Marklogic'),
           ('ag', 'Allegrograph'),
           ('bx', 'BaseX'),
       ]}

class RDFstoreModelView(ModelView):
    form_base_class = SecureForm
    can_create = True
    edit_modal = True
    can_export = True
    column_list = ('name', 'dbname', 'host', 'id')
    column_labels = {'name':"Name", 'host':"Host", 'port':"Port", 'hostip':'Host IP', 'forests':'Forests', 'dbname':"Database", 'user':"User", 'pw':"Password"}
    form_choices = {'dbtype': [
           ('fs', 'Filesystem'),
           ('ml', 'Marklogic'),
           ('ag', 'Allegrograph'),
           ('bx', 'BaseX'),
       ]}

class DatamodelModelView(ModelView):
    form_base_class = SecureForm
    can_create = False
    edit_modal = True
    can_export = True
    column_list = ('project', 'title', 'author', 'dmid', 'id')
    form_excluded_columns = ['dmid', 'dataid', 'components']
    column_labels = {'rdf':"RDF", 'xmlstore':"XML Storage", 'rdfstore':"RDF Storage", 'jsonstore':'JSON Storage'}
    column_descriptions = {'namespaces':'Additional Namespaces', 'schema':'Generated XML schema for model.', 'rdf':'Generated RDF', 'xmlstore':'XML instance storage location.', \
                           'jsonstore':'JSON instance storage location.', 'rdfstore':'RDF instance storage location.', 'catalog':'Generated XML Catalog'}    
    def on_form_prefill(self, form, id):
        form.project.render_kw = {'readonly': True}  # make the field readonly
        form.schema.render_kw = {'readonly': True}  # make the field readonly
        form.rdf.render_kw = {'readonly': True}  # make the field readonly
        form.validations.render_kw = {'readonly': True}  # make the field readonly

class ComponentModelView(ModelView):
    form_base_class = SecureForm
    can_create = False
    can_delete = False
    edit_modal = True
    can_export = True
    column_list = ('header', 'label', 'datatype', 'mcid', 'model_id')
    form_excluded_columns = ['mcid', 'adid', 'datamodel', 'model_link']
    form_widget_args = {
        'description': {'rows': 10, 'style': 'color: black'},
        'pred_obj': {'rows': 5, 'style': 'color: black'},
    }
    column_labels = {'min_len': "Minimum Length", 'max_len': "Maximum Length", 'regex': "Regualr Expression", 'min_incl': 'Minimum Value (Inclusive)', 'max_incl': 'Maximum Value (Inclusive)',
                     'min_excl': 'Minimum Value (Exclusive)', 'max_excl': 'Maximum Value (Exclusive)', 'pred_obj': 'Predicate/\nObject Pairs', 'def_text': 'Default Text',
                     'def_num': 'Default Numeric', 'mcid': 'Model Component ID'}
    column_descriptions = {'min_len':'Used for strings/text.', 'max_len':'Used for strings/text.', 'regex':'Use the XML Schema subset of RegEx.', 'min_incl':'Use for numerics.', \
                           'max_incl':'Use for numerics.','min_excl':'Use for numerics.','max_excl':'Use for numerics.','pred_obj':'One per line. Must have a space between the predicate and object.', \
                           'units':'Use a standardized units abbreviation.', 'choices':'Enumeration of valid values. One per line.'}    
    form_choices = {'datatype': [
           ('Integer', 'Integer'),
           ('Decimal', 'Decimal'),
           ('Float', 'Float'),
           ('String', 'String'),
           ('Date', 'Date'),
           ('Time', 'Time'),
           ('Datetime', 'Datetime'),
       ]}
    
    def on_form_prefill(self, form, id):
        form.header.render_kw = {'readonly': True}  # make the header readonly

class ValidationModelView(ModelView):
    form_base_class = SecureForm
    can_create = False
    can_edit = True
    can_export = True
    column_list = ('model_link', 'timestamp')
    column_descriptions = {'log':'A CSV log. Copy/paste this into a spreadsheet like Excel or Libre Calc.'}


admin.add_view(DatamodelModelView(Datamodel, db.session, 'Data Models'))
admin.add_view(ComponentModelView(Component, db.session, 'Components'))
admin.add_view(ValidationModelView(Validation, db.session, 'Validation'))

admin.add_view(XMLstoreModelView(XMLstore, db.session, 'XML'))
admin.add_view(JSONstoreModelView(JSONstore, db.session, 'JSON'))
admin.add_view(RDFstoreModelView(RDFstore, db.session, 'RDF'))



# Commandline options


@click.command('analyze')
@click.argument('project')
@click.option('--infile', '-i', help='Full path and filename of the input CSV file.', prompt="Enter a valid CSV file")
@click.option('--delim', '-d', type=click.Choice([',', ';', ':', '|', '$']), help=' Overrides the default CSV delimiter value in kunteksto.conf.')
@click.option('--level', '-l', type=click.Choice(['simple', 'full']), help=' Overrides the default value of "full".')
def analyze(project, infile, delim, level):
    """
    Analyze a CSV file (infile) to create a model from the commandline.
    You must include a unique PROJECT.
    """
    click.echo('Analyze ' + infile + ' for the project: ' + project)
    if not delim:
        delim = config['KUNTEKSTO']['delim']
    if not level:
        level = 'full'

    process(project, infile, delim, level)

@click.command('genmodel')
@click.argument('project')
def genmodel(project):
    """
    Generate a model based on PROJECT from the commandline. Note that this creates a new model. 
    You should remove any previous models based on this PROJECT. 
    """
    click.echo('Generating a model for: ' + project)
    make_model(project)

@click.command('gendata')
@click.argument('project')
@click.option('--infile', '-i', help='Full path and filename of the input CSV file.', prompt="Enter a valid CSV file")
def gendata(project, infile):
    """
    Generate data from a CSV file (infile) based on a model (project) from the commandline.
    """
    click.echo('Generate data from ' + infile + ' based on the model: ' + project)
    make_data(project, infile)

@click.command('export')
@click.argument('project')
def export(project):
    """
    Export a model XML Schema and RDF for the project.
    """
    click.echo('Exporting model to: Kunteksto/dmlib/' + project)
    export_model(project)

@click.command('ldexamples')
def ldexamples():
    """
    Generate example repository entries.
    """
    click.echo('Loading examples:')
    create_xmlstores()
    create_rdfstores()
    create_jsonstores()


app.cli.add_command(analyze)
app.cli.add_command(genmodel)
app.cli.add_command(gendata)
app.cli.add_command(export)
app.cli.add_command(ldexamples)


# Add default Datastore records when the tables are first created
def create_xmlstores():
    print('XML Repos')
    try:
        outdir = os.path.abspath(os.path.join(os.getcwd(), os.pardir, 'output', 'xml'))
        ds = XMLstore(dbtype='fs', name='Filesystem (XML example)', host=outdir, port='N/A', dbname='XML')
        db.session.add(ds)
        db.session.commit()
    except sqlite3.IntegrityError as e:
        print(e)
        
    try:
        ds = XMLstore(dbtype='ml', name='Marklogic (XML example)', host='localhost.localdomain', port='10035', dbname='Kunteksto', hostip='192.168.25.120', forests=2, user='admin', pw='admin')
        db.session.add(ds)
        db.session.commit()
    except sqlite3.IntegrityError as e:
        print(e)

    try:
        ds = XMLstore(dbtype='bx', name='BaseX (XML example)', host='localhost', port='1984', dbname='Kunteksto', user='admin', pw='admin')
        db.session.add(ds)
        db.session.commit()
    except sqlite3.IntegrityError as e:
        print(e)


def create_rdfstores():
    print('RDF Repos')
    try:
        outdir = os.path.abspath(os.path.join(os.getcwd(), os.pardir, 'output', 'rdf'))
        ds = RDFstore(dbtype='fs', name='Filesystem (RDF example)', host=outdir, port='N/A', dbname='RDF')
        db.session.add(ds)
        db.session.commit()
    except sqlite3.IntegrityError as e:
        print(e)
    
    try:
        ds = RDFstore(dbtype='ag', name='AllegroGraph (RDF example)', host='localhost', port='10035', dbname='Kunteksto', user='admin', pw='admin')
        db.session.add(ds)
        db.session.commit()
    except sqlite3.IntegrityError as e:
        print(e)
    
    try:
        ds = RDFstore(dbtype='ml', name='Marklogic (RDF example)', host='localhost.localdomain', port='10035', dbname='Kunteksto', hostip='192.168.25.120', forests=2, user='admin', pw='admin')
        db.session.add(ds)
        db.session.commit()
    except sqlite3.IntegrityError as e:
        print(e)


def create_jsonstores():
    print('JSON Repos')    
    try:
        outdir = os.path.abspath(os.path.join(os.getcwd(), os.pardir, 'output', 'json'))
        ds = JSONstore(dbtype='fs', name='Filesystem (JSON example)', host=outdir, port='N/A', dbname='JSON')
        db.session.add(ds)
        db.session.commit()
    except sqlite3.IntegrityError as e:
        print(e)
    
    try:
        ds = JSONstore(dbtype='ml', name='Marklogic (JSON example)', host='localhost.localdomain', port='10035', dbname='Kunteksto', hostip='192.168.25.120', forests=2, user='admin', pw='admin')
        db.session.add(ds)
        db.session.commit()
    except sqlite3.IntegrityError as e:
        print(e)


# Routing
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run()
