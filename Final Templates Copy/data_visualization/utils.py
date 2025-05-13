import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from flask import Flask, render_template
import io
import base64
import seaborn as sns
import random
import time
from math import pi
from bokeh.plotting import figure, ColumnDataSource
from bokeh.embed import components
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.transform import  cumsum, factor_cmap
from bokeh.palettes import Greens3,GnBu3, Bokeh3
import sqlite3



app = Flask(__name__)

def Show_data_file(excel_file_path, sheet_name):
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
    return df

def extract_sheet_names(excel_file_path):
    try:
        xls = pd.ExcelFile(excel_file_path)
        sheet_names = xls.sheet_names
        return sheet_names
    except Exception as e:
        return render_template("error-message.html" , error = e)
def auto_selected_sheet_name(path):
    xls = pd.ExcelFile(path)
    sheet_names = xls.sheet_names
    auto_selected_sheet = sheet_names[0]
    return auto_selected_sheet

def extract_column_names(excel_file_path, sheet_name):
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
    column_names = df.columns.tolist()
    return column_names
#check variable are array 
def is_array(variable):
    variable = variable
    return isinstance(variable, list)
def arrayintostring(xyz_array):
    my_string = ",".join(xyz_array)
    return my_string
def stringintoarray(xyz_string):
    my_list = xyz_string.split(",")
    return my_list
def style_array_to_string(style_plot):
    position_label, Title_of_label, legend_title_size, legend_title_weight, legend_Title_color, legend_text_color, legend_opacity, legend_box_style, legend_box_size, face_color_legend, edge_color_legend, legend_line_style, legend_line_width, layout_axis_spines,Plot_bg_color, layout_theme_style, layout_xtick_color, layout_ytick_color, layout_xlabel_title, layout_xlabel_color, layout_xlabel_background_color, layout_xlabel_border_color, layout_xlabel_box_style, layout_xlabel_Box_Style_pad, layout_ylabel_title, layout_ylabel_color, layout_ylabel_background_color, layout_ylabel_border_color, layout_ylabel_box_style, layout_ylabel_Box_Style_pad, layout_plot_title, layout_title_color, layout_title_background_color, layout_title_border_color, layout_title_box_style, layout_title_Box_Style_pad, marker_color, marker_size,marker_line_width, marker_categorization, marker_palette, marker_alpha, marker_edge_colors= map(str, style_plot)
    return position_label, Title_of_label, legend_title_size, legend_title_weight, legend_Title_color, legend_text_color, legend_opacity, legend_box_style, legend_box_size, face_color_legend, edge_color_legend, legend_line_style, legend_line_width, layout_axis_spines,Plot_bg_color, layout_theme_style, layout_xtick_color, layout_ytick_color, layout_xlabel_title, layout_xlabel_color, layout_xlabel_background_color, layout_xlabel_border_color, layout_xlabel_box_style, layout_xlabel_Box_Style_pad, layout_ylabel_title, layout_ylabel_color, layout_ylabel_background_color, layout_ylabel_border_color, layout_ylabel_box_style, layout_ylabel_Box_Style_pad, layout_plot_title, layout_title_color, layout_title_background_color, layout_title_border_color, layout_title_box_style, layout_title_Box_Style_pad, marker_color, marker_size,marker_line_width, marker_categorization, marker_palette, marker_alpha, marker_edge_colors
def checkcolumnsindataset(path,sheet,x,y,z):
    df = pd.read_excel(path, sheet)
    missing_columns = [col for col in x + y + z if col not in df.columns]
    if missing_columns:
        error = f"The following columns are missing in the DataFrame: {', '.join(missing_columns)}"
        return error
    return ""

def replace_dataset_path_auto_sheetname(data):
    df = pd.DataFrame(data)
    unique_number = int(time.time() * 1000)
    output_file = f"uploads/{unique_number}_replace_dataset.xlsx"
    df.to_excel(output_file, index=False)
    auto_selected_sheet = auto_selected_sheet_name(output_file)
    columns_replace_dataset = extract_column_names(output_file, auto_selected_sheet)
    return output_file, auto_selected_sheet, columns_replace_dataset

def convert_to_integer_or_string(value):
    if value is not None:
        if str(value).isdigit():
            value_as_integer = int(value)
            return value_as_integer
        else:
            value_as_string = str(value)
            return value_as_string
    else:
        return None
def check_int_None(value , n):
    if value is None or value == "None":
        return n
    elif isinstance(value, str) and value.isdigit():
        value_as_integer = int(value)
        return value_as_integer
    elif isinstance(value, str):
        return n
    else:
        return value  # You might want to specify a default value or handle other cases
def check_int_None_alpha_only(value , n):
    if n > 100:
        n = 100
    ans = n/100
    if value is None or value == "None":
        return ans
    elif isinstance(value, str) and value.isdigit():
        value_as_integer = int(value)
        value_as_integer = value_as_integer/100
        return value_as_integer
    elif isinstance(value, str):
        return ans
    else:
        return value 
value = "none"
def check_str_None(value , default_text):
    if value is None or value == "None" or value == "none":
        return default_text
    else:
        return value
def check_none_TandF(value):
    if value is None or value == "None" or value == "none":
        return False
    else: 
        return True
def remove_str_columns_from_Dataframe(data):
    str_columns = data.select_dtypes(include='object').columns
    # Drop columns with string data type
    data_numeric = data.drop(columns=str_columns)
    return data_numeric
def process_html_data(Convert_to_Excel):
    # Replace this with your actual data processing logic
    processed_data = f"Processed HTML data: {Convert_to_Excel}"
    return processed_data
#plot Function Start
def themesseaborn(sns):
    sns.set_theme(style=style_plots["layout_theme_style"], rc={"axes.facecolor": style_plots["layout_axis_spines"], "xtick.color": style_plots["layout_xtick_color"], "ytick.color": style_plots["layout_ytick_color"], 'figure.facecolor': style_plots["Plot_bg_color"]})
def labels(plt):
    legend = plt.legend(loc=style_plots["position_label"])
    legend.get_frame().set_facecolor(style_plots["face_color_legend"])# Set the background color of the legend
    legend.get_frame().set_alpha(style_plots["legend_opacity"])
    legend.get_frame().set_edgecolor(style_plots["edge_color_legend"])   # Set the edge color of the legend
    legend.set_title(style_plots["Title_of_label"], prop={'size': "medium", 'weight': style_plots["legend_title_weight"]})
    legend.get_title().set_color(style_plots["legend_Title_color"])
    legend.get_frame().set_linestyle(style_plots["legend_line_style"])
    legend.get_frame().set_linewidth(style_plots["legend_line_width"])
    # Set the text color of the legend
    for text in legend.get_texts():
        text.set_color(style_plots["legend_text_color"])  # Set the text color to green
    legend.get_frame().set_boxstyle(style_plots["legend_box_style"], pad=style_plots["legend_box_size"])

    
    xlabel = plt.xlabel(style_plots["layout_xlabel_title"], color=style_plots["layout_xlabel_color"])
    ylabel = plt.ylabel(style_plots["layout_ylabel_title"], color=style_plots["layout_ylabel_color"])

# Adding a title with custom color and background color
    title = plt.title(style_plots["layout_plot_title"], color=style_plots["layout_title_color"])

# Set background color for xlabel
    xlabel.set_bbox(dict(facecolor=style_plots["layout_title_background_color"], edgecolor=style_plots["layout_xlabel_border_color"], boxstyle= style_plots["layout_xlabel_box_style"], pad=style_plots["layout_xlabel_Box_Style_pad"]))

# Set background color for ylabel
    ylabel.set_bbox(dict(facecolor=style_plots["layout_ylabel_background_color"], edgecolor=style_plots["layout_ylabel_border_color"], boxstyle= style_plots["layout_ylabel_box_style"], pad=style_plots["layout_ylabel_Box_Style_pad"]))

# Set background color for title
    title.set_bbox(dict(facecolor=style_plots["layout_title_background_color"], edgecolor=style_plots["layout_title_border_color"], boxstyle= style_plots["layout_title_box_style"], pad=style_plots["layout_title_Box_Style_pad"]))    

def underscore_legend(legend):
    legend.set_title(style_plots["Title_of_label"], prop={'size': style_plots["legend_title_size"], 'weight': style_plots["legend_title_weight"]})  # Set legend title with custom properties
    legend.set_bbox_to_anchor([1, 0.4])  # Adjust legend position
# Customize legend text style
    legend_texts = legend.texts
    for text in legend_texts:
        text.set_fontsize(12)  # Set font size
        text.set_color(style_plots["legend_text_color"])  # Set text color
        
def underscore_legend_BG(legend):
    #legend.set_bbox_to_anchor((.2, 1.0))
    legend.get_frame().set_facecolor(style_plots["face_color_legend"])# Set the background color of the legend
    legend.get_frame().set_alpha(style_plots["legend_opacity"])
    legend.get_frame().set_edgecolor(style_plots["edge_color_legend"])   # Set the edge color of the legend
    legend.set_title(style_plots["Title_of_label"], prop={'size': style_plots["legend_title_size"], 'weight': style_plots["legend_title_weight"]})
    legend.get_title().set_color(style_plots["legend_Title_color"])
    legend.get_frame().set_linestyle(style_plots["legend_line_style"])
    
def underscore_axis(plt):
    
    xlabel = plt.xlabel(style_plots["layout_xlabel_title"], color=style_plots["layout_xlabel_color"])
    ylabel = plt.ylabel(style_plots["layout_ylabel_title"], color=style_plots["layout_ylabel_color"])

# Adding a title with custom color and background color
    title = plt.title(style_plots["layout_plot_title"], color=style_plots["layout_title_color"])

# Set background color for xlabel
    xlabel.set_bbox(dict(facecolor=style_plots["layout_xlabel_background_color"], edgecolor = style_plots["layout_xlabel_border_color"], boxstyle = style_plots["layout_xlabel_box_style"],pad=style_plots["layout_xlabel_Box_Style_pad"]))

# Set background color for ylabel
    ylabel.set_bbox(dict(facecolor=style_plots["layout_ylabel_background_color"], edgecolor = style_plots["layout_ylabel_border_color"], boxstyle = style_plots["layout_ylabel_box_style"],pad=style_plots["layout_ylabel_Box_Style_pad"]))

# Set background color for title
    title.set_bbox(dict(facecolor=style_plots["layout_title_background_color"], edgecolor = style_plots["layout_title_border_color"], boxstyle= style_plots["layout_title_box_style"],pad= style_plots["layout_title_Box_Style_pad"]))    
