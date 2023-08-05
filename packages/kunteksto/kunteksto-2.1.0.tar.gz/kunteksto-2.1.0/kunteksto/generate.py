"""
generate.py

For the data index numbers see the list of fields in analyze.py 
"""
import sys
import os
from io import StringIO, BytesIO
import time
import datetime
import csv
from pathlib import Path

import sqlite3
from urllib.parse import quote
from xml.sax.saxutils import escape

import requests
from requests.auth import HTTPDigestAuth
from cuid import cuid
from collections import OrderedDict
import json
import xmltodict
import shortuuid
import iso8601
import click

from lxml import etree
from lxml import sax

from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker

from . import config
from .models import db, Session, Datamodel, Component, Validation
    
RMVERSION = config['SYSTEM']['rmversion'].replace('.', '_')
DELIM = config['KUNTEKSTO']['delim']

with open('../s3model/s3model_' + RMVERSION + '.xsd', 'r') as rmfile:
    rm_str = rmfile.read()
    rm_str = rm_str.replace('<?xml version="1.0" encoding="UTF-8"?>','')
    RM_SCHEMA = etree.XMLSchema(etree.XML(rm_str))
    RM_PARSER = etree.XMLParser(schema=RM_SCHEMA)
    
def is_valid_decimal(s):
    try:
        float(s)
    except ValueError:
        return False
    except TypeError:
        return False
    else:
        return True
    
# add single and double quotes to xml.sax.saxutils.escape
xml_escape_table = {
    '"': "&quot;",
    "'": "&apos;"
}

xml_unescape_table = {v: k for k, v in xml_escape_table.items()}

def xml_escape(text):
    return escape(text, xml_escape_table)

def xml_unescape(text):
    return unescape(text, xml_unescape_table)    

# RDF storage imports
try:
    from franz.openrdf.rio.rdfformat import RDFFormat
except:
    pass


def xsd_header(rec):
    """
    Build the header string for the XSD
    """
    hstr = ''
    hstr += '<?xml-stylesheet type="text/xsl" href="dm-description.xsl"?>\n'
    hstr += '<xs:schema\n'
    hstr += '  xmlns:vc="http://www.w3.org/2007/XMLSchema-versioning"\n'
    hstr += '  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n'
    hstr += '  xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"\n'
    hstr += '  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n'
    hstr += '  xmlns:owl="http://www.w3.org/2002/07/owl#"\n'
    hstr += '  xmlns:xs="http://www.w3.org/2001/XMLSchema"\n'
    hstr += '  xmlns:xsd="http://www.w3.org/2001/XMLSchema#"\n'
    hstr += '  xmlns:dc="http://purl.org/dc/elements/1.1/"\n'
    hstr += '  xmlns:dct="http://purl.org/dc/terms/"\n'
    hstr += '  xmlns:skos="http://www.w3.org/2004/02/skos/core#"\n'
    hstr += '  xmlns:foaf="http://xmlns.com/foaf/0.1/"\n'
    hstr += '  xmlns:schema="http://schema.org/"\n'
    hstr += '  xmlns:sioc="http://rdfs.org/sioc/ns#"\n'
    hstr += '  xmlns:sh="http://www.w3.org/ns/shacl#"\n'
    hstr += '  xmlns:s3m="https://www.s3model.com/ns/s3m/"\n'
    if rec.namespaces is not None:
        for ns in rec.namespaces.splitlines():
            hstr += '  xmlns:' + ns + '\n'
        
    hstr += '  targetNamespace="https://www.s3model.com/ns/s3m/"\n'
    hstr += '  xml:lang="en-US">\n\n'
    hstr += '  <xs:include schemaLocation="https://www.s3model.com/ns/s3m/s3model_' + RMVERSION + '.xsd"/>\n\n'
    return(hstr)


def xsd_metadata(rec):
    """
    Create the metadata for the S3Model data model.
    """
    
    mds = '<!-- Metadata -->\n  <xs:annotation><xs:appinfo><rdf:RDF><rdfs:Class\n'
    mds += '    rdf:about="dm-' + rec.dmid + '">\n'
    mds += '    <dc:title>' + xml_escape(rec.title.strip()) + '</dc:title>\n'
    mds += '    <dc:creator>' + xml_escape(rec.author) + '</dc:creator>\n'
    mds += '    <dc:contributor></dc:contributor>\n'
    mds += '    <dc:subject>S3M</dc:subject>\n'
    mds += '    <dc:rights>' + xml_escape(rec.copyright) + '</dc:rights>\n'
    mds += '    <dc:relation>None</dc:relation>\n'
    mds += '    <dc:coverage>Global</dc:coverage>\n'
    mds += '    <dc:type>S3M Data Model</dc:type>\n'
    mds += '    <dc:identifier>' + rec.dmid.replace('dm-', '') + '</dc:identifier>\n'
    mds += '    <dc:description>' + xml_escape(rec.description) + '</dc:description>\n'
    mds += '    <dc:publisher>Data Insights, Inc. via Kunteksto</dc:publisher>\n'
    mds += '    <dc:date>' + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + \
        '</dc:date>\n'
    mds += '    <dc:format>text/xml</dc:format>\n'
    mds += '    <dc:language>en-US</dc:language>\n'
    mds += '    <rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model/DM"/>\n'
    mds += '  </rdfs:Class></rdf:RDF></xs:appinfo></xs:annotation>\n\n'
    return(mds)


def xdcount_rdf(data):
    """
    Create RDF including SHACL constraints for xdCount model.
    """
    mcID = data.mcid.strip()
    rdfStr = ''
    indent = 2
    padding = ('').rjust(indent)
    rdfStr += padding.rjust(indent + 6) + '<rdfs:Class rdf:about="mc-' + mcID + '">\n'
    rdfStr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model_' + RMVERSION + '.xsd#XdCountType"/>\n'
    rdfStr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model/RMC"/>\n'
    rdfStr += padding.rjust(indent + 8) + '<rdfs:isDefinedBy rdf:resource="' + quote(data.definition_url.strip()) + '"/>\n'
    if data.pred_obj:  # are there additional predicate-object definitions?
        text = os.linesep.join([s for s in data.pred_obj.splitlines() if s])  # remove empty lines
        for po in text.splitlines():
            pred = po.split()[0]
            obj = po[len(pred):].strip()
            rdfStr += padding.rjust(indent + 8) + '<' + pred.strip() + ' rdf:resource="' + quote(obj.strip()) + '"/>\n'
            
    rdfStr += padding.rjust(indent + 6) +'<sh:property>\n'
    rdfStr += padding.rjust(indent + 8) +'<rdf:Description>\n'
    rdfStr += padding.rjust(indent + 8) +'<sh:path rdf:resource="mc-' + mcID + '/xdcount-value"/>\n'
    rdfStr += padding.rjust(indent + 8) +'<sh:datatype rdf:resource="http://www.w3.org/2001/XMLSchema#int"/>\n'
    rdfStr += padding.rjust(indent + 10) +'<sh:maxCount rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">1</sh:maxCount>\n'
    rdfStr += padding.rjust(indent + 10) +'<sh:minCount rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">1</sh:minCount>\n'
    
    if is_valid_decimal(data.min_incl):
        rdfStr += padding.rjust(indent + 10) + '<sh:minInclusive rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">' + data.min_incl.strip() + '</sh:minInclusive>\n'
    elif is_valid_decimal(data.min_excl):
        rdfStr += padding.rjust(indent + 10) + '<sh:minExclusive rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">' + data.min_excl.strip() + '</sh:minExclusive>\n'
    if is_valid_decimal(data.max_incl):
        rdfStr += padding.rjust(indent + 10) + '<sh:maxInclusive rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">' + data.max_incl.strip() + '</sh:maxInclusive>\n'
    elif is_valid_decimal(data.max_excl):
        rdfStr += padding.rjust(indent + 10) + '<sh:maxExclusive rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">' + data.max_excl.strip() + '</sh:maxExclusive>\n'
    rdfStr += padding.rjust(indent + 8) +'</rdf:Description>\n'
    rdfStr += padding.rjust(indent + 6) +'</sh:property>\n'
    
    rdfStr += padding.rjust(indent + 6) + '</rdfs:Class>\n'
    return(rdfStr)


