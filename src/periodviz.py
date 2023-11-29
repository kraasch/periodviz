#!/usr/bin/python3

# main source: https://medium.com/@shimo164/lets-plot-your-own-calendar-with-matplotlib-af6265f50831

import datetime
from calendar import monthrange
from datetime import timedelta
import matplotlib
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import pandas as pd
from pandas import Timestamp
import sys
import getopt

# NOTE: the period returns on average all 28 days (says google), but between 23 to 35 days is normal too.
average_days_between_periods = 28 # TODO: calculate the value, instead of just googling.

primary_types   = ['period']
secondary_types = ['moody', 'pain', 'dizziness', 'sadness']
primary_color   = 'red'
secondary_color = 'red'
predict_color   = 'blue'

pred_list = []
fill_list = []
mark_list = []

def import_csv_as_dict(filename, filter_types):
    df = pd.read_csv(filename, skiprows=[0], usecols=[0,1,2], names=['start', 'end', 'type'], sep=',', parse_dates=[0, 1])
    df = df.loc[df['type'].isin(filter_types)] # only keep allowed types.
    dictionary = df.T.to_dict()
    return dictionary

def days_between(start, end):
    delta = end - start
    all_days = []
    for i in range(delta.days + 1):
        day = start + timedelta(days=i)
        all_days.append(day)
    return all_days

def spans_to_dates(spans, target_list, target_year):
    for span in spans:
        if span['start'].year == target_year or span['end'].year == target_year:
            days = days_between(span['start'], span['end'])
            for d in days:
                day_in_month = (d.month, d.day)
                target_list.append(day_in_month)

def label_month(year, month, ax, i, j, cl="black"):
    months = [ "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month_label = f"{months[month-1]} {year}"
    ax.text(i, j, month_label, color=cl, va="center")

def label_weekday(ax, i, j, cl="black"):
    x_offset_rate = 1
    for weekday in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
        ax.text(i, j, weekday, ha="center", va="center", color=cl)
        i += x_offset_rate

def label_day(ax, day, i, j, cl="black"):
    ax.text(i, j, int(day), ha="center", va="center", color=cl)

def fill_box(ax, i, j, color):
    ax.add_patch(
        patches.Rectangle(
            (i - 0.5, j - 0.5),
            1,
            1,
            edgecolor="black",
            facecolor=color,
            alpha=0.1,
            fill=True,
        )
    )

def check_fill_day(year, month, day, weekday):
    if (month, day) in pred_list:
        return True
    if (month, day) in fill_list:
        return True
    return False

def check_fill_color_day(year, month, day, weekday):
    if (month, day) in pred_list:
        return predict_color
    if (month, day) in fill_list:
        return primary_color
    return "white"

def check_font_color_day(year, month, day, weekday):
    ### some code example.
    #if weekday == 6:  # Sunday
    #    return "green"
    if (month, day) in mark_list:
        return secondary_color
    return "black"

def month_calendar(ax, year, month, fill):
    date = datetime.datetime(year, month, 1)
    weekday, num_days = monthrange(year, month)
    # adjust by 0.5 to set text at the ceter of grid square
    x_start = 1 - 0.5
    y_start = 5 + 0.5
    x_offset_rate = 1
    y_offset = -1
    label_month(year, month, ax, x_start, y_start + 2)
    label_weekday(ax, x_start, y_start + 1)
    j = y_start
    for day in range(1, num_days + 1):
        i = x_start + weekday * x_offset_rate
        font_color = check_font_color_day(year, month, day, weekday)
        fill_color = check_fill_color_day(year, month, day, weekday)
        if fill and check_fill_day(year, month, day, weekday):
            fill_box(ax, i, j, fill_color)
        label_day(ax, day, i, j, font_color)
        weekday = (weekday + 1) % 7
        if weekday == 0:
            j += y_offset

def format_ax(ax, grid=True):
    ax.axis([0, 7, 0, 7])
    ax.axis("off")
    if grid:
        ax.axis("on")
        ax.grid(grid)
        for tick in ax.xaxis.get_major_ticks():
            tick.tick1line.set_visible(False)
            tick.tick2line.set_visible(False)
            tick.label1.set_visible(False)
            tick.label2.set_visible(False)
        for tick in ax.yaxis.get_major_ticks():
            tick.tick1line.set_visible(False)
            tick.tick2line.set_visible(False)
            tick.label1.set_visible(False)
            tick.label2.set_visible(False)

def anual_calender(year, grid, fill):
    nrow = 3
    ncol = 4
    figsize=(10,6)
    fig, axs = plt.subplots(figsize=figsize, nrows=nrow, ncols=ncol)
    month = 1
    for ax in axs.reshape(-1):
        format_ax(ax, grid=grid)
        month_calendar(ax, year, month, fill)
        month += 1

def make_calendar(year, output_file, grid, fill):
    fig = plt.figure()
    anual_calender(year, grid, fill)
    plt.savefig(output_file)

def predict(last_3_periods, target_year):
    last_start = last_3_periods[-1]['start']
    last_end   = last_3_periods[-1]['end']
    next_start = last_start + timedelta(days=average_days_between_periods)
    next_end   = last_end   + timedelta(days=average_days_between_periods)
    return {0: {'start': next_start, 'end': next_end, 'type': 'prediction'}}

def my_args(argv):
    # variables with example values.
    # example call: python3 periodviz.py -i 'data.csv' -o 'export/period.png' -t 2023
    target_year = 2023
    input_file = 'data.csv'
    output_file = 'export/period.png'

    # parase the CLI arguments.
    opts, args = getopt.getopt(argv, 'hi:o:t:', ['ifile=','ofile=','tyear'])
    for opt, arg in opts:
        if opt == '-h':
            print ('periodviz.py -i <input_file> -o <output_file> -t <target_year>')
            sys.exit()
        elif opt in ('-t', '--tyear'):
            target_year = int(arg)
        elif opt in ('-i', '--ifile'):
            input_file = arg
        elif opt in ('-o', '--ofile'):
            output_file = arg

    # open files.
    periods = import_csv_as_dict(input_file, primary_types)
    aches   = import_csv_as_dict(input_file, secondary_types)

    # add predictions.
    last_3_periods = list(periods.values())[-3:]
    predictions = predict(last_3_periods, target_year)

    # extract dates.
    spans_to_dates(predictions.values(), pred_list, target_year)
    spans_to_dates(periods.values(),     fill_list, target_year)
    spans_to_dates(aches.values(),       mark_list, target_year)

    # make a calendar.
    make_calendar(target_year, output_file, True, True)

if __name__ == '__main__':
    my_args(sys.argv[1:])