#plot Function End
def set_style_plots(style_plots,style_plot):
    style_plot = [value if value != "" else None for value in style_plot]
    position_label, Title_of_label, legend_title_size, legend_title_weight, legend_Title_color, legend_text_color, legend_opacity, legend_box_style, legend_box_size, face_color_legend, edge_color_legend, legend_line_style, legend_line_width, layout_axis_spines,Plot_bg_color, layout_theme_style, layout_xtick_color, layout_ytick_color, layout_xlabel_title, layout_xlabel_color, layout_xlabel_background_color, layout_xlabel_border_color, layout_xlabel_box_style, layout_xlabel_Box_Style_pad, layout_ylabel_title, layout_ylabel_color, layout_ylabel_background_color, layout_ylabel_border_color, layout_ylabel_box_style, layout_ylabel_Box_Style_pad, layout_plot_title, layout_title_color, layout_title_background_color, layout_title_border_color, layout_title_box_style, layout_title_Box_Style_pad, marker_color, marker_size,marker_line_width, marker_categorization, marker_palette, marker_alpha, marker_edge_colors = style_array_to_string(style_plot)
    style_plots["position_label"] = position_label
    style_plots["Title_of_label"] = check_str_None(Title_of_label, None)
    style_plots["legend_title_size"] = check_int_None(legend_title_size, 10)
    style_plots["legend_title_weight"] = convert_to_integer_or_string(legend_title_weight)
    style_plots["legend_Title_color"] = check_str_None(legend_Title_color,"black")
    #NOT tesing apply legend(plt) text color testing 
    style_plots["legend_text_color"] = check_str_None(legend_text_color, "black")
    style_plots["legend_opacity"] = check_int_None_alpha_only(legend_opacity , 100)
    style_plots["legend_box_style"] = legend_box_style
    style_plots["legend_box_size"] = check_int_None(legend_box_size, 1)
    style_plots["face_color_legend"] = face_color_legend
    style_plots["edge_color_legend"] = edge_color_legend
    style_plots["legend_line_style"] = legend_line_style
    style_plots["legend_line_width"] = check_int_None(legend_line_width, 1)
    #layout_axis_spines not found 
    style_plots["layout_axis_spines"] = layout_axis_spines
    style_plots["Plot_bg_color"] = check_str_None(Plot_bg_color,"white")
    style_plots["layout_theme_style"] = layout_theme_style
    style_plots["layout_xtick_color"] = check_str_None(layout_xtick_color , "black")
    style_plots["layout_ytick_color"] = check_str_None(layout_ytick_color, "black")
    style_plots["layout_xlabel_title"] = check_str_None(layout_xlabel_title, None)
    style_plots["layout_xlabel_color"] = check_str_None(layout_xlabel_color, "black")
    style_plots["layout_xlabel_background_color"] = layout_xlabel_background_color
    style_plots["layout_xlabel_border_color"] = layout_xlabel_border_color
    style_plots["layout_xlabel_box_style"] = layout_xlabel_box_style
    style_plots["layout_xlabel_Box_Style_pad"] = check_int_None(layout_xlabel_Box_Style_pad, 1)
    style_plots["layout_ylabel_title"] = check_str_None(layout_ylabel_title, None)
    style_plots["layout_ylabel_color"] = check_str_None(layout_ylabel_color, "black")
    style_plots["layout_ylabel_background_color"] = layout_ylabel_background_color
    style_plots["layout_ylabel_border_color"] = layout_ylabel_border_color
    style_plots["layout_ylabel_box_style"] = layout_ylabel_box_style
    style_plots["layout_ylabel_Box_Style_pad"] = check_int_None(layout_ylabel_Box_Style_pad, 1)
    style_plots["layout_plot_title"] = check_str_None(layout_plot_title, None)
    style_plots["layout_title_color"] = check_str_None(layout_title_color, "black")
    style_plots["layout_title_background_color"] = layout_title_background_color
    style_plots["layout_title_border_color"] = layout_title_border_color
    style_plots["layout_title_box_style"] = layout_title_box_style
    style_plots["layout_title_Box_Style_pad"] = check_int_None(layout_title_Box_Style_pad, 1)

    style_plots["marker_color"] = marker_color
    style_plots["marker_size"] = check_int_None(marker_size, 40)
    style_plots["marker_line_width"] = check_int_None(marker_line_width, 2)
    style_plots["marker_categorization"] = check_str_None(marker_categorization , None)
    style_plots["marker_palette"] = check_str_None(marker_palette, "Purples")
    style_plots["marker_alpha"] = check_int_None_alpha_only(marker_alpha , 100)
    style_plots["marker_edge_colors"] = marker_edge_colors
    style_plots["Legend_true_false_check"] = check_none_TandF(style_plots["marker_categorization"])
    


    
    return
def plots_function(path, sheet,x,y,z):
    path = path
    sheet = sheet
    error = ""
    x_axis, y_axis, z_axis = x, y, z
    selected_columns = x_axis+y_axis+z_axis
    df = pd.read_excel(path, sheet)
    # Check if all selected columns exist in the DataFrame
    missing_columns = [col for col in x+y+z if col not in df.columns]
    
    if missing_columns:
        error = (f"The following columns are missing in the DataFrame: {', '.join(missing_columns)}")
        
    else:
        df = pd.read_excel(path, sheet)
        column_data_types = {}  # Dictionary to store column data types
    for column in selected_columns:
        # Check if the column contains only integers
        is_integer_column = pd.api.types.is_integer_dtype(df[column])
        is_date_column = pd.api.types.is_datetime64_any_dtype(df[column])
        is_float_column = pd.api.types.is_float_dtype(df[column])
        is_string_date_column = False
        if is_date_column:
            df[column] = df[column].dt.strftime('%Y-%m-%d %H:%M:%S')
            is_string_date_column = pd.api.types.is_string_dtype(df[column])

        if is_integer_column:
            column_data_types[column] = 'integer'
        elif is_float_column:
            column_data_types[column] = 'integer'
        elif is_string_date_column:
            column_data_types[column] = 'string'
        else:
            column_data_types[column] = 'string'
        
    all_data_type =  column_data_types
    x_int , y_int , z_int =[] , [] , []
    x_str, y_str, z_str = [], [], []

    for i in x_axis:
        if(all_data_type[i] == 'integer'):
            x_int.append(i)
        elif(all_data_type[i] == 'string'):
            x_str.append(i)
    for i in y_axis:
        if(all_data_type[i] == 'integer'):
            y_int.append(i)
        elif(all_data_type[i] == 'string'):
            y_str.append(i)
    for i in z_axis:
        if(all_data_type[i] == 'integer'):
            z_int.append(i)
        elif(all_data_type[i] == 'string'):
            z_str.append(i)
    x_size = len(x_axis)
    y_size = len(y_axis)
    z_size = len(z_axis)
    x_int_size = len(x_int)
    y_int_size = len(y_int)
    z_int_size = len(z_int)
    x_str_size = len(x_str)
    y_str_size = len(y_str)
    z_str_size = len(z_str)
    return error, df, x_size, y_size, z_size, x_int_size, y_int_size, z_int_size, x_str_size, y_str_size, z_str_size, x_int , y_int , z_int, x_str, y_str, z_str
style_plots = {'position_label':"",'Title_of_label':"",'legend_title_size':"",'legend_title_weight':"",'legend_Title_color':"",'legend_text_color':"",'legend_opacity':"",'legend_box_style':"",'legend_box_size':"",'face_color_legend':"",'edge_color_legend':"",'legend_line_style':"",'legend_line_width':"",'layout_axis_spines':"",'Plot_bg_color': "" , 'layout_theme_style':"",'layout_xtick_color':"",'layout_ytick_color':"",'layout_xlabel_title':"",'layout_xlabel_color':"",'layout_xlabel_background_color':"",'layout_xlabel_border_color':"",'layout_xlabel_box_style':"",'layout_xlabel_Box_Style_pad':"",'layout_ylabel_title':"",'layout_ylabel_color':"",'layout_ylabel_background_color':"",'layout_ylabel_border_color':"",'layout_ylabel_box_style':"",'layout_ylabel_Box_Style_pad':"",'layout_plot_title':"",'layout_title_color':"",'layout_title_background_color':"",'layout_title_border_color':"",'layout_title_box_style':"",'layout_title_Box_Style_pad':"",'marker_color':"",'marker_size':"",'marker_line_width': "",'marker_categorization':"",'marker_palette':"",'marker_alpha':"",'marker_edge_colors':""}
def Simple_plot(path,sheet,x,y,z,style_plot):
    plt.rcdefaults()
    plt.clf() 
    sns.set()
    error, df, x_size, y_size, z_size, x_int_size, y_int_size, z_int_size, x_str_size, y_str_size, z_str_size, x_int , y_int , z_int, x_str, y_str, z_str = plots_function(path, sheet,x,y,z)
    image_base1, image_base2, image_base3,image_base4, image_base5, image_base6, image_base7, image_base8, image_base9,image_base10, image_base11, image_base12, image_base13, image_base14, image_base15, image_base16, image_base17 = "","","","","","","","","","","","","","","","",""
    set_style_plots(style_plots,style_plot)
    if (x_size == 1 and y_size == 1 and z_size == 0):
        if (x_int_size == 1 and y_int_size == 1):
            image_base1 , image_base2, image_base3,image_base4 , image_base5, image_base6,image_base7 , image_base8, image_base9, image_base10, image_base11, image_base12, image_base13, image_base14, image_base15, image_base16, image_base17 = Simple_intint(x_int , y_int , df)
        elif (x_str_size == 1 and y_int_size == 1):
            image_base1, image_base2, image_base3,image_base4, image_base5, image_base6, image_base7, image_base8, image_base9, image_base10, image_base11, image_base12 = Simple_strint(x_str, y_int, df)
        elif (x_int_size == 1 and y_str_size == 1):
            image_base1, image_base2, image_base3, image_base4, image_base5, image_base6, image_base7, image_base8 = Simple_intstr(x_int, y_str, df)
    elif(x_size == 2 and y_size == 1 and z_size == 0):
        if(x_int_size ==1 and x_str_size == 1 and y_int_size == 1):
            image_base1, image_base2, image_base3,image_base4 = Simple_intstrint(x_int,x_str,y_int,df)
        elif(x_int_size == 2 and y_int_size == 1):
            image_base1 = Simple_int2int(x_int, y_int, df)
        elif (x_int_size == 1 and x_str_size == 1 and y_str_size == 1):
            image_base1, image_base2 = Simple_strintstr(x_int, x_str, y_str, df)
        elif(x_int_size == 2 and y_str_size == 1):
            image_base1 = Simple_intintstr(x_int,y_str, df)
    elif(x_size == 1 and y_size == 2 and z_size == 0):
        if(x_int_size ==1 and y_str_size == 1 and y_int_size == 1):
            image_base1, image_base2, image_base3, image_base4 = Simple_intstrint(x_int,y_str,y_int,df)
        elif(x_str_size == 1  and y_int_size == 2):
            image_base1 = Simple_strintint(x_str, y_int ,df)
        elif (y_int_size == 1 and x_str_size == 1 and y_str_size == 1):
            image_base1, image_base2 = Simple_strintstr(y_int, x_str, y_str, df)
        elif(x_int_size == 1 and y_int_size == 2):
            image_base1 = Simple_intint2(x_int, y_int, df)
    elif(x_size == 1 and y_size == 0 and z_size ==0):
        if (x_int_size ==1):
            image_base1,image_base2, image_base3, image_base4, image_base5, image_base6, image_base7, image_base8,image_base9, image_base10  = Simple_intx(x_int , df)
    elif(x_size == 0 and y_size == 1 and z_size ==0):
        if (y_int_size == 1):
            image_base1, image_base2, image_base3  = Simple_inty(y_int , df)
    elif(x_size == 1 and y_size == 3 and z_size == 0):
        if (x_str_size == 1 and y_int_size == 3):
            image_base1 = Simple_strintintint(x_str, y_int, df)
        elif(x_int_size == 1 and y_int_size == 3):
            image_base1 = Simple_intint3(x_int, y_int, df)
    elif(x_size == 3 and y_size == 1):
        if(x_int_size == 3 and y_str_size == 1):
            image_base1 = Simple_intintintstr(x_int, y_str,df)
        elif(x_int_size == 3 and y_int_size == 1):
            image_base1 = Simple_int3int(x_int, y_int, df)
    elif(x_size == 2 and y_size == 2 and z_size == 0):
        if(x_int_size == 2 and y_int_size == 2):
            image_base1 = Simple_int2int2(x_int, y_int, df)
    elif(x_size == 3 and y_size == 3 and z_size == 0):
        if(x_int_size == 3 and y_int_size == 3):
            image_base1 = Simple_int3int3(x_int, y_int, df)
    else:
        print("not found")

            
    return image_base1, image_base2, image_base3 ,image_base4, image_base5, image_base6, image_base7, image_base8, image_base9,image_base10, image_base11, image_base12, image_base13, image_base14, image_base15,image_base16, image_base17

