"""
analyze.py

Analyze the CSV and create the Datamodel entry as well as a Component entry for each CSV column. 
"""
import sys
import os
import time
import csv
import logging

import sqlite3
import click
from cuid import cuid
from collections import OrderedDict
import iso8601
import configparser
import argparse
from subprocess import run
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker

from .models import db, Session, Datamodel, Component

# turn off logging to stdout
sqla_logger = logging.getLogger('sqlalchemy')
sqla_logger.propagate = False
sqla_logger.addHandler(logging.FileHandler('sqla.log'))

def checkType(h, dataDict):
    """ test each data item from a column. if one is not a type, turn off that type. 
    If the type is an int or a float then the min/max is set as inclusive. Exclusive is never set."""
    dlist = dataDict[h]
    is_integer = False
    is_float = False
    is_date = False
    is_str = False
    maxincval = None
    minincval = None

    for x in dlist:
        try:
            int(x)
            is_integer = True
        except:
            is_integer = False
            break

    for x in dlist:
        try:
            if not is_integer:
                float(x)
                is_float = True
        except:
            is_float = False
            break

    for x in dlist:
        try:
            if not is_integer and not is_float:
                iso8601.parse_date(x)
                is_date = True
        except:
            is_date = False
            break

    for x in dlist:
        try:
            if not is_integer and not is_float and not is_date:
                str(x)
                is_str = True
        except:
            is_str = False
            break

    if is_integer:
        intlist = [int(x) for x in dlist]
        maxincval = max(intlist)
        minincval = min(intlist)
    if is_float:
        flist = [float(x) for x in dlist]
        maxincval = max(flist)
        minincval = min(flist)

    if is_integer:
        dt = "Integer"
    elif is_float:
        dt = "Decimal"  # most of the time it really is a decimal.
    elif is_date:
        dt = "Date"
    else:
        dt = "String"

    return(dt, maxincval, minincval, h)

def process(project, csvInput, delim, level):
    """
    Process the CSV file.
    """
    session = Session()
    # create the initial data for the Datamodel table
    print("\nCreating model data.")
    print("Level: ", level)
    print("Delimiter: ", delim)
    dmID = str(cuid())   # data model
    dataID = str(cuid())   # data cluster

    model = Datamodel(project=project, title='S3M Data Model for ' + project, description='', copyright='Copyright 2018, Data Insights, Inc.', 
                      author='Data Insights, Inc.', definition_url='http://www.some_url.com', dmid=dmID, dataid=dataID)
    try:
        session.add(model)
        session.flush()
    except Exception as err:
        print('\n\nAdding Model Failed:\n\nError: ' + str(err))
        print('\n\n')
        exit(1)


    # create the initial data for the Component table.
    model_pk = model.id
    print("\nCreating component data.\n")
    with open(csvInput) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delim)
        for h in reader.fieldnames:
            mcID = str(cuid())  # model component ID
            adID = str(cuid())   # adapter ID
            label = 'The ' + h.replace('_', ' ') # arbitrairly add a word to show that the label different from the CSV header name
            
            data = Component(model_id=model_pk, header=h, label=label, datatype='String', min_len=None, max_len=None, choices='', regex='', min_incl='', max_incl='', min_excl='', max_excl='',
                             description='', definition_url='', pred_obj='', def_text='', def_num='', units='', mcid=mcID, adid=adID)
            try:
                session.add(data)
                session.flush()
                print('Added ID: ', data.id)
            except Exception as err:
                print('\n\nAdding Component Failed:\n\nError: ' + str(err))
                print('\n\n')
                exit(1)


    if level.lower() == 'full':
        print("\nAnalyzing columns for min/max values and datatype.\n")
        # indepth analysis of columns for datatypes and ranges.
        with open(csvInput) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=delim)
            hdrs = reader.fieldnames
            dataDict = OrderedDict()
            for h in reader.fieldnames:
                dataDict[h] = []

            for row in reader:
                for h in reader.fieldnames:
                    dataDict[h].append(row[h])

        hdrs = dataDict.keys()

            # check for the column types and min/max values, show progress bar
        with click.progressbar(hdrs, label="Checking types and min/max values: ") as bar:
            for h in bar:
                vals = checkType(h, dataDict)

                # edit the database record for the correct column datatype
                try:
                    col = session.query(Component).filter_by(model_id=model_pk).filter_by(header=h).first()
                    print('Column: ', col.header, ' --> ', vals[0])
                    col.datatype = vals[0]
                    col.max_inc = vals[1]
                    col.min_inc = vals[2]
                    session.flush()
                except Exception as err:
                    print('Updating ' + h + ' Failed:\nError: ' + str(err))

    # close out the session
    session.commit()

    print("\n\n Analysis complete.\n\n")
    return 

