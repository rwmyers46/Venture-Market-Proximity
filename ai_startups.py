#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 16:11:11 2019

@author: rwmyers
"""

from flask import Flask, render_template, request
import pandas as pd

from bokeh.plotting import figure, curdoc
from bokeh.embed import components
from bokeh.models import HoverTool, CustomJS, ColumnDataSource, Slider, Legend
from bokeh.layouts import column
from bokeh.palettes import all_palettes
from bokeh.themes import built_in_themes

app = Flask(__name__)  # create instance of Flask class

embedding = pd.read_csv('./data/bokeh_df.csv')
    
def create_hover_tool():
    hover_tsne = """
    <div style="margin: 10">
        <div style="margin: 0 auto; width:300px;">
            <span style="font-size: 12px; font-weight: bold;">Company:</span>
            <span style="font-size: 12px">@name</span>
            <span style="font-size: 12px; font-weight: bold;">Categories:</span>
            <span style="font-size: 12px">@category</span>
        </div>
    </div>
    """
    return HoverTool(tooltips=hover_tsne)


def create_chart(data, hover_tsne):
    """Creates a bar chart plot with the exact styling for the centcom
       dashboard. Pass in data as a dictionary, desired plot title,
       name of x axis, y axis and the hover tool HTML.
    """
        
    source = ColumnDataSource(data)
        
    tools_tsne = [hover_tsne, 'pan', 'wheel_zoom', 'reset']
    
    plot_tsne = figure(plot_width=900, plot_height=900, tools=tools_tsne, title='AI / ML Venture Market Proximity by Topic Distribution')
    
    plot_tsne.circle('x', 'y', size='size', fill_color='colors', 
                     alpha='alpha', line_alpha=0, line_width=0.01, source=source, name="df", legend = 'location')
    
    plot_tsne.legend.location = "top_left"
    plot_tsne.legend.orientation = "horizontal"
    #plot_tsne.legend.click_policy="hide"
    return plot_tsne

@app.route('/')  # the site to route to, index/main in this case
def index():
    data=dict(
        x = embedding.x,
        y = embedding.y,
        colors = [all_palettes['Inferno'][6][i] for i in embedding.hue],
        name = embedding.name,
        category = embedding.cat,
        location = embedding.location,
        alpha = [0.9] * embedding.shape[0],
        size = [7] * embedding.shape[0]
    )
    curdoc().theme = 'dark_minimal'
    hover_tsne = create_hover_tool()
    plot = create_chart(data, hover_tsne)
    script, div = components(plot)

    return render_template("app_index.html", the_div=div, the_script=script)

if __name__ == '__main__':
    app.run(debug=False)