def testplot(path, sheet,x,y,z):
    script , div,script1, div1 , script2, div2 = "","","","","","",
    error, df, x_size, y_size, z_size, x_int_size, y_int_size, z_int_size, x_str_size, y_str_size, z_str_size, x_int , y_int , z_int, x_str, y_str, z_str = plots_function(path, sheet,x,y,z)

    if (x_size == 1 and y_size == 1 and z_size == 0):
        if (x_int_size == 1 and y_int_size == 1):
            script , div, script1, div1, script2, div2 = Doubleint(x_int , y_int , df)
        elif (x_str_size == 1 and y_int_size == 1):
            script , div, script1, div1= strint(x_str, y_int, df)
        elif (x_int_size == 1 and y_str_size == 1):
            script , div, script1, div1= intstr(x_int, y_str, df)
        else:
            print("not avaiable")
    
    if (x_size == 2 and y_size == 1 and z_size == 0):
        if (x_int_size == 2 and y_str_size == 1):
            script , div = twointonestr(x_int, y_str, df)
    if (x_size == 3 and y_size == 1 and z_size == 0):
        if (x_int_size == 3 and y_str_size == 1):
            script , div = threeintonestr(x_int, y_str, df)   

    if (x_size == 1 and y_size == 2 and z_size == 0):
        if (x_str_size == 1 and y_int_size == 2):
             script , div,script1, div1 = One_str_Two_int(x_str, y_int , df)
    if (x_size == 1 and y_size == 3 and z_size == 0):
        if (x_str_size == 1  and y_int_size == 3):
             script , div,script1, div1 = One_str_Three_int(x_str, y_int , df)
    #return path, sheet,x,y,z, error
    return error, script , div,script1, div1 , script2, div2

#Simple plot
def Simple_intint(x_int , y_int , df):
    valuesx = x_int[0]
    valuesy = y_int[0]
    themesseaborn(sns)
    sns.lmplot(
    data=df, x=valuesx, y=valuesy, 
    hue=style_plots["marker_categorization"],line_kws={'color': style_plots["marker_color"], 'linewidth': style_plots["marker_line_width"]},
      ci=10,
     scatter_kws={"s":style_plots["marker_size"], "alpha": style_plots["marker_alpha"], 'edgecolors': style_plots["marker_edge_colors"], 'linewidth': style_plots["marker_line_width"]},
    palette=style_plots["marker_palette"], legend= False)
    
    labels(plt)
    image_stream_1 = io.BytesIO()
    plt.savefig(image_stream_1, format='png')
    image_stream_1.seek(0)

    # Encode the image to base64
    image_base1 = base64.b64encode(image_stream_1.read()).decode('utf-8')
    plt.close()
    # 2
    # Plot scatterplot with scatterplot
    sns.scatterplot(
        data=df, x=valuesx, y=valuesy,color  = style_plots["marker_color"],
        sizes=[style_plots["marker_size"]], edgecolor= style_plots["marker_edge_colors"], linewidth=style_plots["marker_line_width"],alpha = style_plots["marker_alpha"]
    )
    labels(plt)
    image_stream_2 = io.BytesIO()
    plt.savefig(image_stream_2, format='png')
    image_stream_2.seek(0)

    # Encode the image to base64
    image_base2 = base64.b64encode(image_stream_2.read()).decode('utf-8')
    plt.close()
    # 3
    sns.relplot(
        data=df, x=valuesx, y=valuesy,
        hue=style_plots["marker_categorization"], palette=style_plots["marker_palette"],  markers=True,  # Set markers for each dataset
         linewidth=style_plots["marker_line_width"], color=style_plots["marker_color"], alpha=style_plots["marker_alpha"], kind="line" # Adjust marker size and line width
         , legend= False
    )
    labels(plt)

    image_stream_3 = io.BytesIO()
    plt.savefig(image_stream_3, format='png')
    image_stream_3.seek(0)

    # Encode the image to base64
    image_base3 = base64.b64encode(image_stream_3.read()).decode('utf-8')
    plt.close()
    sns.boxplot(x=valuesx, y=valuesy, 
                hue=style_plots["marker_categorization"], palette=style_plots["marker_palette"],color = style_plots["marker_color"],
                data=df)
    labels(plt)
    image_stream_4 = io.BytesIO()
    plt.savefig(image_stream_4, format='png')
    image_stream_4.seek(0)
    image_base4 = base64.b64encode(image_stream_4.read()).decode('utf-8')
    plt.close()
    # 5
    sns.jointplot(data=df, x=valuesx, y=valuesy , hue=style_plots["marker_categorization"],
                  color = style_plots["marker_color"], palette=style_plots["marker_palette"],alpha =style_plots["marker_alpha"])
    image_stream_5 = io.BytesIO()
    plt.savefig(image_stream_5, format='png')
    image_stream_5.seek(0)
    image_base5 = base64.b64encode(image_stream_5.read()).decode('utf-8')
    plt.close()
    fig, ax = plt.subplots(figsize=(8, 6))
    # Create the histplot
    sns.histplot(data=df, x=valuesx, y=valuesy, hue=style_plots["marker_categorization"], color=style_plots["marker_color"], 
                 palette=style_plots["marker_palette"], alpha=style_plots["marker_alpha"], ax=ax)

    legend = ax.legend_
    #underscore_legend_BG(legend)
    underscore_axis(plt)
    image_stream_6 = io.BytesIO()
    plt.savefig(image_stream_6, format='png')
    image_stream_6.seek(0)
    image_base6 = base64.b64encode(image_stream_6.read()).decode('utf-8')
    plt.close()

    sns.jointplot(data=df, x=valuesx, y=valuesy ,color = style_plots["marker_color"],kind="reg")
    image_stream_7 = io.BytesIO()
    plt.savefig(image_stream_7, format='png')
    image_stream_7.seek(0)
    image_base7 = base64.b64encode(image_stream_7.read()).decode('utf-8')
    plt.close()
    sns.jointplot(data=df, x=valuesx, y=valuesy ,color = style_plots["marker_color"], palette=style_plots["marker_palette"],alpha =style_plots["marker_alpha"], kind="hex")
    image_stream_8 = io.BytesIO()
    plt.savefig(image_stream_8, format='png')
    image_stream_8.seek(0)
    image_base8 = base64.b64encode(image_stream_8.read()).decode('utf-8')
    plt.close()

    g = sns.jointplot(data=df, x=valuesx, y=valuesy , hue=style_plots["marker_categorization"],color = style_plots["marker_color"], palette=style_plots["marker_palette"],alpha =style_plots["marker_alpha"])
    #error testing 
    #g.plot_joint(sns.kdeplot, color=style_plots["marker_color"], zorder=0, levels=6)
    g.plot_marginals(sns.rugplot, color=style_plots["marker_color"], clip_on=False)
    image_stream_9 = io.BytesIO()
    plt.savefig(image_stream_9, format='png')
    image_stream_9.seek(0)
    image_base9 = base64.b64encode(image_stream_9.read()).decode('utf-8')
    plt.close()

    f, ax = plt.subplots(figsize=(6, 6))
    sns.scatterplot(data = df ,x=valuesx, y=valuesy, s=style_plots["marker_size"], color=style_plots["marker_color"])
    sns.histplot(data = df ,x=valuesx, y=valuesy, bins=50, pthresh=.1, cmap=style_plots["marker_palette"])
    sns.kdeplot(data = df ,x=valuesx, y=valuesy, levels=5, color=style_plots["marker_color"], linewidths=style_plots["marker_line_width"])
    image_stream_10 = io.BytesIO()
    plt.savefig(image_stream_10, format='png')
    image_stream_10.seek(0)
    image_base10 = base64.b64encode(image_stream_10.read()).decode('utf-8')
    plt.close()
    g = sns.lmplot(x=valuesx, y=valuesy, data=df, palette=style_plots["marker_palette"],  scatter_kws={'color': style_plots["marker_color"]},line_kws={'color': style_plots["marker_color"], 'linewidth': style_plots["marker_line_width"]},
               y_jitter=.02, logistic=True, truncate=False)    
    underscore_axis(plt)
    image_stream_11 = io.BytesIO()
    plt.savefig(image_stream_11, format='png')
    image_stream_11.seek(0)
    image_base11 = base64.b64encode(image_stream_11.read()).decode('utf-8')
    plt.close()
    g = sns.JointGrid(data=df, x=valuesx, y=valuesy,hue = style_plots["marker_categorization"], space=0, ratio=17)
    g.plot_joint(sns.scatterplot, data=df,size=style_plots["marker_size"], sizes=(30, 120),
                 color=style_plots["marker_color"], alpha=style_plots["marker_alpha"])
    g.plot_marginals(sns.rugplot, height=1, color=style_plots["marker_color"], alpha=style_plots["marker_alpha"])
    image_stream_12 = io.BytesIO()
    plt.savefig(image_stream_12, format='png')
    image_stream_12.seek(0)
    image_base12 = base64.b64encode(image_stream_12.read()).decode('utf-8')
    plt.close()

    sns.barplot(data=df, x=valuesx, y=valuesy,hue = style_plots["marker_categorization"],color = style_plots["marker_color"],palette=style_plots["marker_palette"])
    labels(plt)
    image_stream_13 = io.BytesIO()
    plt.savefig(image_stream_13, format='png')
    image_stream_13.seek(0)
    image_base13 = base64.b64encode(image_stream_13.read()).decode('utf-8')
    plt.close()

    sns.lineplot(
    data=df, x=valuesx, y=valuesy, hue=style_plots["marker_categorization"], err_style="bars", 
    err_kws={"capsize": 2},palette=style_plots["marker_palette"],color = style_plots["marker_color"])
    labels(plt)
    image_stream_14 = io.BytesIO()
    plt.savefig(image_stream_14, format='png')
    image_stream_14.seek(0)
    image_base14 = base64.b64encode(image_stream_14.read()).decode('utf-8')
    plt.close()
    # 15
    sns.residplot(data = df , x=valuesx ,y=valuesy, lowess=True, color = style_plots["marker_color"],
                  scatter_kws={'edgecolor': style_plots["marker_edge_colors"], 'linewidth': style_plots["marker_line_width"], 'alpha': style_plots["marker_alpha"]})
    underscore_axis(plt)
    image_stream_15 = io.BytesIO()
    plt.savefig(image_stream_15, format='png')
    image_stream_15.seek(0)
    image_base15 = base64.b64encode(image_stream_15.read()).decode('utf-8')
    plt.close()

    sns.barplot(data=df, x=valuesx, y=valuesy, hue = style_plots["marker_categorization"],color = style_plots["marker_color"] ,palette=style_plots["marker_palette"])
    labels(plt)
    image_stream_16 = io.BytesIO()
    plt.savefig(image_stream_16, format='png')
    image_stream_16.seek(0)
    image_base16 = base64.b64encode(image_stream_16.read()).decode('utf-8')
    plt.close()

    sns.barplot(data=df, x=valuesx, y=valuesy, hue = style_plots["marker_categorization"] ,orient="h",color = style_plots["marker_color"] ,palette=style_plots["marker_palette"])
    labels(plt)
    image_stream_17 = io.BytesIO()
    plt.savefig(image_stream_17, format='png')
    image_stream_17.seek(0)
    image_base17 = base64.b64encode(image_stream_17.read()).decode('utf-8')
    plt.close()
    return image_base1 , image_base2, image_base3,image_base4 , image_base5, image_base6,image_base7 , image_base8, image_base9, image_base10, image_base11, image_base12, image_base13, image_base14, image_base15, image_base16, image_base17
    

