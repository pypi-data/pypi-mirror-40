# -*- coding: utf-8 -*-
from __future__ import division
from functools import partial
from .pycm_param import *
from .pycm_util import class_filter, rounder
import webbrowser


def html_init(name):
    '''
    This function return report  file first lines
    :param name: name of file
    :type name : str
    :return: html_init as str
    '''
    result = ""
    result += "<html>\n"
    result += "<head>\n"
    result += "<title>" + str(name) + "</title>\n"
    result += "</head>\n"
    result += "<body>\n"
    result += '<h1 style="border-bottom:1px solid ' \
              'black;text-align:center;">PyCM Report</h1>'
    return result


def color_check(color):
    '''
    This function check input color fotmat
    :param color: input color
    :type color : tuple
    :return: color as list
    '''
    if isinstance(color, tuple):
        if all(map(lambda x: isinstance(x, int), color)):
            if all(map(lambda x: x < 256, color)):
                return list(color)
    return [0, 0, 0]


def html_table_color(row, item, color=(0, 0, 0)):
    '''
    This function return background color of each cell of table
    :param row: row dictionary
    :type row : dict
    :param item: cell number
    :type item : int
    :param color : input color
    :type color : tuple
    :return: background color as list [R,G,B]
    '''
    result = [0, 0, 0]
    color_list = color_check(color)
    max_color = max(color_list)
    back_color_index = 255 - int((item / (sum(list(row.values())) + 1)) * 255)
    for i in range(3):
        result[i] = back_color_index - (max_color - color[i])
        if result[i] < 0:
            result[i] = 0
    return result


def html_table(classes, table, rgb_color):
    '''
    This function return report file confusion matrix
    :param classes: matrix classes
    :type classes: list
    :param table: matrix
    :type table : dict
    :param rgb_color : input color
    :type rgb_color : tuple
    :return: html_table as str
    '''
    result = ""
    result += "<h2>Confusion Matrix : </h2>\n"
    result += '<table>\n'
    result += '<tr  align="center">' + "\n"
    result += '<td>Actual</td>\n'
    result += '<td>Predict\n'
    table_size = str((len(classes) + 1) * 7) + "em"
    result += '<table style="border:1px solid black;border-collapse: collapse;height:{0};width:{0};">\n'\
        .format(table_size)
    classes.sort()
    result += '<tr align="center">\n<td></td>\n'
    part_2 = ""
    for i in classes:
        class_name = str(i)
        if len(class_name) > 6:
            class_name = class_name[:4] + "..."
        result += '<td style="border:1px solid ' \
                  'black;padding:10px;height:7em;width:7em;">' + \
            class_name + '</td>\n'
        part_2 += '<tr align="center">\n'
        part_2 += '<td style="border:1px solid ' \
                  'black;padding:10px;height:7em;width:7em;">' + \
            class_name + '</td>\n'
        for j in classes:
            item = table[i][j]
            color = "black;"
            back_color = html_table_color(table[i], item, rgb_color)
            if min(back_color) < 128:
                color = "white"
            part_2 += '<td style="background-color:	rgb({0},{1},{2});color:{3};padding:10px;height:7em;width:7em;">'.format(
                str(back_color[0]), str(back_color[1]), str(back_color[2]), color) + str(item) + '</td>\n'
        part_2 += "</tr>\n"
    result += '</tr>\n'
    part_2 += "</table>\n</td>\n</tr>\n</table>\n"
    result += part_2
    return result


def html_overall_stat(overall_stat, digit=5, overall_param=None):
    '''
    This function return report file overall stat
    :param overall_stat: overall stat
    :type overall_stat : dict
    :param digit: scale (the number of digits to the right of the decimal point in a number.)
    :type digit : int
    :param overall_param : Overall parameters list for print, Example : ["Kappa","Scott PI]
    :type overall_param : list
    :return: html_overall_stat as str
    '''
    result = ""
    result += "<h2>Overall Statistics : </h2>\n"
    result += '<table style="border:1px solid black;border-collapse: collapse;">\n'
    overall_stat_keys = sorted(overall_stat.keys())
    if isinstance(overall_param, list):
        if set(overall_param) <= set(overall_stat_keys):
            overall_stat_keys = sorted(overall_param)
    if len(overall_stat_keys) < 1:
        return ""
    background_color = None
    for i in overall_stat_keys:
        result += '<tr align="center">\n'
        result += '<td style="border:1px solid black;padding:4px;text-align:left;"><a href="' + \
            DOCUMENT_ADR + PARAMS_LINK[i] + '" style="text-decoration:None;">' + str(i) + '</a></td>\n'
        if i.find("SOA") != -1:
            background_color = BENCHMARK_COLOR[overall_stat[i]]
            result += '<td style="border:1px solid black;padding:4px;background-color:{};">'.format(
                background_color)
        else:
            result += '<td style="border:1px solid black;padding:4px;">'
        result += rounder(overall_stat[i], digit) + '</td>\n'
        result += "</tr>\n"
    result += "</table>\n"
    return result