def xdcount(data):
    """
    Create xdCount model used for integers.
    """
    
    adapterID = data.adid.strip()
    mcID = data.mcid.strip()
    unitsID = str(cuid())
    indent = 2
    padding = ('').rjust(indent)
   
    # Adapter
    xdstr = padding.rjust(indent) + '\n<xs:element name="ms-' + adapterID + '" substitutionGroup="s3m:Items" type="s3m:mc-' + adapterID + '"/>\n'
    xdstr += padding.rjust(indent) + '<xs:complexType name="mc-' + adapterID + '">\n'
    xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:XdAdapterType">\n'
    xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="unbounded" minOccurs="0" ref="s3m:ms-' + mcID + '"/>\n'
    xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
    xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
    xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
    xdstr += padding.rjust(indent) + '</xs:complexType>\n'
    # model component
    xdstr += padding.rjust(indent) + '<xs:element name="ms-' + mcID + '" substitutionGroup="s3m:XdAdapter-value" type="s3m:mc-' + mcID + '"/>\n'
    xdstr += padding.rjust(indent) + '<xs:complexType name="mc-' + mcID + '">\n'
    xdstr += padding.rjust(indent + 2) + '<xs:annotation>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:documentation>\n'
    xdstr += padding.rjust(indent + 6) + xml_escape(data.description.strip()) + '\n'
    xdstr += padding.rjust(indent + 4) + '</xs:documentation>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:appinfo>\n'   
    # add the RDF
    xdstr += xdcount_rdf(data)
    xdstr += padding.rjust(indent + 4) + '</xs:appinfo>\n'
    xdstr += padding.rjust(indent + 2) + '</xs:annotation>\n'
    xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:XdCountType">\n'
    xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="label" type="xs:string" fixed="' + data.label.strip() + '"/>\n'
    xdstr += padding.rjust(indent + 8) + '<!-- act -->\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" ref="s3m:ExceptionalValue"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="vtb" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="vte" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="tr" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="modified" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<!-- latitude -->\n'
    xdstr += padding.rjust(indent + 8) + '<!-- longitude -->\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="magnitude-status" type="s3m:MagnitudeStatus"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="error"  type="xs:integer" default="0"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="accuracy" type="xs:integer" default="0"/>\n'
    if data.min_incl.strip().isdigit() or data.max_incl.strip().isdigit() or data.min_excl.strip().isdigit() or data.max_excl.strip().isdigit() or data.def_num.strip().isdigit():
        if data.def_num.strip().isdigit():
            xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1"  name="xdcount-value" type="xs:integer" default="' + str(int(data.def_num)) + '"/>\n'
        else:
            xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1"  name="xdcount-value">\n'
            xdstr += padding.rjust(indent + 10) + '<xs:simpleType>\n'
            xdstr += padding.rjust(indent + 10) + '<xs:restriction base="xs:integer">\n'
            if ddata.min_inclstrip().isdigit():
                xdstr += padding.rjust(indent + 12) + '<xs:minInclusive value="' + str(int(data.min_incl)) + '"/>\n'
            elif data.min_excl.strip().isdigit():
                xdstr += padding.rjust(indent + 12) + '<xs:minExclusive value="' + str(int(data.min_excl)) + '"/>\n'
                
            if data.max_incl.strip().isdigit():
                xdstr += padding.rjust(indent + 12) + '<xs:maxInclusive value="' + str(int(data.max_incl)) + '"/>\n'
            elif data.max_excl.strip().isdigit():
                xdstr += padding.rjust(indent + 12) + '<xs:maxExclusive value="' + str(int(data.max_excl)) + '"/>\n'
                
            xdstr += padding.rjust(indent + 10) + '</xs:restriction>\n'
            xdstr += padding.rjust(indent + 10) + '</xs:simpleType>\n'
            xdstr += padding.rjust(indent + 8) + '</xs:element>\n'
    else:
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1"  name="xdcount-value" type="xs:integer"/>\n'
        
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="xdcount-units" type="s3m:mc-' + unitsID + '"/>\n'
    xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
    xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
    xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
    xdstr += padding.rjust(indent) + '</xs:complexType>\n'

    xdstr += units(unitsID, data)

    return(xdstr)


def xdquantity_rdf(data):
    """
    Create RDF including SHACL constraints for xdQuantity model.
    """
    mcID = data.mcid.strip()    
    rdfStr = ''
    indent = 2
    padding = ('').rjust(indent)
    rdfStr += padding.rjust(indent + 6) + '<rdfs:Class rdf:about="mc-' + mcID + '">\n'
    rdfStr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model_' + RMVERSION + '.xsd#XdQuantityType"/>\n'
    rdfStr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model/RMC"/>\n'
    rdfStr += padding.rjust(indent + 8) + '<rdfs:isDefinedBy rdf:resource="' + quote(data.definition_url.strip()) + '"/>\n'
    if data.pred_obj:  # are there additional predicate-object definitions?
        text = os.linesep.join([s for s in data.pred_obj.splitlines() if s])  # remove empty lines
        for po in text.splitlines():
            pred = po.split()[0]
            obj = po[len(pred):].strip()
            rdfStr += padding.rjust(indent + 8) + '<' + pred.strip() + ' rdf:resource="' + quote(obj.strip()) + '"/>\n'
            
    rdfStr += padding.rjust(indent + 6) +'<sh:property>\n'
    rdfStr += padding.rjust(indent + 8) +'<rdf:Description>\n'
    rdfStr += padding.rjust(indent + 8) +'<sh:path rdf:resource="mc-' + mcID + '/xdquantity-value"/>\n'
    rdfStr += padding.rjust(indent + 8) +'<sh:datatype rdf:resource="http://www.w3.org/2001/XMLSchema#decimal"/>\n'
    rdfStr += padding.rjust(indent + 10) +'<sh:maxCount rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">1</sh:maxCount>\n'
    rdfStr += padding.rjust(indent + 10) +'<sh:minCount rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">1</sh:minCount>\n'
    
    if is_valid_decimal(data.min_incl):
        rdfStr += padding.rjust(indent + 10) + '<sh:minInclusive rdf:datatype="http://www.w3.org/2001/XMLSchema#decimal">' + data.min_incl.strip() + '</sh:minInclusive>\n'
    elif is_valid_decimal(data.min_excl):
        rdfStr += padding.rjust(indent + 10) +'<sh:minExclusive rdf:datatype="http://www.w3.org/2001/XMLSchema#decimal">' + data.min_excl.strip() + '</sh:minExclusive>\n'
        
    if is_valid_decimal(data.max_incl):
        rdfStr += padding.rjust(indent + 10) + '<sh:maxInclusive rdf:datatype="http://www.w3.org/2001/XMLSchema#decimal">' + data.max_incl.strip() + '</sh:maxInclusive>\n'
    elif is_valid_decimal(data.max_excl):
        rdfStr += padding.rjust(indent + 10) +'<sh:maxExclusive rdf:datatype="http://www.w3.org/2001/XMLSchema#decimal">' + data.max_excl.strip() + '</sh:maxExclusive>\n'    
   
    rdfStr += padding.rjust(indent + 8) +'</rdf:Description>\n'
    rdfStr += padding.rjust(indent + 6) +'</sh:property>\n'
    
    rdfStr += padding.rjust(indent + 6) + '</rdfs:Class>\n'
    return(rdfStr)


def xdquantity(data):
    """
    Create xdQuantity model used for decimals.
    """
    
    adapterID = data.adid.strip()
    mcID = data.mcid.strip()
    unitsID = str(cuid())
    indent = 2
    padding = ('').rjust(indent)
    
    # Adapter
    xdstr = padding.rjust(indent) + '\n<xs:element name="ms-' + adapterID + '" substitutionGroup="s3m:Items" type="s3m:mc-' + adapterID + '"/>\n'
    xdstr += padding.rjust(indent) + '<xs:complexType name="mc-' + adapterID + '">\n'
    xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:XdAdapterType">\n'
    xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="unbounded" minOccurs="0" ref="s3m:ms-' + mcID + '"/>\n'
    xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
    xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
    xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
    xdstr += padding.rjust(indent) + '</xs:complexType>\n'
    # model component
    xdstr += padding.rjust(indent) + '<xs:element name="ms-' + mcID + '" substitutionGroup="s3m:XdAdapter-value" type="s3m:mc-' + mcID + '"/>\n'
    xdstr += padding.rjust(indent) + '<xs:complexType name="mc-' + mcID + '">\n'
    xdstr += padding.rjust(indent + 2) + '<xs:annotation>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:documentation>\n'
    xdstr += padding.rjust(indent + 6) + xml_escape(data.description.strip()) + '\n'
    xdstr += padding.rjust(indent + 4) + '</xs:documentation>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:appinfo>\n'
    # add the RDF
    xdstr += xdquantity_rdf(data)
    xdstr += padding.rjust(indent + 4) + '</xs:appinfo>\n'
    xdstr += padding.rjust(indent + 2) + '</xs:annotation>\n'
    xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:XdQuantityType">\n'
    xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="label" type="xs:string" fixed="' + data.label.strip() + '"/>\n'
    xdstr += padding.rjust(indent + 8) + '<!-- act -->\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" ref="s3m:ExceptionalValue"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="vtb" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="vte" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="tr" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="modified" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<!-- latitude -->\n'
    xdstr += padding.rjust(indent + 8) + '<!-- longitude -->\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="magnitude-status" type="s3m:MagnitudeStatus"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="error"  type="xs:integer" default="0"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="accuracy" type="xs:integer" default="0"/>\n'
    if is_valid_decimal(data.min_incl) or is_valid_decimal(data.max_incl) or is_valid_decimal(data.min_excl) or is_valid_decimal(data.max_excl) or is_valid_decimal(data.def_num):
        if is_valid_decimal(data.def_num):
            xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1"  name="xdquantity-value" type="xs:decimal" default="' + data.def_num.strip() + '"/>\n'
        else:
            xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1"  name="xdquantity-value">\n'
            xdstr += padding.rjust(indent + 10) + '<xs:simpleType>\n'
            xdstr += padding.rjust(indent + 10) + '<xs:restriction base="xs:decimal">\n'
            if is_valid_decimal(data.min_incl):
                xdstr += padding.rjust(indent + 12) + '<xs:minInclusive value="' + data.min_incl.strip() + '"/>\n'
            elif is_valid_decimal(data.min_excl):
                xdstr += padding.rjust(indent + 12) + '<xs:minExclusive value="' + data.min_excl.strip() + '"/>\n'
            if is_valid_decimal(data.max_incl):
                xdstr += padding.rjust(indent + 12) + '<xs:maxInclusive value="' + data.max_incl.strip() + '"/>\n'
            elif is_valid_decimal(data.max_excl):
                xdstr += padding.rjust(indent + 12) + '<xs:maxExclusive value="' + data.max_excl.strip() + '"/>\n'
                    
            xdstr += padding.rjust(indent + 10) + '</xs:restriction>\n'
            xdstr += padding.rjust(indent + 10) + '</xs:simpleType>\n'
            xdstr += padding.rjust(indent + 8) + '</xs:element>\n'
    else:
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1"  name="xdquantity-value" type="xs:decimal"/>\n'
        
    xdstr += padding.rjust(indent + 8) +     '<xs:element maxOccurs="1" minOccurs="1" name="xdquantity-units" type="s3m:mc-' + unitsID + '"/>\n'
    xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
    xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
    xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
    xdstr += padding.rjust(indent) + '</xs:complexType>\n'

    xdstr += units(unitsID, data)

    return(xdstr)