def Simple_strint(x_str, y_int, df):
    charx = x_str[0]
    valuesy = y_int[0]
    themesseaborn(sns)
    sns.catplot(
        data=df, x=charx, y=valuesy,
        hue=style_plots["marker_categorization"], palette=style_plots["marker_palette"], s = style_plots["marker_size"],linewidth=style_plots["marker_line_width"],
          color=style_plots["marker_color"], alpha=style_plots["marker_alpha"], edgecolor= style_plots["marker_edge_colors"]  ,legend = True)
    labels(plt)
    image_stream_1 = io.BytesIO()
    plt.savefig(image_stream_1, format='png')
    image_stream_1.seek(0)

    # Encode the image to base64
    image_base1 = base64.b64encode(image_stream_1.read()).decode('utf-8')
    plt.close()
    sns.catplot(
        data=df, x=charx, y=valuesy,
        hue=style_plots["marker_categorization"], palette=style_plots["marker_palette"],  # Arrange plots in columns and rows based on these variables
        kind="point",  # Set the kind of plot to bar
        alpha=style_plots["marker_alpha"],color = style_plots["marker_color"], legend = True # Adjust transparency
    )
    labels(plt)
    image_stream_2 = io.BytesIO()
    plt.savefig(image_stream_2, format='png')
    image_stream_2.seek(0)
    image_base2 = base64.b64encode(image_stream_2.read()).decode('utf-8')
    plt.close()
    sns.catplot(
        data=df, x=charx, y=valuesy,
        hue=style_plots["marker_categorization"], palette=style_plots["marker_palette"], kind="violin", 
        alpha=style_plots["marker_alpha"],color = style_plots["marker_color"], legend = True 
    )
    labels(plt)
    image_stream_3 = io.BytesIO()
    plt.savefig(image_stream_3, format='png')
    image_stream_3.seek(0)
    image_base3 = base64.b64encode(image_stream_3.read()).decode('utf-8')
    plt.close()
    sns.catplot(
        data=df, x=charx, y=valuesy,
        hue=style_plots["marker_categorization"], palette=style_plots["marker_palette"], kind="swarm", 
        alpha=style_plots["marker_alpha"],color = style_plots["marker_color"], legend = True 
    )
    labels(plt)
    image_stream_4 = io.BytesIO()
    plt.savefig(image_stream_4, format='png')
    image_stream_4.seek(0)
    image_base4 = base64.b64encode(image_stream_4.read()).decode('utf-8')
    plt.close()
    themesseaborn(sns)
    sns.catplot(
        data=df, x=charx, y=valuesy,
        hue=style_plots["marker_categorization"], palette=style_plots["marker_palette"], kind="bar", 
        alpha=style_plots["marker_alpha"],color = style_plots["marker_color"], legend = True 
    )
    labels(plt)
    image_stream_5 = io.BytesIO()
    plt.savefig(image_stream_5, format='png')
    image_stream_5.seek(0)
    image_base5 = base64.b64encode(image_stream_5.read()).decode('utf-8')
    plt.close()

    sns.violinplot(data=df, x=charx, y=valuesy, hue=style_plots["marker_categorization"],
               split=True, inner="quart", fill=False,color = style_plots["marker_color"], palette=style_plots["marker_palette"])
    labels(plt)
    image_stream_6 = io.BytesIO()
    plt.savefig(image_stream_6, format='png')
    image_stream_6.seek(0)
    image_base6 = base64.b64encode(image_stream_6.read()).decode('utf-8')
    plt.close()

    sns.boxenplot(
    data = df, x=charx, y=valuesy,color=style_plots["marker_color"],
      hue =style_plots["marker_categorization"],palette=style_plots["marker_palette"])
    labels(plt)
    image_stream_7 = io.BytesIO()
    plt.savefig(image_stream_7, format='png')
    image_stream_7.seek(0)
    image_base7 = base64.b64encode(image_stream_7.read()).decode('utf-8')
    plt.close()

    sns.lineplot(x=charx, y=valuesy, hue=style_plots["marker_categorization"], data=df, marker='o',palette=style_plots["marker_palette"],color = style_plots["marker_color"]) 
    labels(plt)
    image_stream_8 = io.BytesIO()
    plt.savefig(image_stream_8, format='png')
    image_stream_8.seek(0)
    image_base8 = base64.b64encode(image_stream_8.read()).decode('utf-8')
    plt.close()

    sns.set_color_codes("pastel")
    sns.barplot(x=charx, y=valuesy, data=df, color=style_plots["marker_color"],palette=style_plots["marker_palette"], legend=False)
    underscore_axis(plt)
    image_stream_9 = io.BytesIO()
    plt.savefig(image_stream_9, format='png')
    image_stream_9.seek(0)
    image_base9 = base64.b64encode(image_stream_9.read()).decode('utf-8')
    plt.close()

    p = sns.catplot(x=charx, y=valuesy, hue=style_plots["marker_categorization"], data=df, kind="point", markers="o", legend = False, dodge=True,palette=style_plots["marker_palette"],color = style_plots["marker_color"])
    sns.barplot(x=charx, y=valuesy, hue=style_plots["marker_categorization"], data=df, ci="sd", errwidth=1.5, capsize=0.2, dodge=True,palette=style_plots["marker_palette"],color = style_plots["marker_color"])
    labels(plt)
    image_stream_10 = io.BytesIO()
    plt.savefig(image_stream_10, format='png')
    image_stream_10.seek(0)
    image_base10 = base64.b64encode(image_stream_10.read()).decode('utf-8')
    plt.close()

    sns.pointplot(x=charx, y=valuesy,hue = style_plots["marker_categorization"], data=df, palette=style_plots["marker_palette"],color =style_plots["marker_color"])
    labels(plt)
    image_stream_11 = io.BytesIO()
    plt.savefig(image_stream_11, format='png')
    image_stream_11.seek(0)
    image_base11 = base64.b64encode(image_stream_11.read()).decode('utf-8')
    plt.close()

    sns.lineplot(data=df, x=charx, y=valuesy, sort=False, lw=style_plots["marker_line_width"],palette=style_plots["marker_palette"],color = style_plots["marker_color"])
    underscore_axis(plt)

    image_stream_12 = io.BytesIO()
    plt.savefig(image_stream_12, format='png')
    image_stream_12.seek(0)
    image_base12 = base64.b64encode(image_stream_12.read()).decode('utf-8')
    plt.close()
    return image_base1 , image_base2, image_base3, image_base4, image_base5, image_base6, image_base7,image_base8, image_base9, image_base10, image_base11, image_base12

def Simple_intstr(x_int, y_str, df):
    valuesx = x_int[0]
    chary = y_str[0]
    themesseaborn(sns)
    sns.boxplot(
        data = df, x=valuesx, y=chary, palette=style_plots["marker_palette"], color = style_plots["marker_color"]
    )
    sns.stripplot(data = df, x=valuesx, y=chary, hue= style_plots["marker_categorization"], size=style_plots["marker_size"], color=style_plots["marker_color"], palette=style_plots["marker_palette"] )
    labels(plt)
    image_stream_1 = io.BytesIO()
    plt.savefig(image_stream_1, format='png')
    image_stream_1.seek(0)
    image_base1 = base64.b64encode(image_stream_1.read()).decode('utf-8')
    plt.close()
    sns.swarmplot(data=df, x=valuesx, y=chary, hue=style_plots["marker_categorization"] , color =style_plots["marker_color"], palette=style_plots["marker_palette"],s = style_plots["marker_size"], alpha= style_plots["marker_alpha"] ,edgecolor="seagreen", linewidth=style_plots["marker_line_width"] )
    labels(plt)
    image_stream_2 = io.BytesIO()
    plt.savefig(image_stream_2, format='png')
    image_stream_2.seek(0)
    image_base2 = base64.b64encode(image_stream_2.read()).decode('utf-8')
    plt.close()
    sns.violinplot(x=valuesx, y=chary, data=df, orient="h", color = style_plots["marker_color"] , hue =style_plots["marker_categorization"]
               ,palette=style_plots["marker_palette"], fill=False)
    labels(plt)
    image_stream_3 = io.BytesIO()
    plt.savefig(image_stream_3, format='png')
    image_stream_3.seek(0)
    image_base3 = base64.b64encode(image_stream_3.read()).decode('utf-8')
    plt.close()
    sns.lineplot(x=valuesx, y=chary, hue=style_plots["marker_categorization"], data=df, marker='o',palette=style_plots["marker_palette"],color = style_plots["marker_color"]) 
    labels(plt)
    image_stream_4 = io.BytesIO()
    plt.savefig(image_stream_4, format='png')
    image_stream_4.seek(0)
    image_base4 = base64.b64encode(image_stream_4.read()).decode('utf-8')
    plt.close()

    sns.set_color_codes("pastel")
    sns.barplot(x=valuesx, y=chary, data=df, color=style_plots["marker_color"],palette=style_plots["marker_palette"], legend=False)
    underscore_axis(plt)
    image_stream_5 = io.BytesIO()
    plt.savefig(image_stream_5, format='png')
    image_stream_5.seek(0)
    image_base5 = base64.b64encode(image_stream_5.read()).decode('utf-8')
    plt.close()

    sns.stripplot(x=valuesx, y=chary, hue = style_plots["marker_categorization"], data=df, size=style_plots["marker_size"], alpha=style_plots["marker_alpha"], jitter=0.3,palette=style_plots["marker_palette"],color = style_plots["marker_color"])
    sns.boxplot(x=valuesx, y=chary, data=df, width=0.2, color=style_plots["marker_color"],palette=style_plots["marker_palette"])
    labels(plt)
    image_stream_6 = io.BytesIO()
    plt.savefig(image_stream_6, format='png')
    image_stream_6.seek(0)
    image_base6 = base64.b64encode(image_stream_6.read()).decode('utf-8')
    plt.close()

    sns.violinplot(data=df, x=valuesx, y=chary,hue = style_plots["marker_categorization"], scale="width", inner="stick", palette=style_plots["marker_palette"])
    labels(plt)
    image_stream_7 = io.BytesIO()
    plt.savefig(image_stream_7, format='png')
    image_stream_7.seek(0)
    image_base7 = base64.b64encode(image_stream_7.read()).decode('utf-8')
    plt.close()

    sns.boxplot(
    data=df, x=valuesx, y=chary,hue = style_plots["marker_categorization"],
    notch=True, showcaps=False,flierprops={"marker": "x"},boxprops={"alpha": style_plots["marker_alpha"]},
    medianprops={"color": style_plots["marker_color"], "linewidth": style_plots["marker_line_width"]},palette=style_plots["marker_palette"],color = style_plots["marker_color"])
    labels(plt)
    image_stream_8 = io.BytesIO()
    plt.savefig(image_stream_8, format='png')
    image_stream_8.seek(0)
    image_base8 = base64.b64encode(image_stream_8.read()).decode('utf-8')
    plt.close()
    return image_base1, image_base2, image_base3, image_base4,image_base5, image_base6, image_base7, image_base8