def html_class_stat(classes, class_stat, digit=5, class_param=None):
    '''
    This function return report file class_stat
    :param classes: matrix classes
    :type classes: list
    :param class_stat: class stat
    :type class_stat:dict
    :param digit: scale (the number of digits to the right of the decimal point in a number.)
    :type digit : int
    :param class_param : Class parameters list for print, Example : ["TPR","TNR","AUC"]
    :type class_param : list
    :return: html_class_stat as str
    '''
    result = ""
    result += "<h2>Class Statistics : </h2>\n"
    result += '<table style="border:1px solid black;border-collapse: collapse;">\n'
    result += '<tr align="center">\n<td>Class</td>\n'
    for i in classes:
        result += '<td style="border:1px solid black;padding:4px;border-collapse: collapse;">' + \
            str(i) + '</td>\n'
    result += '<td>Description</td>\n'
    result += '</tr>\n'
    class_stat_keys = sorted(class_stat.keys())
    if isinstance(class_param, list):
        if set(class_param) <= set(class_stat_keys):
            class_stat_keys = class_param
    classes.sort()
    if len(classes) < 1 or len(class_stat_keys) < 1:
        return ""
    for i in class_stat_keys:
        result += '<tr align="center" style="border:1px solid black;border-collapse: collapse;">\n'
        result += '<td style="border:1px solid black;padding:4px;border-collapse: collapse;"><a href="' + \
                  DOCUMENT_ADR + PARAMS_LINK[i] + '" style="text-decoration:None;">' + str(i) + '</a></td>\n'
        for j in classes:
            if i in ["PLRI", "DPI", "AUCI"]:
                background_color = BENCHMARK_COLOR[class_stat[i][j]]
                result += '<td style="border:1px solid black;padding:4px;border-collapse: collapse;background-color:{};">'.format(
                    background_color)
            else:
                result += '<td style="border:1px solid black;padding:4px;border-collapse: collapse;">'
            result += rounder(class_stat[i][j], digit) + '</td>\n'
        result += '<td style="border:1px solid black;padding:4px;border-collapse: collapse;text-align:left;">' + \
                  PARAMS_DESCRIPTION[i].capitalize() + '</td>\n'
        result += "</tr>\n"
    result += "</table>\n"
    return result


def html_end(version):
    '''
    This function return report file end lines
    :param version: pycm version
    :type version:str
    :return: html_end as str
    '''
    result = "</body>\n"
    result += '<p style="text-align:center;border-top:1px solid black;">Generated By ' \
        '<a href="http://www.pycm.ir" ' \
              'style="text-decoration:none;color:red;">PyCM</a> Version ' + version + '</p>\n'
    result += "</html>"
    return result


def html_maker(
    html_file,
    name,
    classes,
    table,
    overall_stat,
    class_stat,
    digit=5,
    overall_param=None,
    class_param=None,
    class_name=None,
    color=(
        0,
        0,
        0)):
    '''
    This function create html report
    :param html_file : file object of html
    :type html_file: file object
    :param name: file name
    :type name : str
    :param classes: matrix classes
    :type classes: list
    :param table: matrix
    :type table: dict
    :param overall_stat: overall stat
    :type overall_stat: dict
    :param class_stat: class stat
    :type class_stat: dict
    :param digit: scale (the number of digits to the right of the decimal point in a number.)
    :type digit : int
    :param overall_param : overall parameters list for print, Example : ["Kappa","Scott PI]
    :type overall_param : list
    :param class_param : class parameters list for print, Example : ["TPR","TNR","AUC"]
    :type class_param : list
    :param class_name : class name (sub set of classes), Example :[1,2,3]
    :type class_name : list
    :param color : input color
    :type color : tuple
    :return: None
    '''
    html_file.write(html_init(name))
    html_file.write(html_table(classes, table, color))
    html_file.write(html_overall_stat(overall_stat, digit, overall_param))
    class_stat_classes = class_filter(classes, class_name)
    html_file.write(
        html_class_stat(
            class_stat_classes,
            class_stat,
            digit,
            class_param))
    html_file.write(html_end(VERSION))


def pycm_help():
    '''
    This function print pycm details
    :return: None
    '''
    print(OVERVIEW)
    print("Repo : https://github.com/sepandhaghighi/pycm")
    print("Webpage : http://www.pycm.ir")