def xdfloat_rdf(data):
    """
    Create RDF including SHACL constraints for xdFloat model.
    """
    mcID = data.mcid.strip()    
    rdfStr = ''
    indent = 2
    padding = ('').rjust(indent)
    rdfStr += padding.rjust(indent + 6) + '<rdfs:Class rdf:about="mc-' + mcID + '">\n'
    rdfStr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model_' + RMVERSION + '.xsd#XdFloatType"/>\n'
    rdfStr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model/RMC"/>\n'
    rdfStr += padding.rjust(indent + 8) + '<rdfs:isDefinedBy rdf:resource="' + quote(data.definition_url.strip()) + '"/>\n'
    if data.pred_obj:  # are there additional predicate-object definitions?
        text = os.linesep.join([s for s in data.pred_obj.splitlines() if s]) # remove empty lines
        for po in text.splitlines():
            pred = po.split()[0]
            obj = po[len(pred):].strip()
            rdfStr += padding.rjust(indent + 8) + '<' + pred.strip() + ' rdf:resource="' + quote(obj.strip()) + '"/>\n'
            
    rdfStr += padding.rjust(indent + 6) +'<sh:property>\n'
    rdfStr += padding.rjust(indent + 8) +'<rdf:Description>\n'
    rdfStr += padding.rjust(indent + 8) +'<sh:path rdf:resource="mc-' + mcID + '/xdfloat-value"/>\n'
    rdfStr += padding.rjust(indent + 8) +'<sh:datatype rdf:resource="http://www.w3.org/2001/XMLSchema#float"/>\n'
    rdfStr += padding.rjust(indent + 10) +'<sh:maxCount rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">1</sh:maxCount>\n'
    rdfStr += padding.rjust(indent + 10) +'<sh:minCount rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">1</sh:minCount>\n'
    
    if is_valid_decimal(data.min_incl):
        rdfStr += padding.rjust(indent + 10) + '<sh:minInclusive rdf:datatype="http://www.w3.org/2001/XMLSchema#float">' + data.min_incl.strip() + '</sh:minInclusive>\n'
    elif is_valid_decimal(data.min_excl):
        rdfStr += padding.rjust(indent + 10) +'<sh:minExclusive rdf:datatype="http://www.w3.org/2001/XMLSchema#float">' + data.min_excl.strip() + '</sh:minExclusive>\n'
        
    if is_valid_decimal(data.max_incl):
        rdfStr += padding.rjust(indent + 10) + '<sh:maxInclusive rdf:datatype="http://www.w3.org/2001/XMLSchema#float">' + data.max_incl.strip() + '</sh:maxInclusive>\n'
    elif is_valid_decimal(data.max_excl):
        rdfStr += padding.rjust(indent + 10) +'<sh:maxExclusive rdf:datatype="http://www.w3.org/2001/XMLSchema#float">' + data.max_excl.strip() + '</sh:maxExclusive>\n'    
   
    rdfStr += padding.rjust(indent + 8) +'</rdf:Description>\n'
    rdfStr += padding.rjust(indent + 6) +'</sh:property>\n'
    
    rdfStr += padding.rjust(indent + 6) + '</rdfs:Class>\n'
    return(rdfStr)


def xdfloat(data):
    """
    Create xdFloat model used for floats.
    """
    
    adapterID = data.adid.strip()
    mcID = data.mcid.strip()
    unitsID = str(cuid())
    indent = 2
    padding = ('').rjust(indent)
    
    # Adapter
    xdstr = padding.rjust(indent) + '\n<xs:element name="ms-' + adapterID + '" substitutionGroup="s3m:Items" type="s3m:mc-' + adapterID + '"/>\n'
    xdstr += padding.rjust(indent) + '<xs:complexType name="mc-' + adapterID + '">\n'
    xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:XdAdapterType">\n'
    xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="unbounded" minOccurs="0" ref="s3m:ms-' + mcID + '"/>\n'
    xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
    xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
    xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
    xdstr += padding.rjust(indent) + '</xs:complexType>\n'
    # model component
    xdstr += padding.rjust(indent) + '<xs:element name="ms-' + mcID + '" substitutionGroup="s3m:XdAdapter-value" type="s3m:mc-' + mcID + '"/>\n'
    xdstr += padding.rjust(indent) + '<xs:complexType name="mc-' + mcID + '">\n'
    xdstr += padding.rjust(indent + 2) + '<xs:annotation>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:documentation>\n'
    xdstr += padding.rjust(indent + 6) + xml_escape(data.description.strip()) + '\n'
    xdstr += padding.rjust(indent + 4) + '</xs:documentation>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:appinfo>\n'
    # add the RDF
    xdstr += xdquantity_rdf(data)
    xdstr += padding.rjust(indent + 4) + '</xs:appinfo>\n'
    xdstr += padding.rjust(indent + 2) + '</xs:annotation>\n'
    xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:XdFloatType">\n'
    xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="label" type="xs:string" fixed="' + data.label.strip() + '"/>\n'
    xdstr += padding.rjust(indent + 8) + '<!-- act -->\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" ref="s3m:ExceptionalValue"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="vtb" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="vte" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="tr" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="modified" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<!-- latitude -->\n'
    xdstr += padding.rjust(indent + 8) + '<!-- longitude -->\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="magnitude-status" type="s3m:MagnitudeStatus"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="error"  type="xs:integer" default="0"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="accuracy" type="xs:integer" default="0"/>\n'
    if is_valid_decimal(data.min_incl) or is_valid_decimal(data.max_incl) or is_valid_decimal(data.min_excl) or is_valid_decimal(data.max_excl) or is_valid_decimal(data.def_num):
        if is_valid_decimal(data.def_num):
            xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1"  name="xdfloat-value" type="xs:float" default="' + data.def_num.strip() + '"/>\n'
        else:
            xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1"  name="xdfloat-value">\n'
            xdstr += padding.rjust(indent + 10) + '<xs:simpleType>\n'
            xdstr += padding.rjust(indent + 10) + '<xs:restriction base="xs:float">\n'
            if is_valid_decimal(data.min_incl):
                xdstr += padding.rjust(indent + 12) + '<xs:minInclusive value="' + data.min_incl.strip() + '"/>\n'
            elif is_valid_decimal(data.min_excl):
                xdstr += padding.rjust(indent + 12) + '<xs:minExclusive value="' + data.min_excl.strip() + '"/>\n'
            if is_valid_decimal(data.max_incl):
                xdstr += padding.rjust(indent + 12) + '<xs:maxInclusive value="' + data.max_incl.strip() + '"/>\n'
            elif is_valid_decimal(data.max_excl):
                xdstr += padding.rjust(indent + 12) + '<xs:maxExclusive value="' + data.max_excl.strip() + '"/>\n'
                    
            xdstr += padding.rjust(indent + 10) + '</xs:restriction>\n'
            xdstr += padding.rjust(indent + 10) + '</xs:simpleType>\n'
            xdstr += padding.rjust(indent + 8) + '</xs:element>\n'
    else:
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1"  name="xdfloat-value" type="xs:float"/>\n'
        
    xdstr += padding.rjust(indent + 8) +     '<xs:element maxOccurs="1" minOccurs="0" name="xdfloat-units" type="s3m:mc-' + unitsID + '"/>\n'
    xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
    xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
    xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
    xdstr += padding.rjust(indent) + '</xs:complexType>\n'

    xdstr += units(unitsID, data)

    return(xdstr)


def xdstring_rdf(data):
    """
    Create RDF including SHACL constraints for xdString model.
    """
    mcID = data.mcid.strip()    
    rdfStr = ''
    indent = 2
    padding = ('').rjust(indent)
    rdfStr += padding.rjust(indent + 6) + '<rdfs:Class rdf:about="mc-' + mcID + '">\n'
    rdfStr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model_' + RMVERSION + '.xsd#XdStringType"/>\n'
    rdfStr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model/RMC"/>\n'
    rdfStr += padding.rjust(indent + 8) + '<rdfs:isDefinedBy rdf:resource="' + quote(data.definition_url.strip()) + '"/>\n'
    if data.pred_obj:  # are there additional predicate-object definitions?
        text = os.linesep.join([s for s in data.pred_obj.splitlines() if s]) # remove empty lines
        for po in text.splitlines():
            pred = po.split()[0]
            obj = po[len(pred):].strip()
            rdfStr += padding.rjust(indent + 8) + '<' + pred.strip() + ' rdf:resource="' + quote(obj.strip()) + '"/>\n'
            
    rdfStr += padding.rjust(indent + 6) +'<sh:property>\n'
    rdfStr += padding.rjust(indent + 8) +'<rdf:Description>\n'
    rdfStr += padding.rjust(indent + 10) +'<sh:path rdf:resource="mc-' + mcID + '/xdstring-value"/>\n'
    rdfStr += padding.rjust(indent + 10) +'<sh:datatype rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>\n'
    rdfStr += padding.rjust(indent + 10) +'<sh:maxCount rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">1</sh:maxCount>\n'
    rdfStr += padding.rjust(indent + 10) +'<sh:minCount rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">1</sh:minCount>\n'
    if data.def_text:
        rdfStr += padding.rjust(indent + 10) + '<sh:defaultValue rdf:datatype="http://www.w3.org/2001/XMLSchema#string">' + data.def_text.strip() + '</sh:defaultValue>\n'
    if is_valid_decimal(data.min_len):
        rdfStr += padding.rjust(indent + 10) +'<sh:minLength rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">' + data.min_len.strip() + '</sh:minLength>\n'
        
    if is_valid_decimal(data.max_len):
        rdfStr += padding.rjust(indent + 10) +'<sh:maxLength rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">' + data.max_len.strip() + '</sh:maxLength>\n'
        
    if data.regex:
        rdfStr += padding.rjust(indent + 10) +'<sh:pattern rdf:datatype="http://www.w3.org/2001/XMLSchema#string">' + data.regex.strip() + '</sh:pattern>\n'
        
    rdfStr += padding.rjust(indent + 10) +'\n'
    rdfStr += padding.rjust(indent + 10) +'\n'
    rdfStr += padding.rjust(indent + 10) +'\n'
    rdfStr += padding.rjust(indent + 10) +'\n'
    
    
    rdfStr += padding.rjust(indent + 8) +'</rdf:Description>\n'
    rdfStr += padding.rjust(indent + 6) +'</sh:property>\n'
    
    rdfStr += padding.rjust(indent + 6) + '</rdfs:Class>\n'
    return(rdfStr)