def Simple_intstrint(x_int,x_str,y_int,df):
    valuesx = x_int[0]
    charx = x_str[0]
    valuesy = y_int[0]
    themesseaborn(sns)
    scatter_plot =sns.relplot(
        data=df, x=valuesx, y=valuesy,
        hue=style_plots["marker_categorization"], palette=style_plots["marker_palette"],  # Set color palette for different datasets
        style=charx, markers=True,s = style_plots["marker_size"], # Set markers for each dataset
          color=style_plots["marker_color"], alpha=style_plots["marker_alpha"], kind="scatter" # Adjust marker size and line width
    )
    legend = scatter_plot._legend
    underscore_legend(legend)
    underscore_axis(plt)

    image_stream_1 = io.BytesIO()
    plt.savefig(image_stream_1, format='png')
    image_stream_1.seek(0)

    # Encode the image to base64
    image_base1 = base64.b64encode(image_stream_1.read()).decode('utf-8')
    plt.close()

    scatter_plot =sns.relplot(
        data=df, x=valuesx, y=valuesy,
        hue=style_plots["marker_categorization"], palette=style_plots["marker_palette"],  # Set color palette for different datasets
        style=charx, markers=True, linewidth = style_plots["marker_line_width"], # Set markers for each dataset
          color=style_plots["marker_color"], alpha=style_plots["marker_alpha"], kind="line" # Adjust marker size and line width
    )

    legend = scatter_plot._legend
    underscore_legend(legend)
    underscore_axis(plt)

    image_stream_2 = io.BytesIO()
    plt.savefig(image_stream_2, format='png')
    image_stream_2.seek(0)
    image_base2 = base64.b64encode(image_stream_2.read()).decode('utf-8')
    plt.close()

    sns.lineplot(
    data=df, x=valuesx, y=valuesy, 
    hue=style_plots["marker_categorization"], palette=style_plots["marker_palette"],  # Set color palette for different datasets
    style=charx, markers=True,  # Set markers for each dataset
    markersize=style_plots["marker_size"], linewidth=style_plots["marker_line_width"],color = style_plots["marker_color"] ,alpha = style_plots["marker_alpha"],markeredgecolor= style_plots["marker_edge_colors"],markeredgewidth=2    # Adjust marker size and line width
    )
    labels(plt)
    image_stream_3 = io.BytesIO()
    plt.savefig(image_stream_3, format='png')
    image_stream_3.seek(0)
    image_base3 = base64.b64encode(image_stream_3.read()).decode('utf-8')
    plt.close()

    sns.lineplot(data=df, x=valuesx, y=valuesy, hue=style_plots["marker_categorization"], style=charx, markers=True,palette=style_plots["marker_palette"],color = style_plots["marker_color"])
    labels(plt)
    image_stream_4 = io.BytesIO()
    plt.savefig(image_stream_4, format='png')
    image_stream_4.seek(0)
    image_base4 = base64.b64encode(image_stream_4.read()).decode('utf-8')
    plt.close()

    return image_base1, image_base2, image_base3, image_base4

def Simple_strintstr(x_int, x_str, y_str, data):
    value = x_int[0]
    char1 = y_str[0]
    char2 = x_str[0]
    heatmap_data = data.pivot_table(index=char1, columns=char2, values=value)
    # Create a heatmap using Seaborn
    sns.heatmap(heatmap_data, cmap=style_plots["marker_palette"], annot=True, fmt=".2f", cbar=True)
    underscore_axis(plt)
    image_stream_1 = io.BytesIO()
    plt.savefig(image_stream_1, format='png')
    image_stream_1.seek(0)
    image_base1 = base64.b64encode(image_stream_1.read()).decode('utf-8')
    plt.close()
    clustermap_data = data.pivot_table(index=char1, columns=char2, values=value)
    clustermap_data = clustermap_data.fillna(clustermap_data.mean())
    sns.clustermap(
        data=clustermap_data,
        figsize=(10, 8),
        row_cluster=True,
        col_cluster=True,
        annot=True,
        cmap=style_plots["marker_palette"],
        dendrogram_ratio=(.1, .2),
        cbar_pos=(0, .2, .03, .4),color = style_plots["marker_color"]
    )
    image_stream_2 = io.BytesIO()
    plt.savefig(image_stream_2, format='png')
    image_stream_2.seek(0)
    image_base2 = base64.b64encode(image_stream_2.read()).decode('utf-8')
    plt.close()
    return image_base1, image_base2

def Simple_intintstr(x_int,y_str, df):
    valuex1 = x_int[0]
    valuex2 = x_int[1]
    chary = y_str[0]
    themesseaborn(sns)
    palette = sns.color_palette(style_plots["marker_palette"])
    sns.barplot(x=valuex1, y=chary, data=df,
                label=valuex1, color=palette[0])
    sns.barplot(x=valuex2, y=chary, data=df,
                label=valuex2, color=palette[1])
    underscore_axis(plt)
    image_stream_1 = io.BytesIO()
    plt.savefig(image_stream_1, format='png')
    image_stream_1.seek(0)
    image_base1 = base64.b64encode(image_stream_1.read()).decode('utf-8')
    return image_base1
def Simple_strintint(x_str, y_int ,df):
    charx = x_str[0]
    valuesy1 = y_int[0]
    valuesy2 = y_int[1]
    themesseaborn(sns)
    palette = sns.color_palette(style_plots["marker_palette"])
    sns.barplot(x=charx, y=valuesy1, data=df,
                label=valuesy1,color=palette[0])
    sns.barplot(x=charx, y=valuesy2, data=df,
                label=valuesy2,color=palette[1])
    underscore_axis(plt)
    image_stream_1 = io.BytesIO()
    plt.savefig(image_stream_1, format='png')
    image_stream_1.seek(0)
    image_base1 = base64.b64encode(image_stream_1.read()).decode('utf-8')
    plt.close()
    return image_base1
def Simple_strintintint(x_str, y_int, df):
    charx = x_str[0]
    valuesy1 = y_int[0]
    valuesy2 = y_int[1]
    valuesy3 = y_int[2]
    themesseaborn(sns)
    palette = sns.color_palette(style_plots["marker_palette"])
    sns.barplot(x=charx, y=valuesy1, data=df,
                label=valuesy1, color=palette[0])
    sns.barplot(x=charx, y=valuesy2, data=df,
                label=valuesy2, color=palette[1])
    sns.barplot(x=charx, y=valuesy3, data=df,
                label=valuesy3, color=palette[2])
    underscore_axis(plt)
    image_stream_1 = io.BytesIO()
    plt.savefig(image_stream_1, format='png')
    image_stream_1.seek(0)
    image_base1 = base64.b64encode(image_stream_1.read()).decode('utf-8')
    plt.close()
    return image_base1
def Simple_intintintstr(x_int, y_str,df):
    valuex1 = x_int[0]
    valuex2 = x_int[1]
    valuex3 = x_int[2]
    chary = y_str[0]
    themesseaborn(sns)
    palette = sns.color_palette(style_plots["marker_palette"])
    sns.barplot(x=valuex1, y=chary, data=df,
                label=valuex1, color=palette[0])
    sns.barplot(x=valuex2, y=chary, data=df,
                label=valuex2, color=palette[1])
    sns.barplot(x=valuex3, y=chary, data=df,
                label=valuex3, color=palette[2])
    underscore_axis(plt)
    image_stream_1 = io.BytesIO()
    plt.savefig(image_stream_1, format='png')
    image_stream_1.seek(0)
    image_base1 = base64.b64encode(image_stream_1.read()).decode('utf-8')
    plt.close()
    return image_base1
def Simple_intx(x_int , df):
    valuesx = x_int[0]
    themesseaborn(sns)
    sns.displot(
    data=df, x=valuesx, hue=style_plots["marker_categorization"], palette=style_plots["marker_palette"],  # Set color palette for different datasets
    kde=True, rug=True,  # Add kernel density estimate and rug plot
    element="step", linewidth=style_plots["marker_line_width"],  # Adjust line width
    edgecolor=style_plots["marker_edge_colors"],color = style_plots["marker_color"],alpha = style_plots["marker_alpha"], bins = 41   # Set the color of the step edges
    )
    underscore_axis(plt)
    image_stream_1 = io.BytesIO()
    plt.savefig(image_stream_1, format='png')
    image_stream_1.seek(0)

    # Encode the image to base64
    image_base1 = base64.b64encode(image_stream_1.read()).decode('utf-8')
    plt.close()
    sns.histplot(
    data = df,x=valuesx, hue=style_plots["marker_categorization"],multiple="stack",
    palette=style_plots["marker_palette"],edgecolor=style_plots["marker_edge_colors"],linewidth=style_plots["marker_line_width"],log_scale=True)
    underscore_axis(plt)
    image_stream_2 = io.BytesIO()
    plt.savefig(image_stream_2, format='png')
    image_stream_2.seek(0)
    image_base2 = base64.b64encode(image_stream_2.read()).decode('utf-8')
    plt.close()
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.histplot(data=df, x=valuesx, hue=style_plots["marker_categorization"],multiple="stack", color=style_plots["marker_color"], palette=style_plots["marker_palette"], 
                 alpha=style_plots["marker_alpha"], ax=ax, edgecolor=style_plots['marker_edge_colors'],linewidth=style_plots["marker_line_width"],log_scale=True,)

    #legend = ax.legend
    #underscore_legend_BG(legend)
    #underscore_axis(plt)
    labels(plt)
    image_stream_3 = io.BytesIO()
    plt.savefig(image_stream_3, format='png')
    image_stream_3.seek(0)
    image_base3 = base64.b64encode(image_stream_3.read()).decode('utf-8')
    plt.close()
    if(style_plots["marker_categorization"] != None):

        sns.displot(
        data=df,x=valuesx, hue=style_plots["marker_categorization"],kind="kde",
        multiple="fill", clip=(0, None),palette=style_plots["marker_palette"])
        underscore_axis(plt)
        image_stream_4 = io.BytesIO()
        plt.savefig(image_stream_4, format='png')
        image_stream_4.seek(0)
        image_base4 = base64.b64encode(image_stream_4.read()).decode('utf-8')
        plt.close()
    else:
        image_base4 = ""

    sns.displot(
        data = df,x=valuesx, hue=style_plots["marker_categorization"],
    kind="ecdf", aspect=.75, linewidth=style_plots["marker_line_width"], palette=style_plots["marker_palette"])
    underscore_axis(plt)
    image_stream_5 = io.BytesIO()
    plt.savefig(image_stream_5, format='png')
    image_stream_5.seek(0)
    image_base5 = base64.b64encode(image_stream_5.read()).decode('utf-8')
    plt.close()

    ax = sns.countplot(x =valuesx, data=df, palette=style_plots["marker_palette"],orient="h", hue = style_plots["marker_categorization"],color = style_plots["marker_color"])
    # Add count annotations
    for p in ax.patches:
        ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', fontsize=10, color='black', xytext=(0, 5),
                    textcoords='offset points')

    labels(plt)
    image_stream_6 = io.BytesIO()
    plt.savefig(image_stream_6, format='png')
    image_stream_6.seek(0)
    image_base6 = base64.b64encode(image_stream_6.read()).decode('utf-8')
    plt.close()

    sns.histplot(x=valuesx, data=df, bins=30, kde=True, hue=style_plots["marker_categorization"], multiple="stack", palette=style_plots["marker_palette"], element="step", fill=False, alpha=style_plots["marker_alpha"],color = style_plots["marker_color"])
    underscore_axis(plt)
    image_stream_7 = io.BytesIO()
    plt.savefig(image_stream_7, format='png')
    image_stream_7.seek(0)
    image_base7 = base64.b64encode(image_stream_7.read()).decode('utf-8')
    plt.close()

    sns.countplot(x=valuesx, hue= style_plots["marker_categorization"], data=df, palette=style_plots["marker_palette"], dodge=False,color = style_plots["marker_color"])
    labels(plt)
    image_stream_8 = io.BytesIO()
    plt.savefig(image_stream_8, format='png')
    image_stream_8.seek(0)
    image_base8 = base64.b64encode(image_stream_8.read()).decode('utf-8')
    plt.close()

    sns.countplot(x=valuesx, hue=style_plots["marker_categorization"], data=df, palette=style_plots["marker_palette"], dodge=True,color = style_plots["marker_color"])
    labels(plt)
    image_stream_9 = io.BytesIO()
    plt.savefig(image_stream_9, format='png')
    image_stream_9.seek(0)
    image_base9 = base64.b64encode(image_stream_9.read()).decode('utf-8')
    plt.close()

    sns.kdeplot(
        data=df, x=valuesx, hue=style_plots["marker_categorization"],
        fill=True, common_norm=False, palette=style_plots["marker_palette"],
        alpha=style_plots["marker_alpha"], linewidth=style_plots["marker_line_width"],color = style_plots["marker_color"])
    underscore_axis(plt)
    image_stream_10 = io.BytesIO()
    plt.savefig(image_stream_10, format='png')
    image_stream_10.seek(0)
    image_base10 = base64.b64encode(image_stream_10.read()).decode('utf-8')
    plt.close()
    return image_base1,image_base2, image_base3, image_base4, image_base5, image_base6, image_base7, image_base8,image_base9, image_base10