def table_print(classes, table):
    '''
    This function print confusion matrix
    :param classes: classes list
    :type classes:list
    :param table: table
    :type table:dict
    :return: printable table as str
    '''
    classes_len = len(classes)
    table_list = []
    for key in classes:
        table_list.extend(list(table[key].values()))
    table_list.extend(classes)
    table_max_length = max(map(len, map(str, table_list)))
    shift = "%-" + str(4 + table_max_length) + "s"
    result = "Predict" + 10 * " " + shift * \
        classes_len % tuple(map(str, classes)) + "\n"
    result = result + "Actual\n"
    classes.sort()
    for key in classes:
        row = [table[key][i] for i in classes]
        result += str(key) + " " * (17 - len(str(key))) + \
            shift * classes_len % tuple(map(str, row)) + "\n\n"
    return result


def csv_print(classes, class_stat, digit=5, class_param=None):
    '''
    This function return csv file data
    :param classes: classes list
    :type classes:list
    :param class_stat: statistic result for each class
    :type class_stat:dict
    :param digit: scale (the number of digits to the right of the decimal point in a number.)
    :type digit : int
    :param class_param : class parameters list for print, Example : ["TPR","TNR","AUC"]
    :type class_param : list
    :return: csv file data as str
    '''
    result = "Class"
    classes.sort()
    for item in classes:
        result += ',"' + str(item) + '"'
    result += "\n"
    class_stat_keys = sorted(class_stat.keys())
    if isinstance(class_param, list):
        if set(class_param) <= set(class_stat_keys):
            class_stat_keys = class_param
    if len(class_stat_keys) < 1 or len(classes) < 1:
        return ""
    for key in class_stat_keys:
        row = [rounder(class_stat[key][i], digit) for i in classes]
        result += key + "," + ",".join(row)
        result += "\n"
    return result


def stat_print(
        classes,
        class_stat,
        overall_stat,
        digit=5,
        overall_param=None,
        class_param=None):
    '''
    This function return statistics
    :param classes: classes list
    :type classes:list
    :param class_stat: statistic result for each class
    :type class_stat:dict
    :param overall_stat : overall statistic result
    :type overall_stat:dict
    :param digit: scale (the number of digits to the right of the decimal point in a number.)
    :type digit : int
    :param overall_param : overall parameters list for print, Example : ["Kappa","Scott PI]
    :type overall_param : list
    :param class_param : class parameters list for print, Example : ["TPR","TNR","AUC"]
    :type class_param : list
    :return: printable result as str
    '''
    shift = max(map(len, PARAMS_DESCRIPTION.values())) + 5
    classes_len = len(classes)
    overall_stat_keys = sorted(overall_stat.keys())
    result = ""
    if isinstance(overall_param, list):
        if set(overall_param) <= set(overall_stat_keys):
            overall_stat_keys = sorted(overall_param)
    if len(overall_stat_keys) > 0:
        result = "Overall Statistics : " + "\n\n"
        for key in overall_stat_keys:
            result += key + " " * (shift - len(key) + 7) + \
                rounder(overall_stat[key], digit) + "\n"
    class_stat_keys = sorted(class_stat.keys())
    if isinstance(class_param, list):
        if set(class_param) <= set(class_stat_keys):
            class_stat_keys = sorted(class_param)
    classes.sort()
    if len(class_stat_keys) > 0 and len(classes) > 0:
        result += "\nClass Statistics :\n\n"
        result += "Classes" + shift * " " + "%-24s" * \
            classes_len % tuple(map(str, classes)) + "\n"
        rounder_map = partial(rounder, digit=digit)
        for key in class_stat_keys:
            row = [class_stat[key][i] for i in classes]
            result += key + "(" + PARAMS_DESCRIPTION[key].capitalize() + ")" + " " * (
                shift - len(key) - len(PARAMS_DESCRIPTION[key]) + 5) + "%-24s" * classes_len % tuple(
                map(rounder_map, row)) + "\n"
    return result


def online_help(param=None):
    '''
    This function open online document
    :param param: input parameter
    :type param : int or str
    :return: None
    '''
    try:
        PARAMS_LINK_KEYS = sorted(PARAMS_LINK.keys())
        if param in PARAMS_LINK_KEYS:
            webbrowser.open_new_tab(DOCUMENT_ADR + PARAMS_LINK[param])
        elif param in range(1, len(PARAMS_LINK_KEYS) + 1):
            webbrowser.open_new_tab(
                DOCUMENT_ADR + PARAMS_LINK[PARAMS_LINK_KEYS[param - 1]])
        else:
            print("Please choose one parameter : \n")
            print('Example : online_help("J") or online_help(2)\n')
            for index, item in enumerate(PARAMS_LINK_KEYS):
                print(str(index + 1) + "-" + item)
    except Exception:
        print("Error in online help")