def xdstring(data):
    """
    Create xdString model.
    """

    adapterID = data.adid.strip()
    mcID = data.mcid.strip()
    indent = 2
    padding = ('').rjust(indent)
        
    # Adapter
    xdstr = padding.rjust(indent) + '\n<xs:element name="ms-' + adapterID + '" substitutionGroup="s3m:Items" type="s3m:mc-' + adapterID + '"/>\n'
    xdstr += padding.rjust(indent) + '<xs:complexType name="mc-' + adapterID + '">\n'
    xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:XdAdapterType">\n'
    xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="unbounded" minOccurs="0" ref="s3m:ms-' + mcID + '"/>\n'
    xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
    xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
    xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
    xdstr += padding.rjust(indent) + '</xs:complexType>\n'
    # model component
    xdstr += padding.rjust(indent) + '<xs:element name="ms-' + mcID + '" substitutionGroup="s3m:XdAdapter-value" type="s3m:mc-' + mcID + '"/>\n'
    xdstr += padding.rjust(indent) + '<xs:complexType name="mc-' + mcID + '">\n'
    xdstr += padding.rjust(indent + 2) + '<xs:annotation>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:documentation>\n'
    xdstr += padding.rjust(indent + 6) + xml_escape(data.description.strip()) + '\n'
    xdstr += padding.rjust(indent + 4) + '</xs:documentation>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:appinfo>\n'

    # add the RDF
    xdstr += xdstring_rdf(data)

    xdstr += padding.rjust(indent + 4) + '</xs:appinfo>\n'
    xdstr += padding.rjust(indent + 2) + '</xs:annotation>\n'    
    xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:XdStringType">\n'
    xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="label" type="xs:string" fixed="' + data.label.strip() + '"/>\n'
    xdstr += padding.rjust(indent + 8) + '<!-- act -->\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" ref="s3m:ExceptionalValue"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="vtb" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="vte" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="tr" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="modified" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<!-- latitude -->\n'
    xdstr += padding.rjust(indent + 8) + '<!-- longitude -->\n'

    if not is_valid_decimal(data.min_len) and not is_valid_decimal(data.max_len) and not data.choices and not data.regex and not data.def_text:
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1"  name="xdstring-value" type="xs:string"/>\n'

    elif data.def_text and not is_valid_decimal(data.min_len) and not is_valid_decimal(data.max_len) and not data.choices and not data.regex:
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1"  name="xdstring-value" type="xs:string" default="' + data.def_text.strip() + '"/>\n'

    else:
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1"  name="xdstring-value">\n'
        xdstr += padding.rjust(indent + 10) + '<xs:simpleType>\n'
        xdstr += padding.rjust(indent + 10) + '<xs:restriction base="xs:string">\n'
        if data.choices:
            enums = data.choices.split('|')
            for e in enums:
                xdstr += padding.rjust(indent + 12) + '<xs:enumeration value="' + xml_escape(e.strip()) + '"/>\n'
        else:
            if is_valid_decimal(data.min_len):
                xdstr += padding.rjust(indent + 12) + '<xs:minLength value="' + str(int(data.min_len)).strip() + '"/>\n'
                                                                                    
            if is_valid_decimal(data.max_len):
                xdstr += padding.rjust(indent + 12) + '<xs:maxLength value="' + str(int(data.max_len)).strip() + '"/>\n'
                
            if data.regex:
                xdstr += padding.rjust(indent + 12) + '<xs:pattern value="' + data.regex.strip() + '"/>\n'
        xdstr += padding.rjust(indent + 10) + '</xs:restriction>\n'
        xdstr += padding.rjust(indent + 10) + '</xs:simpleType>\n'
        xdstr += padding.rjust(indent + 8) + '</xs:element>\n'

    xdstr += padding.rjust(indent + 8) + \
        '<xs:element maxOccurs="1" minOccurs="1" name="xdstring-language" type="xs:language" default="en-US"/>\n'
    xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
    xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
    xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
    xdstr += padding.rjust(indent) + '</xs:complexType>\n'

    return(xdstr)


def xdtemporal_rdf(data):
    """
    Create RDF including SHACL constraints for xdTemporal model.
    """
    mcID = data.mcid.strip()    
    rdfStr = ''
    indent = 2
    padding = ('').rjust(indent)
    rdfStr += padding.rjust(indent + 6) + '<rdfs:Class rdf:about="mc-' + mcID + '">\n'
    rdfStr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model_' + RMVERSION + '.xsd#XdTemporalType"/>\n'
    rdfStr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model/RMC"/>\n'
    rdfStr += padding.rjust(indent + 8) + '<rdfs:isDefinedBy rdf:resource="' + quote(data.definition_url.strip()) + '"/>\n'
    if data.pred_obj:  # are there additional predicate-object definitions?
        text = os.linesep.join([s for s in data.pred_obj.splitlines() if s]) # remove empty lines
        for po in text.splitlines():
            pred = po.split()[0]
            obj = po[len(pred):].strip()
            rdfStr += padding.rjust(indent + 8) + '<' + pred.strip() + ' rdf:resource="' + quote(obj.strip()) + '"/>\n'
            
    rdfStr += padding.rjust(indent + 6) +'<sh:property>\n'
    rdfStr += padding.rjust(indent + 8) +'<rdf:Description>\n'
    if data.datatype.lower() == 'date':
        rdfStr += padding.rjust(indent + 8) +'<sh:path rdf:resource="mc-' + mcID + '/xdtemporal-date"/>\n'
        rdfStr += padding.rjust(indent + 8) +'<sh:datatype rdf:resource="http://www.w3.org/2001/XMLSchema#date"/>\n'
    elif data.datatype.lower() == 'time':    
        rdfStr += padding.rjust(indent + 8) +'<sh:path rdf:resource="mc-' + mcID + '/xdtemporal-time"/>\n'
        rdfStr += padding.rjust(indent + 8) +'<sh:datatype rdf:resource="http://www.w3.org/2001/XMLSchema#time"/>\n'
    elif data.datatype.lower() == 'datetime':    
        rdfStr += padding.rjust(indent + 8) +'<sh:path rdf:resource="mc-' + mcID + '/xdtemporal-datetime"/>\n'
        rdfStr += padding.rjust(indent + 8) +'<sh:datatype rdf:resource="http://www.w3.org/2001/XMLSchema#dateTime"/>\n'

    rdfStr += padding.rjust(indent + 10) +'<sh:maxCount rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">1</sh:maxCount>\n'
    rdfStr += padding.rjust(indent + 10) +'<sh:minCount rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">1</sh:minCount>\n'
        
    rdfStr += padding.rjust(indent + 8) +'</rdf:Description>\n'
    rdfStr += padding.rjust(indent + 6) +'</sh:property>\n'
    
    rdfStr += padding.rjust(indent + 6) + '</rdfs:Class>\n'
    return(rdfStr)


def xdtemporal(data):
    """
    Create xdTemporal model used for dates & times.
    """
    
    adapterID = data.adid.strip()
    mcID = data.mcid.strip()
    indent = 2
    padding = ('').rjust(indent)
    
    # Adapter
    xdstr = padding.rjust(indent) + '\n<xs:element name="ms-' + adapterID + '" substitutionGroup="s3m:Items" type="s3m:mc-' + adapterID + '"/>\n'
    xdstr += padding.rjust(indent) + '<xs:complexType name="mc-' + adapterID + '">\n'
    xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:XdAdapterType">\n'
    xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="unbounded" minOccurs="0" ref="s3m:ms-' + mcID + '"/>\n'
    xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
    xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
    xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
    xdstr += padding.rjust(indent) + '</xs:complexType>\n'
    # model component
    xdstr += padding.rjust(indent) + '<xs:element name="ms-' + mcID + '" substitutionGroup="s3m:XdAdapter-value" type="s3m:mc-' + mcID + '"/>\n'
    xdstr += padding.rjust(indent) + '<xs:complexType name="mc-' + mcID + '">\n'
    xdstr += padding.rjust(indent + 2) + '<xs:annotation>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:documentation>\n'
    xdstr += padding.rjust(indent + 6) + xml_escape(data.description.strip()) + '\n'
    xdstr += padding.rjust(indent + 4) + '</xs:documentation>\n'
    
    xdstr += padding.rjust(indent + 4) + '<xs:appinfo>\n'
    # add the RDF
    xdstr += xdtemporal_rdf(data)
    xdstr += padding.rjust(indent + 4) + '</xs:appinfo>\n'

    
    xdstr += padding.rjust(indent + 2) + '</xs:annotation>\n'
    xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:XdTemporalType">\n'
    xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="label" type="xs:string" fixed="' + data.label.strip() + '"/>\n'
    xdstr += padding.rjust(indent + 8) + '<!-- act -->\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" ref="s3m:ExceptionalValue"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="vtb" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="vte" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="tr" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="modified" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<!-- latitude -->\n'
    xdstr += padding.rjust(indent + 8) + '<!-- longitude -->\n'
    if data.datatype.lower() == 'date':
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="xdtemporal-date" type="xs:date"/>\n'
    else:
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="0" minOccurs="0" name="xdtemporal-date" type="xs:date"/>\n'

    if data.datatype.lower() == 'time':
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="xdtemporal-time" type="xs:time"/>\n'
    else:
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="0" minOccurs="0" name="xdtemporal-time" type="xs:time"/>\n'

    if data.datatype.lower() == 'datetime':
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="xdtemporal-datetime" type="xs:dateTime"/>\n'
    else:
        xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="0" minOccurs="0" name="xdtemporal-datetime" type="xs:dateTime"/>\n'

    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="0" minOccurs="0" name="xdtemporal-day" type="xs:gDay"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="0" minOccurs="0" name="xdtemporal-month" type="xs:gMonth"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="0" minOccurs="0" name="xdtemporal-year" type="xs:gYear"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="0" minOccurs="0" name="xdtemporal-year-month" type="xs:gYearMonth"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="0" minOccurs="0" name="xdtemporal-month-day" type="xs:gMonthDay"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="0" minOccurs="0" name="xdtemporal-duration" type="xs:duration"/>\n'
    xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
    xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
    xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
    xdstr += padding.rjust(indent) + '</xs:complexType>\n'

    return(xdstr)