def Simple_inty(y_int , df):
    valuesy = y_int[0]
    themesseaborn(sns)
    sns.displot(
    data=df, y=valuesy, hue=style_plots["marker_categorization"], palette=style_plots["marker_palette"],  # Set color palette for different datasets
    kde=True, rug=True,  # Add kernel density estimate and rug plot
    element="step", linewidth=style_plots["marker_line_width"],  # Adjust line width
    edgecolor=style_plots["marker_edge_colors"],color = style_plots["marker_color"],alpha = style_plots["marker_alpha"], bins = 41   # Set the color of the step edges
    )
    underscore_axis(plt)
    image_stream_1 = io.BytesIO()
    plt.savefig(image_stream_1, format='png')
    image_stream_1.seek(0)

    # Encode the image to base64
    image_base1 = base64.b64encode(image_stream_1.read()).decode('utf-8')
    plt.close()

    ax = sns.countplot(y=valuesy, data=df, palette=style_plots["marker_palette"], hue = style_plots["marker_categorization"] ,color = style_plots["marker_color"])
    for p in ax.patches:
        ax.annotate(f'{p.get_width()}', (p.get_width(), p.get_y() + p.get_height() / 2.),
                    ha='left', va='center', fontsize=10, color='black', xytext=(5, 0),
                    textcoords='offset points')

    labels(plt)
    image_stream_2 = io.BytesIO()
    plt.savefig(image_stream_2, format='png')
    image_stream_2.seek(0)
    image_base2 = base64.b64encode(image_stream_2.read()).decode('utf-8')
    plt.close()

    sns.histplot(y=valuesy, data=df,hue =style_plots["marker_categorization"],  bins=30, kde=True, color=style_plots["marker_color"],palette=style_plots["marker_palette"])
    underscore_axis(plt)
    image_stream_3 = io.BytesIO()
    plt.savefig(image_stream_3, format='png')
    image_stream_3.seek(0)
    image_base3 = base64.b64encode(image_stream_3.read()).decode('utf-8')
    plt.close()

    return image_base1, image_base2, image_base3

def Simple_int2int(x_int, y_int, df):
    valuex1 = x_int[0]
    valuex2 = x_int[1]
    valuey = y_int[0]
    themesseaborn(sns)
    sns.set_palette(style_plots["marker_palette"])
    sns.scatterplot(x=valuex1, y=valuey, data=df, label=valuex1, marker='o')
    sns.scatterplot(x=valuex2, y=valuey, data=df, label=valuex2, marker='s')

    sns.lineplot(x=valuex1, y=valuey, data=df)
    sns.lineplot(x=valuex2, y=valuey, data=df)
    labels(plt)
    image_stream_1 = io.BytesIO()
    plt.savefig(image_stream_1, format='png')
    image_stream_1.seek(0)

    # Encode the image to base64
    image_base1 = base64.b64encode(image_stream_1.read()).decode('utf-8')
    plt.close()
    return image_base1
def Simple_intint2(x_int, y_int, df):
    valuex = x_int[0]
    valuey1 = y_int[0]
    valuey2 = y_int[1]
    themesseaborn(sns)
    sns.set_palette(style_plots["marker_palette"])
    sns.scatterplot(x=valuex, y=valuey1, data=df, label=valuey1, marker='o')
    sns.scatterplot(x=valuex, y=valuey2, data=df, label=valuey2, marker='s')

    sns.lineplot(x=valuex, y=valuey1, data=df)
    sns.lineplot(x=valuex, y=valuey2, data=df)

    labels(plt)
    image_stream_1 = io.BytesIO()
    plt.savefig(image_stream_1, format='png')
    image_stream_1.seek(0)

    # Encode the image to base64
    image_base1 = base64.b64encode(image_stream_1.read()).decode('utf-8')
    plt.close()
    return image_base1
def Simple_intint3(x_int, y_int, df):
    valuex = x_int[0]
    valuey1 = y_int[0]
    valuey2 = y_int[1]
    valuey3 = y_int[2]
    themesseaborn(sns)
    sns.set_palette(style_plots["marker_palette"])
    sns.scatterplot(x=valuex, y=valuey1, data=df, label=valuey1, marker='o')
    sns.scatterplot(x=valuex, y=valuey2, data=df, label=valuey2, marker='s')
    sns.scatterplot(x=valuex, y=valuey3, data=df, label=valuey3, marker='^')

    sns.lineplot(x=valuex, y=valuey1, data=df)
    sns.lineplot(x=valuex, y=valuey2, data=df)
    sns.lineplot(x=valuex, y=valuey3, data=df)

    labels(plt)
    image_stream_1 = io.BytesIO()
    plt.savefig(image_stream_1, format='png')
    image_stream_1.seek(0)

    # Encode the image to base64
    image_base1 = base64.b64encode(image_stream_1.read()).decode('utf-8')
    plt.close()
    return image_base1
def Simple_int3int(x_int, y_int, df):
    valuex1 = x_int[0]
    valuex2 = x_int[1]
    valuex3 = x_int[2]
    valuey = y_int[0]
    themesseaborn(sns)
    sns.set_palette(style_plots["marker_palette"])
    sns.scatterplot(x=valuex1, y=valuey, data=df, label=valuex1, marker='o')
    sns.scatterplot(x=valuex2, y=valuey, data=df, label=valuex2, marker='s')
    sns.scatterplot(x=valuex3, y=valuey, data=df, label=valuex3, marker='^')

    sns.lineplot(x=valuex1, y=valuey, data=df)
    sns.lineplot(x=valuex2, y=valuey, data=df)
    sns.lineplot(x=valuex3, y=valuey, data=df)

    labels(plt)
    image_stream_1 = io.BytesIO()
    plt.savefig(image_stream_1, format='png')
    image_stream_1.seek(0)

    # Encode the image to base64
    image_base1 = base64.b64encode(image_stream_1.read()).decode('utf-8')
    plt.close()
    return image_base1
def Simple_int2int2(x_int, y_int, df):
    valuex1 = x_int[0]
    valuex2 = x_int[1]
    valuey1 = y_int[0]
    valuey2 = y_int[1]
    themesseaborn(sns)
    sns.set_palette(style_plots["marker_palette"])
    sns.scatterplot(x=valuex1, y=valuey1, data=df, label=valuey1, marker='o')
    sns.scatterplot(x=valuex2, y=valuey2, data=df, label=valuey2, marker='s')

    sns.lineplot(x=valuex1, y=valuey1, data=df)
    sns.lineplot(x=valuex2, y=valuey2, data=df)

    labels(plt)
    image_stream_1 = io.BytesIO()
    plt.savefig(image_stream_1, format='png')
    image_stream_1.seek(0)

    # Encode the image to base64
    image_base1 = base64.b64encode(image_stream_1.read()).decode('utf-8')
    plt.close()
    return image_base1
def Simple_int3int3(x_int, y_int, df):
    valuex1 = x_int[0]
    valuex2 = x_int[1]
    valuex3 = x_int[2]
    valuey1 = y_int[0]
    valuey2 = y_int[1]
    valuey3 = y_int[2]
    themesseaborn(sns)
    sns.set_palette(style_plots["marker_palette"])
    sns.scatterplot(x=valuex1, y=valuey1, data=df, label=valuey1, marker='o')
    sns.scatterplot(x=valuex2, y=valuey2, data=df, label=valuey2, marker='s')
    sns.scatterplot(x=valuex3, y=valuey3, data=df, label=valuey3, marker='^')

    sns.lineplot(x=valuex1, y=valuey1, data=df)
    sns.lineplot(x=valuex2, y=valuey2, data=df)
    sns.lineplot(x=valuex3, y=valuey3, data=df)

    labels(plt)
    image_stream_1 = io.BytesIO()
    plt.savefig(image_stream_1, format='png')
    image_stream_1.seek(0)

    # Encode the image to base64
    image_base1 = base64.b64encode(image_stream_1.read()).decode('utf-8')
    plt.close()
    return image_base1



def color_generate(size):
    color_code = []
    for i in range(1,size+1):
        # Generate random values for RR, GG, and BB (0-255)
            rr = random.randint(0, 255)
            gg = random.randint(0, 255)
            bb = random.randint(0, 255)

        # Convert the values to hexadecimal format and create the color code
            color_code.append("#{:02X}{:02X}{:02X}".format(rr, gg, bb))
    return color_code

def Doubleint(x_int , y_int , df):
    x = x_int[0]
    x = str(x)
    y = y_int[0]
    y = str(y)
    source = ColumnDataSource(df)
    TOOLS="hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,examine,help"
    fig = figure(width=600, height=600, tools=TOOLS)
    fig.vbar(
        x = x,
        width=0.5,
        bottom=0,
        top=y,
        source = source,
        color='navy'
    )
    #2 plot
    source = ColumnDataSource(df)
    p = figure(tools=TOOLS)
    p.scatter(x=x, y=y, source=source, color = '#F05223', size=10, fill_alpha=0.6)
    #3 plot
    source = ColumnDataSource(df)
    l = figure(width=800, height=300, tools=TOOLS)
    l.line(x=x, y=y, source=source ,color="navy", alpha=0.4, line_width=4)

    script, div = components(fig)
    script1, div1 = components(p)
    script2, div2 = components(l)


    return script , div, script1, div1, script2, div2

