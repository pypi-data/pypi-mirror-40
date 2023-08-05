"""
Main entry point for the Kunteksto application.
"""
import sys
import os
from subprocess import run
import click
import configparser
import sqlite3
import requests
from requests.auth import HTTPDigestAuth

from .analyze  import analyze
from .generate  import make_model, make_data
from .catalogmgr import  get_catalog
from .modeledit import edit_model
from .recordedit import edit_record

@click.command()
@click.option('--mode', '-m', type=click.Choice(['all', 'editdb', 'gendata', 'genmodel']), help="See the documentation. If you don't know then use: all", prompt="Enter a valid mode")
@click.option('--infile', '-i', help='Full path and filename of the input CSV file.', prompt="Enter a valid CSV file")
@click.option('--dbfile', '-db', help='Full path and filename of the existing model database file.', prompt=False)
@click.option('--outdir', '-o', help='Full path to the output directory for writing the database and other files. Overrides the config file default value.')
@click.option('--delim', '-d', type=click.Choice([',', ';', ':', '|', '$']), help=' Overrides the config file default value.')
@click.option('--analyzelevel', '-a', type=click.Choice(['simple', 'full']), help=' Overrides the config file default value.')
def main(mode, infile, outdir, delim, analyzelevel, dbfile):
    """Kunteksto (ˈkänˌteksto) adds validation and semantics to your data."""

    # Setup config info based on the current working directory
    config = configparser.ConfigParser()
    config.read('../kunteksto.conf')
    print("\n\nKunteksto version: " + config['SYSTEM']['version'] + " using S3Model RM: " + config['SYSTEM']['rmversion'] + "\n\n")

    # override the delimiter and/or analyzelevel if provided
    if not delim:
        delim = config['KUNTEKSTO']['delim']
    if not analyzelevel:
        analyzelevel = config['KUNTEKSTO']['analyzelevel']
    
    if outdir is None:
        if config['KUNTEKSTO']['outdir'].lower() in ['output', 'none']:
            config['KUNTEKSTO']['outdir'] = 'output'
            outdir = os.getcwd() + os.path.sep + config['KUNTEKSTO']['outdir']
        else:
            print("You must supply a writable output directory.")
            exit(code=1)

    if not infile:
        print("You must supply a readable CSV input file.")
        exit(code=1)

    if not mode:
        click.echo("You must supply a mode.")
        exit(code=1)
        
    elif mode == 'all':
        dname, fname = os.path.split(infile)
        outdir += os.path.sep + fname[:fname.index('.')] 
        prjname = fname[:fname.index('.')]
        get_catalog(outdir, prjname) # Set the environment variable XML_CATALOG_FILES for lxml
        if not dbfile:
            outDB = analyze(infile, delim, analyzelevel, outdir)
            edit_model(outDB)
            edit_record(outDB)
            modelName = make_model(outDB, outdir)
            datagen(modelName, outDB, infile, delim, outdir, config)
        else:
            outDB = dbfile
            modelName = make_model(outDB, outdir)
            datagen(modelName, outDB, infile, delim, outdir, config)
            
        
            
    elif mode == 'genmodel':
        if not dbfile:
            click.echo("You must supply a full path and name of an existing model database.")
            exit(code=1)
            
        dname, fname = os.path.split(dbfile)
        prjname = fname[:fname.index('.')]
        dbName =  prjname + '.db'
        get_catalog(outdir, prjname)        
        conn = sqlite3.connect(dbfile)
        c = conn.cursor()
        c.execute("SELECT * FROM model")
        row = c.fetchone()
        dmID = row[5].strip()
        outdir = outdir + os.path.sep + prjname        
        modelName = outdir + '/dm-' + dmID + '.xsd'
        make_model(dbfile, outdir)

    elif mode == 'gendata':
        if not dbfile:
            click.echo("You must supply a full path and name of an existing model database.")
            exit(code=1)
            
        dname, fname = os.path.split(dbfile)
        prjname = fname[:fname.index('.')]
        dbName =  prjname + '.db'
        get_catalog(outdir, prjname)        
        conn = sqlite3.connect(dbfile)
        c = conn.cursor()
        c.execute("SELECT * FROM model")
        row = c.fetchone()
        dmID = row[5].strip()
        outdir = outdir + os.path.sep + prjname        
        modelName = outdir + '/dm-' + dmID + '.xsd'
        datagen(modelName, dbfile, infile, delim, outdir, config)
        
    elif mode == 'editdb':
        dname, fname = os.path.split(infile)
        dbName = fname[:fname.index('.')] + '.db'
        db_file = dbfile
        edit_model(db_file)
        edit_record(db_file)
                
    return(True)