def units(mcID, data):
    """
    Create xdString model as a Units component of a xdCount or xdQuantity.
    """
    
    indent = 2
    padding = ('').rjust(indent)
    xdstr = padding.rjust(indent) + '<xs:complexType name="mc-' + mcID + '">\n'
    xdstr += padding.rjust(indent + 2) + '<xs:annotation>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:documentation>\n'
    xdstr += padding.rjust(indent + 6) + 'Unit constraint for: ' + xml_escape(data.description.strip()) + '\n'
    xdstr += padding.rjust(indent + 4) + '</xs:documentation>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:appinfo>\n'
    xdstr += padding.rjust(indent + 6) + '<rdfs:Class rdf:about="mc-' + mcID + '">\n'
    xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model_' + RMVERSION + '.xsd#XdStringType"/>\n'
    xdstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model/RMC"/>\n'
    xdstr += padding.rjust(indent + 8) + '<rdfs:isDefinedBy rdf:resource="' + quote(data.definition_url.strip()) + '"/>\n'
    if data.pred_obj:  # are there additional predicate-object definitions?
        for po in data.pred_obj.splitlines():
            pred = po.split()[0]
            obj = po[len(pred):].strip()
            xdstr += padding.rjust(indent + 8) + '<' + pred.strip() + ' rdf:resource="' + quote(obj.strip()) + '"/>\n'
    xdstr += padding.rjust(indent + 6) + '</rdfs:Class>\n'
    xdstr += padding.rjust(indent + 4) + '</xs:appinfo>\n'
    xdstr += padding.rjust(indent + 2) + '</xs:annotation>\n'
    xdstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
    xdstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:XdStringType">\n'
    xdstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="label" type="xs:string" fixed="' + data.label.strip() + ' Units"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" ref="s3m:ExceptionalValue"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="vtb" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="vte" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="tr" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" name="modified" type="xs:dateTime"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1"  name="xdstring-value" type="xs:string" fixed="' + data.def_text.strip() + '"/>\n'
    xdstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="xdstring-language" type="xs:language" default="en-US"/>\n'
    xdstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
    xdstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
    xdstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
    xdstr += padding.rjust(indent) + '</xs:complexType>\n'

    return(xdstr)


def xsd_data(rec, indent, session):
    """
    Create a Cluster model for the data portion of an Entry.
    """
    
    indent += 2
    padding = ('').rjust(indent)
    dstr = padding.rjust(indent) + '<xs:element name="ms-' + rec.dataid + '" substitutionGroup="s3m:Item" type="s3m:mc-' + rec.dataid + '"/>\n'
    dstr += padding.rjust(indent) + '<xs:complexType name="mc-' + rec.dataid + '">\n'
    dstr += padding.rjust(indent + 2) + '<xs:annotation>\n'
    dstr += padding.rjust(indent + 4) + '<xs:documentation>\n'
    dstr += padding.rjust(indent + 6) + 'This is the Cluster that groups all of the data items (columns) definitions into one unit.\n'
    dstr += padding.rjust(indent + 4) + '</xs:documentation>\n'
    dstr += padding.rjust(indent + 4) + '<xs:appinfo>\n'
    dstr += padding.rjust(indent + 6) + '<rdfs:Class rdf:about="mc-' + rec.dataid + '">\n'
    dstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model_' + RMVERSION + '.xsd#ClusterType"/>\n'
    dstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model/RMC"/>\n'
    dstr += padding.rjust(indent + 8) + '<rdfs:isDefinedBy rdf:resource="' + rec.definition_url + '"/>\n'
    dstr += padding.rjust(indent + 6) + '</rdfs:Class>\n'
    dstr += padding.rjust(indent + 4) + '</xs:appinfo>\n'
    dstr += padding.rjust(indent + 2) + '</xs:annotation>\n'
    dstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
    dstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:ClusterType">\n'
    dstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
    dstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="1" name="label" type="xs:string" fixed="Data Items"/>\n'

    # now we need to loop through the db and create all of the model components while keeping track so we can add them here too.
    # the dictionary uses the mc-{cuid} as the key. The items are the complete mc code.
    mcDict = OrderedDict()
    components = session.query(Component).filter_by(model_id=rec.id).all()
    
    for row in components:
        if row.datatype.lower() == 'integer':
            mcDict[row.adid.strip()] = xdcount(row)
        elif row.datatype.lower() == 'decimal':
            mcDict[row.adid.strip()] = xdquantity(row)
        elif row.datatype.lower() in ('date', 'datetime', 'time'):
            mcDict[row.adid.strip()] = xdtemporal(row)
        elif row.datatype.lower() == 'string':
            mcDict[row.adid.strip()] = xdstring(row)
        elif row.datatype.lower() == 'float':
            mcDict[row.adid.strip()] = xdfloat(row)
        else:
            raise ValueError("Invalid datatype. The type " + row.datatype + " is not a valid choice.")

    for mc_id in mcDict.keys():
        dstr += padding.rjust(indent + 8) + '<xs:element maxOccurs="1" minOccurs="0" ref="s3m:ms-' + mc_id + '"/>\n'

    dstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
    dstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
    dstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
    dstr += padding.rjust(indent) + '</xs:complexType>\n\n'

    for mc_id in mcDict.keys():
        dstr += mcDict[mc_id]

    return(dstr)


def xsd_dm(rec):
    """
    Create the Data Model wrapper for the metadata and the data Cluster.
    """
    
    indent = 2
    padding = ('').rjust(indent)

    dmstr = padding.rjust(indent) + '<xs:element name="dm-' + rec.dmid.strip() + '" type="s3m:mc-' + rec.dmid.strip() + '"/>\n'
    dmstr += padding.rjust(indent) + '<xs:complexType name="mc-' + rec.dmid.strip() + '">\n'
    dmstr += padding.rjust(indent + 2) + '<xs:annotation>\n'
    dmstr += padding.rjust(indent + 4) + '<xs:documentation>\n'
    dmstr += padding.rjust(indent + 6) + xml_escape(rec.description.strip()) + '\n'
    dmstr += padding.rjust(indent + 4) + '</xs:documentation>\n'
    dmstr += padding.rjust(indent + 4) + '<xs:appinfo>\n'
    dmstr += padding.rjust(indent + 6) + '<rdfs:Class rdf:about="mc-' + rec.dmid.strip() + '">\n'
    dmstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model_' + RMVERSION + '.xsd#DMType"/>\n'
    dmstr += padding.rjust(indent + 8) + '<rdfs:subClassOf rdf:resource="https://www.s3model.com/ns/s3m/s3model/RMC"/>\n'
    dmstr += padding.rjust(indent + 8) + '<rdfs:isDefinedBy rdf:resource="' + quote(rec.definition_url.strip()) + '"/>\n'
    dmstr += padding.rjust(indent + 6) + '</rdfs:Class>\n'
    dmstr += padding.rjust(indent + 4) + '</xs:appinfo>\n'
    dmstr += padding.rjust(indent + 2) + '</xs:annotation>\n'
    dmstr += padding.rjust(indent + 2) + '<xs:complexContent>\n'
    dmstr += padding.rjust(indent + 4) + '<xs:restriction base="s3m:DMType">\n'
    dmstr += padding.rjust(indent + 6) + '<xs:sequence>\n'
    dmstr += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='label' type='xs:string' fixed=" + '"' + escape(rec.title.strip()) + '"' + "/>\n")
    # TODO: add language, encoding & current state elements to DB
    dmstr += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='dm-language' type='xs:language' fixed='" + 'en-US' + "'/>\n")
    dmstr += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' name='dm-encoding' type='xs:string' fixed='" + 'utf-8' + "'/>\n")
    dmstr += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='0' name='current-state' type='xs:string' default='" + 'new' + "'/>\n")
    dmstr += padding.rjust(indent + 8) + ("<xs:element maxOccurs='1' minOccurs='1' ref='s3m:ms-" + str(rec.dataid) + "'/>\n")
    dmstr += padding.rjust(indent + 8) + '<!-- subject -->\n'
    dmstr += padding.rjust(indent + 8) + '<!-- provider -->\n'
    dmstr += padding.rjust(indent + 8) + '<!-- participations -->\n'
    dmstr += padding.rjust(indent + 8) + '<!-- protocol -->\n'
    dmstr += padding.rjust(indent + 8) + '<!-- workflow -->\n'
    dmstr += padding.rjust(indent + 8) + '<!-- acs -->\n'
    dmstr += padding.rjust(indent + 8) + '<!-- audit -->\n'
    dmstr += padding.rjust(indent + 8) + '<!-- attestation -->\n'
    dmstr += padding.rjust(indent + 8) + '<!-- entry links -->\n'
    dmstr += padding.rjust(indent + 6) + '</xs:sequence>\n'
    dmstr += padding.rjust(indent + 4) + '</xs:restriction>\n'
    dmstr += padding.rjust(indent + 2) + '</xs:complexContent>\n'
    dmstr += padding.rjust(indent) + '</xs:complexType>\n'
    return(dmstr)


