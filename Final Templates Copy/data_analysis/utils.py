import pandas as pd
from flask import Flask, render_template
import time
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
    

def remove_str_columns_from_Dataframe(data):
    str_columns = data.select_dtypes(include='object').columns
    # Drop columns with string data type
    data_numeric = data.drop(columns=str_columns)
    return data_numeric

def process_html_data(Convert_to_Excel):
    # Replace this with your actual data processing logic
    processed_data = f"Processed HTML data: {Convert_to_Excel}"
    return processed_data


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
        else:
            result = tbl[selected_column_describe].describe()
            result = result.to_frame()
           
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