def strint(x_str, y_int, df):
    size = len(df)
    color_code = color_generate(size)
    x = x_str[0]
    y = y_int[0]
    grouped_data = df.groupby(x)[y].sum().reset_index()
    xstr = grouped_data[x]
    yint = grouped_data[y]
    size = len(grouped_data)
    color_code = color_generate(size)
    grouped_data['angle'] = yint/yint.sum() * 2*pi
    Selected_Column = ("@{{{}}}:@{{{}}}".format(x ,y))

    p = figure(height=350, title="", toolbar_location=None,
           tools="hover", tooltips=Selected_Column, x_range=(-0.5, 1.0))
    grouped_data['color'] = color_code[0:size]
    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color="color", legend_field=x_str[0], source=grouped_data)

    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None

    # 2
    color_palette = color_code
    b = figure(x_range=xstr, height=350, title="Profit by State", toolbar_location=None, tools="")

    # Use factor_cmap to map each state to a color
    b.vbar(x=xstr, top=yint, width=0.9,
           line_color="white", fill_color=factor_cmap(field_name='x', palette=color_palette, factors=xstr))

    b.xgrid.grid_line_color = None
    #b.y_range.start = 0

    script, div = components(p)
    script1, div1 = components(b)
    return script, div ,script1, div1

def intstr(x_int, y_str, df):
    x = x_int[0]
    y = y_str[0]
    grouped_data = df.groupby(y)[x].sum().reset_index()
    ystr = grouped_data[y]
    xint = grouped_data[x]
    size = len(grouped_data)
    color_code = color_generate(size)
    grouped_data['angle'] = xint/xint.sum() * 2*pi
    Selected_Column = ("@{{{}}}:@{{{}}}".format(y ,x))

    p = figure(height=350, title="", toolbar_location="right",
           tools="hover, save", tooltips=Selected_Column, x_range=(-0.5, 1.0))
    grouped_data['color'] = color_code[0:size]
    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color="color", legend_field=y_str[0], source=grouped_data)

    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None
    script, div = components(p)
    #2 
    color_palette = color_code

    # Create a ColumnDataSource for the data
    source = ColumnDataSource(data=dict(ystr=ystr, xint=xint))

    b = figure(y_range=ystr, title="Profit by State", toolbar_location=None, tools="")

    # Use hbar_stack to create a stacked bar plot
    b.hbar(y='ystr', left=0, right='xint', height=0.9, source=source, line_color="white",
           fill_color=factor_cmap(field_name='ystr', palette=color_palette, factors=ystr))

    b.xgrid.grid_line_color = None
    b.ygrid.grid_line_color = None
    b.xaxis.axis_label = ""
    b.yaxis.axis_label = ""
    script, div = components(p)
    script1, div1 = components(b)
    return script, div ,script1, div1

def twointonestr(x_int, y_str, df):
    data = df
    x1 = x_int[0]
    x2 = x_int[1]
    y = y_str[0]
    x_col = [x1,x2]
    tooltips = "$name, @{}:@$name".format(y)
    df = pd.DataFrame(data)
    grouped = df.groupby(y).sum()
    y_grouped = grouped.index.tolist()
    source = ColumnDataSource(grouped)

    p = figure(y_range=y_grouped, height=250, title="", tools="hover", tooltips=tooltips)
    acolor = ('#756bb1', '#bcbddc')
    p.hbar_stack([x1,x2], y=y, height=0.9, color=acolor ,source=source, legend_label=x_col)
    script, div = components(p)
    return script, div 

def threeintonestr(x_int, y_str, df):
    data = df
    x1 = x_int[0]
    x2 = x_int[1]
    x3 = x_int[2]
    y = y_str[0]
    x_col = [x1,x2,x3]
    tooltips = "$name, @{}:@$name".format(y)
    df = pd.DataFrame(data)
    grouped = df.groupby(y).sum()
    y_grouped = grouped.index.tolist()
    source = ColumnDataSource(grouped)
    p = figure(y_range=y_grouped, height=250, title="",tools="hover", tooltips=tooltips)
    p.hbar_stack([x1,x2,x3], y=y, height=0.9, color=GnBu3 ,source=source, legend_label=x_col)

    script, div = components(p)
    return script, div

def One_str_Two_int(x_str, y_int , df):
    y1 = y_int[0]
    y2 = y_int[1]
    x = x_str[0]
    data = df
    y = [y1,y2]
    tooltips = "$name @{}: @$name".format(x)
    df = pd.DataFrame(data)
    grouped = df.groupby(x).sum()
    x_grouped = grouped.index.tolist()
    source = ColumnDataSource(grouped)
    green2 = ('#31a354', '#a1d99b')
    p = figure(x_range=x_grouped, height=250, title="",toolbar_location=None, 
           tools="hover", tooltips=tooltips)
    p.vbar_stack([y1,y2], x=x, width=0.9, color=green2, source=source,legend_label=y)

    #p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"

    x_grouped = grouped.index.tolist()
    source = ColumnDataSource(grouped)

    df = pd.DataFrame(data)
    grouped = df.groupby(x).sum()
    y = [y1,y2]
    x_grouped = grouped.index.tolist()
    source = ColumnDataSource(grouped)
    
    x_data = [ (x_grouped, y_data) for x_grouped in x_grouped for y_data in y ]
    counts = sum(zip(grouped[y1], grouped[y2]), ()) 
    
    source = ColumnDataSource(data=dict(x_side=x_data, counts=counts))
    TOOLS="hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,examine,help"

    b = figure(x_range=FactorRange(*x_data), height=350, title="",
            toolbar_location="left",output_backend="svg", tools="hover,zoom_in,zoom_out,box_zoom,undo,redo,reset", tooltips="@counts @x_side")
    
    b.vbar(x='x_side', top='counts', width=0.9, source=source, line_color="white",
        fill_color=factor_cmap('x_side', palette=Greens3, factors=y, start=1, end=2))
    
    #b.y_range.start = 0
    b.x_range.range_padding = 0.1
    b.y_range.range_padding = 0.1
    b.xaxis.major_label_orientation = 1
    b.xgrid.grid_line_color = "green"


    script, div = components(p)
    script1, div1 = components(b)
    return script, div,script1, div1
def One_str_Three_int(x_str, y_int , df):
    y1 = y_int[0]
    y2 = y_int[1]
    y3 = y_int[2]
    x = x_str[0]
    data = df
    y = [y1,y2,y3]
    tooltips = "$name @{}: @$name".format(x)
    df = pd.DataFrame(data)
    grouped = df.groupby(x).sum()
    x_grouped = grouped.index.tolist()
    source = ColumnDataSource(grouped)
    p = figure(x_range=x_grouped, height=250, title="",toolbar_location=None, tools="hover", tooltips=tooltips)
    p.vbar_stack([y1,y2,y3], x=x, width=0.9, color=Greens3, source=source,legend_label=y)
    #p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"


    
    x_grouped = grouped.index.tolist()
    source = ColumnDataSource(grouped)

    df = pd.DataFrame(data)
    grouped = df.groupby(x).sum()
    y = [y1,y2,y3]
    x_grouped = grouped.index.tolist()
    source = ColumnDataSource(grouped)
    
    x_data = [ (x_grouped, y_data) for x_grouped in x_grouped for y_data in y ]
    counts = sum(zip(grouped[y1], grouped[y2], grouped[y3]), ()) 
    
    source = ColumnDataSource(data=dict(x_side=x_data, counts=counts))
    
    b = figure(x_range=FactorRange(*x_data), height=350, title="",
            toolbar_location=None,output_backend="svg", tools="hover", tooltips="@counts @x_side")
    
    b.vbar(x='x_side', top='counts', width=0.9, source=source, line_color="white",
        fill_color=factor_cmap('x_side', palette=Bokeh3, factors=y, start=1, end=2))
    
    #b.y_range.start = 0
    b.x_range.range_padding = 0.1
    b.xaxis.major_label_orientation = 1
    b.xgrid.grid_line_color = None
    

    script, div = components(p)
    script1, div1 = components(b)
    return script, div,script1, div1
    


def One_data_analysis(data , selected_column_max, selected_column_min, selected_column_sum, selected_column_count, selected_column_mean, selected_column_median
                      , selected_column_nunique , selected_column_mode , selected_column_std , selected_column_prod , selected_column_idxmax , selected_column_idxmin):
    if (data.map(lambda x: x != 0)).any().any():
        if(selected_column_max):
            one_data = data[selected_column_max].max()
            columns = selected_column_max
        elif(selected_column_min):
            one_data= data[selected_column_min].min()
            columns = selected_column_min
        elif(selected_column_sum):
            one_data= data[selected_column_sum].sum()
            columns = selected_column_sum
        elif(selected_column_count):
            one_data= data[selected_column_count].count()
            columns = selected_column_count
        elif(selected_column_mean):
            one_data= data[selected_column_mean].mean()
            columns = selected_column_mean
        elif(selected_column_median):
            one_data= data[selected_column_median].median()
            columns = selected_column_median
        elif(selected_column_nunique ):
            one_data= data[selected_column_nunique].nunique() 
            columns = selected_column_nunique

        elif(selected_column_mode ):
            mode_result = data[selected_column_mode].mode()
            if len(mode_result) > 1:
              one_data =  ', '.join(map(str, mode_result))
            else:
                one_data = mode_result[0]
            columns = selected_column_mode
        elif(selected_column_std ):
            one_data= data[selected_column_std].std() 
            columns = selected_column_std
        elif(selected_column_prod ):
            one_data= data[selected_column_prod].prod() 
            columns = selected_column_prod
        elif(selected_column_idxmax ):
            one_data= data[selected_column_idxmax].idxmax() 
            columns = selected_column_idxmax
        elif(selected_column_idxmin):
            one_data= data[selected_column_idxmin].idxmin() 
            columns = selected_column_idxmin
    return  columns ,one_data