def xsd_rdf(rec, session):
    """
        Generate the RDF from the semantics embedded in the XSD.
        """

    rootdir = '.'
    ns_dict = {'xs': 'http://www.w3.org/2001/XMLSchema',
              'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
              'xsd': 'http://www.w3.org/2001/XMLSchema#',
              'dc': 'http://purl.org/dc/elements/1.1/',
              'skos': 'http://www.w3.org/2004/02/skos/core#',
              'foaf': 'http://xmlns.com/foaf/0.1/',
              'schema': 'http://schema.org/',
              'sioc': 'http://rdfs.org/sioc/ns#',
              'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
              'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
              'dct': 'http://purl.org/dc/terms/',
              'owl': 'http://www.w3.org/2002/07/owl#',
              'sh': 'http://www.w3.org/ns/shacl#',
              'vc': 'http://www.w3.org/2007/XMLSchema-versioning',
              's3m': 'https://www.s3model.com/ns/s3m/'}

    print("\nGenerating RDF for Datamodel : dm-" + rec.dmid + '.xsd\n')

    if rec.namespaces is not None:
        for ns in rec.namespaces.splitlines():
            ns_dict[ns.split('=')[0]]=ns.split('=')[1]

    # parser = etree.XMLParser(ns_clean=True, recover=True)
    cls_def = etree.XPath("//xs:annotation/xs:appinfo/rdfs:Class", namespaces=ns_dict)
    sh_def = etree.XPath("//xs:annotation/xs:appinfo/sh:property", namespaces=ns_dict)

    md = etree.XPath("//rdf:RDF/rdfs:Class", namespaces=ns_dict)

    rdfstr = """<?xml version="1.0" encoding="UTF-8"?>\n<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#' \nxmlns:s3m='https://www.s3model.com/ns/s3m/'>\n"""

    # have to remove the encoding declaration and stylesheet pointer
    xsd_str = rec.schema.replace('<?xml version="1.0" encoding="UTF-8"?>','')
    xsd_str = xsd_str.replace('<?xml-stylesheet type="text/xsl" href="dm-description.xsl"?>','')
    tree = etree.parse(StringIO(xsd_str))
    root = tree.getroot()

    rdf = cls_def(root)
    shacl = sh_def(root)
    
    for s in shacl:
        rdfstr += '    ' + etree.tostring(s).decode('utf-8') + '\n'
        
    for m in md(root):
        rdfstr += '    ' + etree.tostring(m).decode('utf-8') + '\n'

    for r in rdf:
        rdfstr += '    ' + etree.tostring(r).decode('utf-8') + '\n'

    # create triples for all of the Components of this Model
    cols = session.query(Component).filter_by(model_id=rec.id).all()
    for col in cols:
        rdfstr += '<rdfs:Class xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"  xmlns:s3m="https://www.s3model.com/ns/s3m/" rdf:about="s3m:ms-' + col.mcid.strip() + '">\n'
        rdfstr += '  <s3m:isRMSOf rdf:resource="s3m:mc-' + col.mcid.strip() + '"/>\n'
        rdfstr += '</rdfs:Class>\n'

    rdfstr += '</rdf:RDF>\n'
    
    rec.rdf = rdfstr
    session.commit()
    exit(1)
    
    
    #if config['ALLEGROGRAPH']['status'].upper() == "ACTIVE":
        ## Set environment variables for AllegroGraph
        #os.environ['AGRAPH_HOST'] = config['ALLEGROGRAPH']['host']
        #os.environ['AGRAPH_PORT'] = config['ALLEGROGRAPH']['port']
        #os.environ['AGRAPH_USER'] = config['ALLEGROGRAPH']['user']
        #os.environ['AGRAPH_PASSWORD'] = config['ALLEGROGRAPH']['password']            
        #try:
            #from franz.openrdf.connect import ag_connect
            #connRDF = ag_connect(config['ALLEGROGRAPH']['repo'], host=os.environ.get('AGRAPH_HOST'), port=os.environ.get('AGRAPH_PORT'),  user=os.environ.get('AGRAPH_USER'), password=os.environ.get('AGRAPH_PASSWORD'))
            #print('Current Kunteksto RDF Repository Size: ', connRDF.size(), '\n')
            #print('AllegroGraph connections are okay.\n\n')
        #except: 
            #connRDF = None
            #print("Unexpected error: ", sys.exc_info()[0])
            #print('RDF Connection Error', 'Could not create connection to AllegroGraph.')

        #if connRDF:
            #try:
                #connRDF.addData(rdfstr, rdf_format=RDFFormat.RDFXML, base_uri=None, context=None)
            #except Exception as e:
                #print('\n\nAllegroGraphDB Error: Could not load the Model RDF for ' + xsdfile + '\n' + str(e.args) + '\n')
                #sys.exit(1)                    

def make_model(project):
    """
    Create an S3M data model schema based on the database information.
    """
    session = Session()
    rec = session.query(Datamodel).filter_by(project=project).first()

    dmID = rec.dmid

    print("\nGenerating Datamodel : dm-" + dmID + '.xsd\n')
    #xsd = open(model, 'w')

    xsd_str = xsd_header(rec)
    xsd_str += xsd_metadata(rec)
    xsd_str += xsd_dm(rec)
    xsd_str += xsd_data(rec, 0, session)
    xsd_str += '\n</xs:schema>\n'
    
    # persist a copy so we can troubleshoot for erros when needed.
    rec.schema = xsd_str
    session.commit()
    
    try:
        xmlschema_doc = etree.fromstring(xsd_str)
    except Exception as e:
        # print('\nModel Error', "There was an error in generating the schema. \nPlease re-edit the database and look for errors.\n You probably have undefined namespaces or improperly formatted predicate-object pair.\n")
        print('\n\n', e)
        sys.exit(1)
    
    # Must add the encoding declation after checking the schema.
    xsd_str = '<?xml version="1.0" encoding="UTF-8"?>\n' + xsd_str
    rec.schema = xsd_str
    session.commit()
    
    xsd_rdf(rec, session)

    return


def xml_hdr(rec):
    xstr = '<s3m:dm-' + rec.dmid.strip() + '\n'
    xstr += 'xmlns:s3m="https://www.s3model.com/ns/s3m/"\n'
    xstr += 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n'
    xstr += 'xsi:schemaLocation="https://www.s3model.com/ns/s3m/ https://s3model.com/dmlib/dm-' + rec.dmid.strip() + '.xsd">\n'
    xstr += '    <label>' + xml_escape(rec.title.strip()) + '</label>\n'
    xstr += '    <dm-language>en-US</dm-language>\n'
    xstr += '    <dm-encoding>utf-8</dm-encoding>\n'
    xstr += '    <current-state>new</current-state>\n'    
    xstr += '    <s3m:ms-' + rec.dataid.strip() + '>\n'
    xstr += '      <label>Data Items</label>\n'
    return(xstr)


def xml_count(col, data):
    xstr = '      <s3m:ms-' + col.adid.strip() + '>\n'
    xstr += '      <s3m:ms-' + col.mcid.strip() + '>\n'
    xstr += '        <label>' + col.label.strip() + '</label>\n'
    xstr += '        <magnitude-status>equal</magnitude-status>\n'
    xstr += '        <error>0</error>\n'
    xstr += '        <accuracy>0</accuracy>\n'
    xstr += '        <xdcount-value>' + data[col.header.strip()] + '</xdcount-value>\n'
    xstr += '        <xdcount-units>\n'
    xstr += '          <label>' + xml_escape(col.label.strip()) + ' Units</label>\n'
    xstr += '          <xdstring-value>' + xml_escape(col.units.strip()) + '</xdstring-value>\n'
    xstr += '          <xdstring-language>en-US</xdstring-language>\n'
    xstr += '        </xdcount-units>\n'
    xstr += '      </s3m:ms-' + col.mcid.strip() + '>\n'
    xstr += '      </s3m:ms-' + col.adid.strip() + '>\n'
    return(xstr)


def rdf_count(col, data):
    rstr = '      <rdfs:Class rdf:about="s3m:ms-' + col.mcid.strip() + '">\n'
    rstr += '        <rdfs:label>' + xml_escape(col.label.strip()) + '</rdfs:label>\n'
    rstr += '        <rdfs:value rdf:datatype="xs:integer">' + data[col.header.strip()] + '</rdfs:value>\n'
    rstr += '      </rdfs:Class>\n'
    return(rstr)


def xml_quantity(col, data):
    xstr = '      <s3m:ms-' + col.adid.strip() + '>\n'
    xstr += '      <s3m:ms-' + col.mcid.strip() + '>\n'
    xstr += '        <label>' + xml_escape(col.label.strip()) + '</label>\n'
    xstr += '        <magnitude-status>equal</magnitude-status>\n'
    xstr += '        <error>0</error>\n'
    xstr += '        <accuracy>0</accuracy>\n'
    xstr += '        <xdquantity-value>' + data[col.header.strip()] + '</xdquantity-value>\n'
    xstr += '        <xdquantity-units>\n'
    xstr += '          <label>' + xml_escape(col.label.strip()) + ' Units</label>\n'
    xstr += '          <xdstring-value>' + xml_escape(col.units.strip()) + '</xdstring-value>\n'
    xstr += '          <xdstring-language>en-US</xdstring-language>\n'
    xstr += '        </xdquantity-units>\n'
    xstr += '      </s3m:ms-' + col.mcid.strip() + '>\n'
    xstr += '      </s3m:ms-' + col.adid.strip() + '>\n'
    return(xstr)