def datagen(modelName, outDB, infile, delim, outdir, config):
    """
    Generate XML, JSON and RDF data from the CSV. 
    """
    # open a connection to the RDF store if one is defined and RDF is to be generated.  
    if config['KUNTEKSTO']['rdf']:
        # load the model RDF
        modelRDF = modelName.split('.')[0]+'.rdf'
        with open(os.path.join(outdir,modelRDF), 'r') as rdffile:
            rdfStr=rdffile.read()         
        
        if config['ALLEGROGRAPH']['status'].upper() == "ACTIVE":
            # Set environment variables for AllegroGraph
            os.environ['AGRAPH_HOST'] = config['ALLEGROGRAPH']['host']
            os.environ['AGRAPH_PORT'] = config['ALLEGROGRAPH']['port']
            os.environ['AGRAPH_USER'] = config['ALLEGROGRAPH']['user']
            os.environ['AGRAPH_PASSWORD'] = config['ALLEGROGRAPH']['password']            
            try:
                from franz.openrdf.connect import ag_connect
                connRDF = ag_connect(config['ALLEGROGRAPH']['repo'], host=os.environ.get('AGRAPH_HOST'), port=os.environ.get('AGRAPH_PORT'),  user=os.environ.get('AGRAPH_USER'), password=os.environ.get('AGRAPH_PASSWORD'))
                connRDF.addData(rdfStr, rdf_format=RDFFormat.RDFXML, base_uri=None, context=None)
                print('Current Kunteksto RDF Repository Size: ', connRDF.size(), '\n')
                print('AllegroGraph connections are okay.\n\n')
            except: 
                connRDF = None
                print("Unexpected error: ", sys.exc_info()[0])
                print('RDF Connection Error', 'Could not create connection to AllegroGraph.')
        else:
            connRDF = None
        if config['MARKLOGIC']['status'] == 'ACTIVE' and config['MARKLOGIC']['loadrdf'].lower() == 'true':
            dbname = config['MARKLOGIC']['dbname']
            hostip = config['MARKLOGIC']['hostip']
            port = config['MARKLOGIC']['port']
            user = config['MARKLOGIC']['user']
            pw = config['MARKLOGIC']['password']            
            headers = {"Content-Type": "application/xml", 'user-agent': 'Kunteksto'}
            url = 'http://' + hostip + ':' + port + '/v1/documents?uri=/'+ modelRDF
            r = requests.put(url, auth=HTTPDigestAuth(user, pw), headers=headers, data=rdfStr)                                
            
    # open a connection to the XML DB if one is defined and XML is to be generated.
    if config['KUNTEKSTO']['xml']:
        if config['BASEX']['status'].upper() == "ACTIVE":
            from BaseXClient import BaseXClient
            try:
                from BaseXClient import BaseXClient
                connXML = BaseXClient.Session(config['BASEX']['host'], int(config['BASEX']['port']), config['BASEX']['user'], config['BASEX']['password'])
                connXML.execute("create db " + config['BASEX']['dbname'])
                print("BaseX ", connXML.info())
            except: 
                connXML = None
                print("Unexpected error: ", sys.exc_info()[0])
                print('XML Connection Error', 'Could not create connection to BaseX.')
        else:
            connXML = None

    # generate the data
    if modelName:
        make_data(modelName, outDB, infile,  delim, outdir, connRDF, connXML, config)

        if connRDF:
            connRDF.close()
        if connXML:
            connXML.close()
        print('\n\nData Generation: ', 'Completed.')

    else:
        print('\n\nProcedure Error: ', 'Missing model DB or no selected output directory.')

    return(True)


if __name__ == '__main__':
    print('\n Kunteksto started ...\n\n')
    main()
