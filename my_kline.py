# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 09:43:52 2019

@author: Administrator
"""

from pyecharts import Kline, Line, Bar
from pyecharts import Overlap
import pandas as pd
from pyecharts import configure

configure(global_theme = "roma")

def kline_plot(data, avg_list):
    
# pre data process    
    date = [str(data["date"][i]) for i in range(len(data["date"]))]    # 必须是list，否则叠加失败
    v = []
    for i in range(len(data)):
        temp = [data["open"][i], data["close"][i], data["low"][i], data["high"][i]]
        v.append(temp)
    
    # Kline
    kline = Kline("**价值K线图","a little prediction ")
    kline.add("Value", date, v,
              mark_point=["max"],
              tooltip_tragger = "axis", is_datazoom_show = True, datazoom_range = [0,100],
              tooltip_axispointer_type = 'cross',
              is_legend_show = True, is_more_utils = True, yaxis_min = (min(data["low"])-(max(data["high"])-min(data["low"]))/4))
        
    
    # MA Line
    if len(avg_list) > 0:
        line1 = Line("**价值K线图","a little prediction ")
        for ma in avg_list:
            v_ma = (data['close'].rolling(ma).mean()).apply(lambda vol: vol if vol > 0 else 0)
            line1.add("MA{}".format(ma), date, v_ma, 
                      tooltip_tragger="axis", 
                      tooltip_axispointer_type = 'cross',
                      is_more_utils = True,
                      is_datazoom_show = True, datazoom_range = [0,100],
                      yaxis_min = min(v_ma)-(max(v_ma)-min(v_ma))/4)
    
    # Volume bar
    bar = Bar()
    bar.add("volume", date, data["volume"], tooltip_tragger="axis", is_legend_show = True, is_yaxis_show = False, yaxis_max = 10 * max(data["volume"]))

    # 添加特殊点（波纹状）
#    es = EffectScatter("buy")
#    es.add("",x,y)
    
#    v1 = date[10]
#    v2 = da['high'].iloc[10]
#    es = EffectScatter()
#    es.add("", [v1], [v2])
#    v1 = date[18]
#    v2 = da['high'].iloc[18]
#    es.add( "sell",  [v1],  [v2], symbol="pin",)
#    
#    
#    overlap.add(es)#  需要移动到下面    

    
    
    # overlap fig 
    WIDTH = 1500
    HEIGHT = 800
    overlap = Overlap(width = WIDTH, height = HEIGHT)  
     
    if len(avg_list) > 0:
        overlap.add(line1)    
    overlap.add(kline) 
    overlap.add(bar, yaxis_index = 1, is_add_yaxis = True)
    
    return overlap


if __name__ == "__main__":
#    configure(global_theme = "dark")
    data = pd.read_csv('table_name.csv')    # k 线图数据 
    charts = kline_plot(data, avg_list = [3,7])
    charts.render("value_kline.html")