def rdf_quantity(col, data):
    rstr = '      <rdfs:Class rdf:about="s3m:ms-' + col.mcid.strip() + '">\n'
    rstr += '        <rdfs:label>' + xml_escape(col.label.strip()) + '</rdfs:label>\n'
    rstr += '        <rdfs:value rdf:datatype="xs:decimal">' + data[col.header.strip()] + '</rdfs:value>\n'
    rstr += '      </rdfs:Class>\n'
    return(rstr)


def xml_float(col, data):
    xstr = '      <s3m:ms-' + col.adid.strip() + '>\n'
    xstr += '      <s3m:ms-' + col.mcid.strip() + '>\n'
    xstr += '        <label>' + col.label.strip() + '</label>\n'
    xstr += '        <magnitude-status>equal</magnitude-status>\n'
    xstr += '        <error>0</error>\n'
    xstr += '        <accuracy>0</accuracy>\n'
    xstr += '        <xdfloat-value>' + data[col.header.strip()] + '</xdfloat-value>\n'
    xstr += '        <xdfloat-units>\n'
    xstr += '          <label>' + xml_escape(col.label.strip()) + ' Units</label>\n'
    xstr += '          <xdstring-value>' + xml_escape(col.units.strip()) + '</xdstring-value>\n'
    xstr += '          <xdstring-language>en-US</xdstring-language>\n'
    xstr += '        </xdfloat-units>\n'
    xstr += '      </s3m:ms-' + col.mcid.strip() + '>\n'
    xstr += '      </s3m:ms-' + col.adid.strip() + '>\n'
    return(xstr)

def rdf_float(col, data):
    rstr = '      <rdfs:Class rdf:about="s3m:ms-' + col.mcid.strip() + '">\n'
    rstr += '        <rdfs:label>' + xml_escape(col.label.strip()) + '</rdfs:label>\n'
    rstr += '        <rdfs:value rdf:datatype="xs:float">' + data[col.header.strip()] + '</rdfs:value>\n'
    rstr += '      </rdfs:Class>\n'
    return(rstr)


def xml_temporal(col, data):
    xstr = '      <s3m:ms-' + col.adid.strip() + '>\n'
    xstr += '      <s3m:ms-' + col.mcid.strip() + '>\n'
    xstr += '        <label>' + xml_escape(col.label.strip()) + '</label>\n'
    if col.datatype.lower() == 'date':
        xstr += '        <xdtemporal-date>' + data[col.header.strip()] + '</xdtemporal-date>\n'
    if col.datatype.lower() == 'time':
        xstr += '        <xdtemporal-time>' + data[col.header.strip()] + '</xdtemporal-time>\n'
    if col.datatype.lower() == 'datetime':
        xstr += '        <xdtemporal-datetime>' + data[col.header.strip()] + '</xdtemporal-datetime>\n'
    xstr += '      </s3m:ms-' + col.mcid.strip() + '>\n'
    xstr += '      </s3m:ms-' + col.adid.strip() + '>\n'
    return(xstr)


def rdf_temporal(col, data):
    rstr = '      <rdfs:Class rdf:about="s3m:ms-' + col.mcid.strip() + '">\n'
    rstr += '        <rdfs:label>' + xml_escape(col.label.strip()) + '</rdfs:label>\n'
    if col.datatype.lower() == 'date':
        rstr += '        <rdfs:value rdf:datatype="xs:date">' + data[col.header.strip()] + '</rdfs:value>\n'
    if col.datatype.lower() == 'time':
        rstr += '        <rdfs:value rdf:datatype="xs:time">' + data[col.header.strip()] + '</rdfs:value>\n'
    if col.datatype.lower() == 'datetime':
        rstr += '        <rdfs:value rdf:datatype="xs:dateTime">' + data[col.header.strip()] + '</rdfs:value>\n'
    rstr += '      </rdfs:Class>\n'
    return(rstr)


def xml_string(col, data):
    xstr = '      <s3m:ms-' + col.adid.strip() + '>\n'
    xstr += '      <s3m:ms-' + col.mcid.strip() + '>\n'
    xstr += '        <label>' + xml_escape(col.label.strip()) + '</label>\n'
    xstr += '        <xdstring-value>' + xml_escape(data[col.header.strip()]) + '</xdstring-value>\n'
    xstr += '        <xdstring-language>en-US</xdstring-language>\n'
    xstr += '      </s3m:ms-' + col.mcid.strip() + '>\n'
    xstr += '      </s3m:ms-' + col.adid.strip() + '>\n'
    return(xstr)


def rdf_string(col, data):
    rstr = '      <rdfs:Class rdf:about="s3m:ms-' + col.mcid.strip() + '">\n'
    rstr += '        <rdfs:label>' + xml_escape(col.label.strip()) + '</rdfs:label>\n'
    rstr += '        <rdfs:value rdf:datatype="xs:string">' + xml_escape(data[col.header.strip()]) + '</rdfs:value>\n'
    rstr += '      </rdfs:Class>\n'
    return(rstr)


def injectEV(xmlStr, code, msg, path):
    """
    Based on the error inject an Exceptional Value tag into the XML instance.
    Return the updated XML instance and the RDF error information.
    """
    
    ns_dict = {'xs': 'http://www.w3.org/2001/XMLSchema',
              'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
              'xsd': 'http://www.w3.org/2001/XMLSchema#',
              'dc': 'http://purl.org/dc/elements/1.1/',
              'skos': 'http://www.w3.org/2004/02/skos/core#',
              'foaf': 'http://xmlns.com/foaf/0.1/',
              'schema': 'http://schema.org/',
              'sioc': 'http://rdfs.org/sioc/ns#',
              'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
              'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
              'dct': 'http://purl.org/dc/terms/',
              'owl': 'http://www.w3.org/2002/07/owl#',
              'sh': 'http://www.w3.org/ns/shacl#',
              'vc': 'http://www.w3.org/2007/XMLSchema-versioning',
              's3m': 'https://www.s3model.com/ns/s3m/'}
    
    parser = etree.XMLParser(remove_blank_text=True)
    root = etree.XML(xmlStr, parser=parser)
    
    mcPath = etree.XPath(path[0:path.rfind('/')], namespaces=ns_dict)
    labelPath = etree.XPath(path[0:path.rfind('/')] + '/label', namespaces=ns_dict)
    actPath = etree.XPath(path[0:path.rfind('/')] + '/act', namespaces=ns_dict)
    
    
    # schema validation erros are 1801 - 1879 see: http://lxml.de/api/lxml.etree.ErrorTypes-class.html
    error2ev = {1824:['INV','Invalid'], 1825:['INV','Invalid'], 1826:['INV','Invalid'], 1833:['INV','Invalid'], 1845:['INV','Invalid'], 1846:['INV','Invalid'], \
                1847:['INV','Invalid'], 1848:['INV','Invalid'], 1849:['INV','Invalid'], 1850:['INV','Invalid'], 1851:['INV','Invalid'], 1852:['INV','Invalid'], \
                1853:['INV','Invalid'], 1854:['INV','Invalid'], 1855:['INV','Invalid'], 1856:['INV','Invalid'], 1857:['INV','Invalid'], 1858:['INV','Invalid'], \
                1859:['INV','Invalid'], 1860:['INV','Invalid'], 1840:['OTH','Other'], 1829:['OTH','Other'], 1838:['OTH','Other'], 1877:['OTH','Other'], 1840:['OTH','Other'], \
                1830:['OTH','Other'], 1836:['OTH','Other'], 1834:['OTH','Other'], 1832:['OTH','Other'], 1835:['OTH','Other'], 1833:['OTH','Other'], 1831:['OTH','Other'], \
                1839:['OTH','Other'], 1837:['OTH','Other'], 1875:['OTH','Other'], 1876:['OTH','Other'], 1827:['OTH','Other'], 1828:['OTH','Other'], 1878:['OTH','Other']}

    # best fit Exceptional Value element base on error message the default is the NI element.
    errname = error2ev.get(code, ['NI','No Information'])
    qname = etree.QName('https://www.s3model.com/ns/s3m/', errname[0])
    ev_text = errname[1]
        
    # Create a human readable comment just to be nice
    comment = etree.Comment(text = "ERROR MSG: " + msg)
    
    # Create the element tree to insert
    ev_element = etree.Element(qname)
    evname = etree.Element('ev-name')
    evname.text = ev_text
    ev_element.insert(0, evname)
        
    # Insert the element
    if actPath(root):
        actPath(root)[0].addnext(ev_element)
        actPath(root)[0].addnext(comment)
    if labelPath(root):
        labelPath(root)[0].addnext(ev_element)
        labelPath(root)[0].addnext(comment)


    xmlStr = etree.tostring(root, pretty_print=True, encoding="unicode")
    return(xmlStr)