def Table_data_analysis(data, SQL_query , selected_column_name , selected_column_1_operation , selected_operation , selected_column_2_operation, selected_column_describe,selected_column_drop
                        , selected_column_dropna , selected_column_head , selected_column_tail , selected_column_sort_type , selected_column_sort , current_column_name , new_column_name, 
                        selected_column_pivot_index,selected_column_pivot_column , selected_column_pivot_value , selected_column_fillna ,selected_column_fillna_text, selected_column_operations_on_columns , 
                        selected_operation_on_column , selected_operation_on_column_number, selected_column_replace ,old_value_of_replace ,new_value_of_replace , selected_column_duplicated , duplicate_occurrence ,
                        selected_column_drop_duplicates , drop_duplicate_occurrence , selected_column_cross_tabulation_row , selected_column_cross_tabulation_column , selected_column_stacking_and_unstacking , 
                        selected_column_cumulative_sum , selected_column_cumulative_product , selected_column_cumulative_maximum , selected_column_cumulative_minimum , selected_column_column_update_condition , 
                        column_update_condition_text , selected_column_column_update_set , column_update_set_text , selected_column_delete_row_condition , delete_row_condition_text , selected_column_rename_column , 
                        selected_column_rename_column_new_name , selected_column_column_copy, selected_column_column_copy_name , selected_Column_GroupBy , selected_Column_Aggregation , aggregation_Method):
    if (SQL_query):
        tbl = pd.DataFrame(data)
        conn = sqlite3.connect(':memory:')
        # Write the DataFrame to a table in the database
        tbl.to_sql('tbl', conn, index=False, if_exists='replace')
        # SQL-like update query
        input_query = SQL_query
        # Execute the update query using the SQLite connection
        result = conn.execute(input_query)
        #IF for select query only:
        if input_query.startswith("s") or input_query.startswith("S"):
            selected_data = pd.DataFrame(result.fetchall(), columns=tbl.columns)
            return selected_data
        # Read the DataFrame back from the database but not for select query
        show_tbl = pd.read_sql('SELECT * FROM tbl', conn)
        return show_tbl
    elif(selected_column_name and selected_column_1_operation and selected_operation and selected_column_2_operation):
        tbl = pd.DataFrame(data)
        if(selected_operation == "Division"):
            tbl[selected_column_name] = tbl[selected_column_1_operation] / tbl[selected_column_2_operation]
        elif(selected_operation == "Multiplication"):
            tbl[selected_column_name] = tbl[selected_column_1_operation] * tbl[selected_column_2_operation]
        elif(selected_operation == "Addition"):
            tbl[selected_column_name] = tbl[selected_column_1_operation] + tbl[selected_column_2_operation]
        elif(selected_operation == "Subtraction"):
            tbl[selected_column_name] = tbl[selected_column_1_operation] - tbl[selected_column_2_operation]
        return tbl
    elif(selected_column_describe):
        tbl = pd.DataFrame(data)
        if(selected_column_describe=="all"):
            result = tbl.describe()
            #result[''] = result.index
            #column_order = [''] + [col for col in result.columns if col != '']
            #result = result[column_order]
        else:
            result = tbl[selected_column_describe].describe()
            result = result.to_frame()
            #result[''] = result.index
            #column_order = [''] + [col for col in result.columns if col != '']
            #result = result[column_order]
        return result
    elif(selected_column_drop):
        tbl = pd.DataFrame(data)
        tbl.drop(selected_column_drop, axis=1, inplace=True)
        return tbl
    elif(selected_column_dropna):
        tbl = pd.DataFrame(data)
        if(selected_column_dropna=="all"):
            dropna = tbl.dropna()
        else:
            dropna = tbl.dropna(subset=[selected_column_dropna])
        return dropna
    elif(selected_column_head):
        tbl = pd.DataFrame(data)
        selected_column_head = int(selected_column_head)
        head = tbl.head(selected_column_head)
        return head
    elif(selected_column_tail):
        selected_column_tail = int(selected_column_tail)
        tbl = pd.DataFrame(data)
        tail = tbl.tail(selected_column_tail)
        return tail
    elif(selected_column_sort_type and selected_column_sort):
        tbl = pd.DataFrame(data)
        if(selected_column_sort_type == "ascending"):
            sort = tbl.sort_values(by=selected_column_sort)
        elif(selected_column_sort_type == "descending"):
            sort = tbl.sort_values(by=selected_column_sort, ascending=False)
        return sort
    elif(current_column_name and new_column_name):
        tbl = pd.DataFrame(data)
        rename = tbl.rename(columns={current_column_name: new_column_name})
        return rename
    #start
    elif(selected_column_pivot_index and selected_column_pivot_column  and  selected_column_pivot_value ):
        tbl = pd.DataFrame(data)
        pivot = tbl.pivot(index=selected_column_pivot_index, columns=selected_column_pivot_column, values=selected_column_pivot_value)
        return pivot
    elif(selected_column_fillna and selected_column_fillna_text):
        selected_column_fillna_text = convert_to_integer_or_string(selected_column_fillna_text)
        #test it
        tbl = pd.DataFrame(data)
        if(selected_column_fillna=="all"):
            fillna = tbl.fillna()
        else:
            fillna = tbl[selected_column_fillna].fillna(selected_column_fillna_text)
        return fillna
    elif (selected_column_operations_on_columns and selected_operation_on_column and selected_operation_on_column_number):
        selected_operation_on_column_number = convert_to_integer_or_string(selected_operation_on_column_number)
        tbl = pd.DataFrame(data)
        if(selected_operation_on_column == "Division"):
            tbl[selected_column_operations_on_columns] = tbl[selected_column_operations_on_columns] / selected_operation_on_column_number
        elif(selected_operation_on_column == "Multiplication"):
            tbl[selected_column_operations_on_columns] = tbl[selected_column_operations_on_columns] * selected_operation_on_column_number
        elif(selected_operation_on_column == "Addition"):
            tbl[selected_column_operations_on_columns] = tbl[selected_column_operations_on_columns] + selected_operation_on_column_number
        elif(selected_operation_on_column == "Subtraction"):
            tbl[selected_column_operations_on_columns] = tbl[selected_column_operations_on_columns] - selected_operation_on_column_number
        return tbl
    elif(selected_column_replace and old_value_of_replace and new_value_of_replace):
        old_value_of_replace = convert_to_integer_or_string(old_value_of_replace)
        new_value_of_replace = convert_to_integer_or_string(new_value_of_replace)
        tbl = pd.DataFrame(data)
        tbl[selected_column_replace] = tbl[selected_column_replace].replace(old_value_of_replace, new_value_of_replace)
        return tbl
    elif(selected_column_duplicated and duplicate_occurrence):
        tbl = pd.DataFrame(data)
        if (duplicate_occurrence == "false"):
            duplicate_occurrence = False
        if (selected_column_duplicated == "all"):
            duplicate = tbl[tbl.duplicated(keep=duplicate_occurrence)]
        else:
            duplicate = tbl[tbl[selected_column_duplicated].duplicated(keep=duplicate_occurrence)]
        return duplicate
    elif(selected_column_drop_duplicates and drop_duplicate_occurrence):
        tbl = pd.DataFrame(data)
        if (drop_duplicate_occurrence == "false"):
            drop_duplicate_occurrence = False
        if (selected_column_drop_duplicates == "all"):
            drop_duplicate = tbl.drop_duplicates(keep=drop_duplicate_occurrence)
        else:
            drop_duplicate = tbl.drop_duplicates(subset=[selected_column_drop_duplicates], keep=drop_duplicate_occurrence)
        return drop_duplicate
    elif(selected_column_cross_tabulation_row and selected_column_cross_tabulation_column):
        tbl = pd.DataFrame(data)
        cross_tab = pd.crosstab(tbl[selected_column_cross_tabulation_row], tbl[selected_column_cross_tabulation_column])
        return cross_tab
    elif(selected_column_stacking_and_unstacking):
        tbl = pd.DataFrame(data)
        if (selected_column_stacking_and_unstacking == "stack"):
            stacking_unstacking = tbl.stack()
        elif(selected_column_stacking_and_unstacking == "unstack"):
            stacking_unstacking = tbl.unstack()
        stacking_unstacking = stacking_unstacking.to_frame()
        return stacking_unstacking
    elif(selected_column_cumulative_sum):
        tbl = pd.DataFrame(data)
        tbl = remove_str_columns_from_Dataframe(tbl)
        if(selected_column_cumulative_sum=="all"):
            cumulative_sum = tbl.cumsum()
        else:
            cumulative_sum = tbl[selected_column_cumulative_sum].cumsum()
            cumulative_sum = cumulative_sum.to_frame()
        return cumulative_sum
    elif(selected_column_cumulative_product):
        tbl = pd.DataFrame(data)
        tbl = remove_str_columns_from_Dataframe(tbl)
        if(selected_column_cumulative_product=="all"):
            cumulative_product = tbl.cumprod()
        else:
            cumulative_product = tbl[selected_column_cumulative_product].cumprod()
            cumulative_product = cumulative_product.to_frame()
        return cumulative_product
    # ,  ,
    elif(selected_column_cumulative_maximum):
        tbl = pd.DataFrame(data)
        tbl = remove_str_columns_from_Dataframe(tbl)
        if(selected_column_cumulative_maximum=="all"):
            cumulative_maximum = tbl.cummax()
        else:
            cumulative_maximum = tbl[selected_column_cumulative_maximum].cummax()
            cumulative_maximum = cumulative_maximum.to_frame()
        return cumulative_maximum
    elif(selected_column_cumulative_minimum):
        tbl = pd.DataFrame(data)
        tbl = remove_str_columns_from_Dataframe(tbl)
        if(selected_column_cumulative_minimum=="all"):
            cumulative_minimum = tbl.cummin()
        else:
            cumulative_minimum = tbl[selected_column_cumulative_minimum].cummin()
            cumulative_minimum = cumulative_minimum.to_frame()
        return cumulative_minimum
    elif(selected_column_column_update_condition and column_update_condition_text and selected_column_column_update_set and column_update_set_text):
        tbl = pd.DataFrame(data)
        column_update_condition_text = convert_to_integer_or_string(column_update_condition_text)
        column_update_set_text = convert_to_integer_or_string(column_update_set_text)
        if (selected_column_column_update_condition == "index"):
            tbl.loc[tbl.index == column_update_condition_text, selected_column_column_update_set] = column_update_set_text
        else:
            tbl.loc[tbl[selected_column_column_update_condition] == column_update_condition_text, selected_column_column_update_set] = column_update_set_text
        return tbl
    elif(selected_column_delete_row_condition and delete_row_condition_text):
        tbl = pd.DataFrame(data)
        delete_row_condition_text = convert_to_integer_or_string(delete_row_condition_text)
        if (selected_column_delete_row_condition == "index"):
            tbl = tbl.drop(delete_row_condition_text)
        else:
            condition = (tbl[selected_column_delete_row_condition] == delete_row_condition_text)
            tbl = tbl[~condition]
        return tbl
    elif(selected_column_rename_column and selected_column_rename_column_new_name):
        tbl = pd.DataFrame(data)
        tbl.rename(columns={selected_column_rename_column: selected_column_rename_column_new_name}, inplace=True)
        return tbl
    elif(selected_column_column_copy and selected_column_column_copy_name):
        tbl = pd.DataFrame(data)
        selected_columns = [selected_column_column_copy]
        tbl[selected_column_column_copy_name] = tbl[selected_columns].copy()
        return tbl
    elif(selected_Column_GroupBy and selected_Column_Aggregation and aggregation_Method):
        tbl = pd.DataFrame(data)
        if (aggregation_Method=="mean" or aggregation_Method=="median" or aggregation_Method=="std" or aggregation_Method=="var"):
            tbl = remove_str_columns_from_Dataframe(tbl)
        if (selected_Column_Aggregation == "all"):
            result = tbl.groupby(selected_Column_GroupBy).agg([aggregation_Method])
        else:
            result = tbl.groupby(selected_Column_GroupBy)[selected_Column_GroupBy].agg([aggregation_Method])
        return result

def admin_read_unread_plot(read , unread, colors):
    if read == 0 and unread == 0  :
        return None
    else:
        read_color = colors[0]
        unread_color = colors[1]
        text_color = colors[2]
        sizes = [read, unread]  # Define your sizes here
        labels = ['read', 'unread']
        colors = [read_color, unread_color]
    
        # Create a pie chart
        plt.figure(figsize=(6, 6), facecolor='none')
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors, textprops={'color': text_color})
        plt.axis('equal')
        plt.title('Pie Chart of read and unread', color = text_color)
    
        # Convert the plot to an image
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        img_base64 = base64.b64encode(img.getvalue()).decode()
    
        # Embed the image in the HTML output
        return img_base64