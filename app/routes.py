import os
import pandas as pd
from flask import render_template, json, request #, flash, redirect, url_for
from app import app, db
#from app.models import Company, Product
from custom_tweet import construct_tweet_link
import elementary 
from web_content import ibm_query_to_html

import json
import pandas as pd

@app.route('/')
@app.route('/index')
def index():
    # Pull down the company info.

    comp_name = request.args.get('compname')
    product_name = request.args.get('productname')

    # Populate company info.
    #name = Company.query.filter_by(name=comp_name).first()
    df = pd.read_csv('company_info.csv')
    if comp_name:
        row = df[df.comp_name == comp_name]
        name = row.comp_name
        comphandle = row.twitter_handle.values[0][1:]
        tweet_link = construct_tweet_link( comphandle )
        
        name = row.comp_name.values[0]
    else:
        name = 'Select a Company'
        tweet_link = construct_tweet_link( 'custom_link')

    watson_query, watson_description = elementary.mydearwatson(comp_name)
    #print(watson_query.columns)
    table = ibm_query_to_html( watson_query, watson_description)

    print(watson_query.columns)

    ## Only for dev purposes
    return render_template('index.html', comp_name=name, tweet=tweet_link, table=table)    
    #return render_template('index.html', comp_name=name)


@app.route('/test')
def test():
    json_url = os.path.join(app.root_path, "../public/example.json")
    print(json_url)
    dat = json.load(open(json_url))
    return render_template('test.html', data=dat)


@app.route('/data')
def data():
    p = Product.query.get(1)
    return render_template("data.html", product=p.productname)


@app.route('/d3')
def d3():
    # load population data into dataframe
    tsv = os.path.join(app.root_path, "../public/world_population.tsv")
    df = pd.read_csv(tsv, sep='\t')
    df = df.loc[:, ["id", "name", "population"]]
    chart_data = df.to_dict(orient='records')
    chart_data = json.dumps(chart_data, indent=2)
    data = {'chart_data': chart_data}
    return render_template("d3.html", data=data)