def make_data(project, infile):
    """
    Create XML and JSON data files and an RDF graph based on the model.
    """
    session = Session()
    rec = session.query(Datamodel).filter_by(project=project).first()
    cols = session.query(Component).filter_by(model_id=rec.id).all()
    
    # begin a validation log
    vlsession = Session()
    vlog = Validation(model_id=rec.id, log='id,status,error\n')
    vlsession.add(vlog)
    vlsession.flush()
    
    xmldb = rec.xmlstore
    jsondb = rec.jsonstore
    rdfdb = rec.rdfstore
    
    # if filesystem persistence is defined insure the paths + project name exist
    if xmldb.dbtype == 'fs':
        path = Path(os.path.join(xmldb.host.strip(), rec.project.strip()))
        path.mkdir(parents=True)

    if rdfdb.dbtype == 'fs':
        path = Path(os.path.join(rdfdb.host.strip(), rec.project.strip()))
        path.mkdir(parents=True)
            
    if jsondb.dbtype == 'fs':
        path = Path(os.path.join(jsondb.host.strip(), rec.project.strip()))
        path.mkdir(parents=True)
            
    try:
        xsd_str = rec.schema.replace('<?xml version="1.0" encoding="UTF-8"?>','')
        xsd_str = xsd_str.replace('<?xml-stylesheet type="text/xsl" href="dm-description.xsl"?>','')
        schema = etree.parse(StringIO(xsd_str))        
        modelSchema = etree.XMLSchema(schema)
    except etree.XMLSchemaParseError as e:
        print("\n\nCannot parse this schema. Please check the database for errors.\n" + str(e.args))
        sys.exit(1)

    print('\n\nGeneration: ', "Generate data for project: " + rec.project + ' using ' + infile + '\n')

    namespaces = {"https://www.s3model.com/ns/s3m/": "s3m", "http://www.w3.org/2001/XMLSchema-instance": "xsi"}
    
    # count the lines in the file
    with open(infile) as f:
        s = f.read()
    csv_len =  s.count('\n') - 1
    f.close()
    
    with open(infile) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=DELIM)
        
        # this test is for the 'generate' mode to insure the model matches the input CSV file. 
        print('\nChecking that data file matches model.\n')
        hdrs = reader.fieldnames
        
        for i in range(0,len(hdrs)):
            col = session.query(Component).filter_by(model_id=rec.id).filter_by(header=hdrs[i]).first()
            if col == None:
                print("\n\nThere was an error matching the data input file to the selected model database.")
                print('The Datafile contains a header label, ' + hdrs[i] + ' that does not match the Component headers. \n\n')
                exit(code=1)
        
        # for data in reader:
        with click.progressbar(reader, label="Creating a total of " + str(csv_len) + " data files: ", length=csv_len) as bar:
            for data in bar:
                file_id = rec.project.strip() + '-' + shortuuid.uuid()    
                xmlProlog = '<?xml version="1.0" encoding="UTF-8"?>\n'  # lxml doesn't want this in the file during validation, it has to be reinserted afterwards.     
                xmlStr = ''
                rdfStr = '<?xml version="1.0" encoding="UTF-8"?>\n<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\nxmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"\nxmlns:s3m="https://www.s3model.com/ns/s3m/"\nxmlns:xs="http://www.w3.org/2001/XMLSchema">\n'
                rdfStr += '<rdfs:Class rdf:about="' + file_id + '">\n'
                rdfStr += '  <s3m:isInstanceOf rdf:resource="dm-' + rec.dmid.strip() + '"/>\n'
                rdfStr += '</rdfs:Class>\n'
    
                # get the DM tag content.
                xmlStr += xml_hdr(rec)          
    
                # get the data element for each type with the data from the CSV.
                for col in cols:
                    if col.datatype.lower() == 'integer':
                        xmlStr += xml_count(col, data)
                        rdfStr += rdf_count(col, data)
                    elif col.datatype.lower() == 'decimal':
                        xmlStr += xml_quantity(col, data)
                        rdfStr += rdf_quantity(col, data)
                    elif col.datatype.lower() == 'float':
                        xmlStr += xml_float(col, data)
                        rdfStr += rdf_float(col, data)
                    elif col.datatype.lower() in ('date', 'datetime', 'time'):
                        xmlStr += xml_temporal(col, data)
                        rdfStr += rdf_temporal(col, data)
                    elif col.datatype.lower() == 'string':
                        xmlStr += xml_string(col, data)
                        rdfStr += rdf_string(col, data)
                    else:
                        raise ValueError("Invalid datatype")
    
                xmlStr += '    </s3m:ms-' + rec.dataid.strip() + '>\n'
                xmlStr += '</s3m:dm-' + rec.dmid.strip() + '>\n'
                                
                # validate the XML data file and enter the appropriate RDF statement as well as an entry in the validation log.
                try:
                    tree = etree.parse(StringIO(xmlStr))  # turn the string into a tree
                    modelSchema.assertValid(tree)  # now validate the tree against the schema 
                    
                    rdfStr += '  <rdfs:Class rdf:about="' + file_id + '">\n'
                    rdfStr += '    <rdf:type rdf:resource="https://www.s3model.com/ns/s3m/s3model/DataInstanceValid"/>\n'
                    rdfStr += '  </rdfs:Class>\n'
                    vlogStr = file_id + ',valid,\n'
                except etree.DocumentInvalid:
                    log = modelSchema.error_log
                    used_lines = []
                    for err in log:
                        if err.line not in used_lines:
                            used_lines.append(err.line)
                            print('\nPlease check the validation log for invalid values.\n')
                            xmlStr = injectEV(xmlStr, err.type, err.message, err.path)
                            rdfStr += '  <rdfs:Class rdf:about="' + file_id + err.path + '">\n'
                            rdfStr += '    <rdfs:comment>' + repr(err.message) + '</rdfs:comment>\n'
                            rdfStr += '  </rdfs:Class>\n'
                    rdfStr += '  <rdfs:Class rdf:about="' + file_id + '">\n'
                    rdfStr += '    <rdf:type rdf:resource="https://www.s3model.com/ns/s3m/s3model/DataInstanceInvalid"/>\n'
                    rdfStr += '  </rdfs:Class>\n'
                    vlogStr = file_id + ',invalid,' + err.message + '\n'
                except etree.LxmlError as e:
                    print('\nPlease check the validation log for errors in parsing the file.\n')
                    rdfStr += '  <rdfs:Class rdf:about="' + file_id + '">\n'
                    rdfStr += '    <rdf:type rdf:resource="https://www.s3model.com/ns/s3m/s3model/DataInstanceError"/>\n'
                    rdfStr += '  </rdfs:Class>\n'
                    vlogStr = file_id + ',error,' + str(e.args) + '\n'
                finally:
                    vlog.log = vlog.log + vlogStr 
                    vlsession.flush()
                    
                rdfStr += '</rdf:RDF>\n'
                
                # add the prolog back to the top
                xmlStr = xmlProlog + xmlStr

                # Persistence Choices               
                if xmldb is not None:
                    if xmldb.dbtype == 'bx': # BasexDB
                        try:
                            connXML.add(file_id + '.xml', xmlStr)
                        except Exception as e:
                            vlog.log = vlog.log + (file_id + ',BaseXDB Error,' + str(e.args) + '\n')
                            vlsession.flush()
                    
                    elif xmldb.dbtype == 'ml': # Marklogic 
                        headers = {"Content-Type": "application/xml", 'user-agent': 'Kunteksto'}
                        url = 'http://' + hostip + ':' + port + '/v1/documents?uri=/' + prj + '/xml/' + file_id 
                        r = requests.put(url, auth=HTTPDigestAuth(user, pw), headers=headers, rec=xmlStr)                                
                        
                    elif xmldb.dbtype == 'fs': # Filesystem
                        with open(os.path.join(xmldb.host.strip(), rec.project.strip(), file_id + '.xml'), 'w') as xmlFile:
                            xmlFile.write(xmlStr)
                    else:
                        print("\nNo XML persistence option for specified.\n")
    
                if rdfdb is not None:                     
                    if rdfdb.dbtype == 'ag': 
                        try:
                            connRDF.addData(rdfStr, rdf_format=RDFFormat.RDFXML, base_uri=None, context=None)
                        except Exception as e:
                            vlog.log = vlog.log + (file_id + ',AllegroDB Error,' + str(e.args) + '\n')
                            vlsession.flush() 
                            
                    elif rdfdb.dbtype == 'ml': 
                        headers = {"Content-Type": "application/xml", 'user-agent': 'Kunteksto'}
                        url = 'http://' + hostip + ':' + port + '/v1/documents?uri=/' + prj + '/rdf/' + file_id 
                        r = requests.put(url, auth=HTTPDigestAuth(user, pw), headers=headers, rec=rdfStr)                                
                            
                    elif rdfdb.dbtype == 'fs': 
                        with open(os.path.join(rdfdb.host.strip(), rec.project.strip(), file_id + '.rdf'), 'w') as rdfFile:
                            rdfFile.write(rdfStr)
                    else:
                        print("\nNo RDF persistence option for specified.\n")

                if jsondb is not None:                                         
                    try:
                        d = xmltodict.parse(xmlStr, xml_attribs=True, process_namespaces=True, namespaces=namespaces)
                        jsonStr = json.dumps(d, indent=4)
                    except Exception as e:
                        vlog.log = vlog.log + (file_id + ',JSON Parse Error,' + str(e.args) + '\n')
                        vlsession.flush()                                            
                                
                    if jsondb.dbtype == 'ml':
                        headers = {"Content-Type": "application/json", 'user-agent': 'Kunteksto'}
                        url = 'http://' + hostip + ':' + port + '/v1/documents?uri=/' + prj + '/json/' + file_id 
                        r = requests.put(url, auth=HTTPDigestAuth(user, pw), headers=headers, rec=jsonStr)
                            
                    elif jsondb.dbtype == 'fs':
                        with open(os.path.join(jsondb.host.strip(), rec.project.strip(), file_id + '.json'), 'w') as jsonFile:
                            jsonFile.write(jsonStr)
                    else:
                        print("\nNo JSON persistence option for specified.\n")
    vlsession.commit()
    return True

def export_model(project):
    """
    Export the XML Schema and RDF graph based on the model.
    """
    session = Session()
    try:
        rec = session.query(Datamodel).filter_by(project=project).first()
    except sqlite3.Error as e:
        print("Failed to find the model for " + project)
        print('\n\n', e)
        exit(1)

    dmlibpath = Path(os.path.join(os.getcwd(), os.pardir, 'dmlib', rec.project.strip()))
    dmlibpath.mkdir(parents=True)

    with open(os.path.join(dmlibpath, 'dm-' + rec.dmid + '.xsd'), 'w') as xsd:
        xsd.write(rec.schema.strip())

    with open(os.path.join(dmlibpath, 'dm-' + rec.dmid + '.rdf'), 'w') as rdf:
        rdf.write(rec.rdf.strip())

    print(rec.project, " was exported to the dmlib subdirectory.\n\n")
    return