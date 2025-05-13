
import pandas as pd
from io import StringIO
from functools import wraps
from flask import Flask, flash, render_template, request, jsonify, redirect,url_for,make_response, session, send_from_directory, abort,send_file
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
import time
import utils
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx','xls'}

app.config['SECRET_KEY'] = 'z5d54d54d51d15#dddddddddd'
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
app.config['SESSION_COOKIE_NAME'] = 'my_session'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def decrypted_cookies(cookies_name):
    # Get the 'username' cookie
    get_cookie_name = request.cookies.get(cookies_name)
    
    if get_cookie_name is not None:
            # Try to decrypt the cookie
            decrypted_data = serializer.loads(get_cookie_name)
            
            # If decryption is successful, decrypted_data will contain the original data
            return decrypted_data
        
    else:
        return ""


@app.route('/analysis' , methods=['GET', 'POST'])
def analysis_data():
    data_analysis , second_data = "" , ""
    excel_file_path = decrypted_cookies("path")
    selected_sheet = decrypted_cookies("sheet")
    if (excel_file_path == None or selected_sheet == None or excel_file_path == '' or selected_sheet == ''):
            return redirect(url_for('upload_file'))
    
    
    if request.method == 'POST':
        #one_data
        selected_column_max = request.form.get('selected_column_max', '')
        selected_column_min = request.form.get('selected_column_min', '')
        selected_column_sum = request.form.get('selected_column_sum', '')
        selected_column_count = request.form.get('selected_column_count', '')
        selected_column_mean = request.form.get('selected_column_mean', '')
        selected_column_median = request.form.get('selected_column_median', '')
        selected_column_nunique = request.form.get('selected_column_nunique', '')
        selected_column_mode = request.form.get('selected_column_mode', '')
        selected_column_std = request.form.get('selected_column_std', '')
        selected_column_prod = request.form.get('selected_column_prod', '')
        selected_column_idxmax = request.form.get('selected_column_idxmax', '')
        selected_column_idxmin = request.form.get('selected_column_idxmin', '')
        
        #table_data
        selected_column_name = request.form.get('selected_column_name', '')
        selected_column_1_operation = request.form.get('selected_column(1)_operation', '')
        selected_operation = request.form.get('selected_operation', '')
        selected_column_2_operation = request.form.get('selected_column(2)_operation', '')
        selected_column_describe = request.form.get('selected_column_describe', '')
        selected_column_drop = request.form.get('selected_column_drop', '')
        selected_column_dropna = request.form.get('selected_column_dropna', '')
        selected_column_head = request.form.get('selected_column_head', '')
        selected_column_tail = request.form.get('selected_column_tail', '')
        selected_column_sort_type = request.form.get('selected_column_sort_type', '')
        selected_column_sort = request.form.get('selected_column_sort', '')
        current_column_name = request.form.get('current_column_name', '')
        new_column_name = request.form.get('new_column_name', '')
        # start
       
        selected_column_pivot_index = request.form.get('selected_column_pivot_index', '')
        selected_column_pivot_column = request.form.get('selected_column_pivot_column', '')
        selected_column_pivot_value = request.form.get('selected_column_pivot_value', '')
        selected_column_fillna = request.form.get('selected_column_fillna', '')
        selected_column_fillna_text = request.form.get('selected_column_fillna_text', '')
        selected_column_operations_on_columns = request.form.get('selected_column_operations_on_columns', '')
        selected_operation_on_column = request.form.get('selected_operation_on_column', '')
        selected_operation_on_column_number = request.form.get('selected_operation_on_column_number', '')
        selected_column_replace = request.form.get('selected_column_replace', '')
        old_value_of_replace = request.form.get('old_value_of_replace', '')
        new_value_of_replace = request.form.get('new_value_of_replace', '')
        selected_column_duplicated = request.form.get('selected_column_duplicated', '')
        duplicate_occurrence = request.form.get('duplicate_occurrence', '')
        selected_column_drop_duplicates = request.form.get('selected_column_drop_duplicates', '')
        drop_duplicate_occurrence = request.form.get('drop_duplicate_occurrence', '')
        selected_column_cross_tabulation_row = request.form.get('selected_column_cross_tabulation_row', '')
        selected_column_cross_tabulation_column = request.form.get('selected_column_cross_tabulation_column', '')
        selected_column_stacking_and_unstacking = request.form.get('selected_column_stacking_and_unstacking', '')
        selected_column_cumulative_sum = request.form.get('selected_column_cumulative_sum', '')
        selected_column_cumulative_product = request.form.get('selected_column_cumulative_product', '')
        selected_column_cumulative_maximum = request.form.get('selected_column_cumulative_maximum', '')
        selected_column_cumulative_minimum = request.form.get('selected_column_cumulative_minimum', '')
        selected_column_column_update_condition = request.form.get('selected_column_column_update_condition', '')
        column_update_condition_text = request.form.get('column_update_condition_text', '')
        selected_column_column_update_set = request.form.get('selected_column_column_update_set', '')
        column_update_set_text = request.form.get('column_update_set_text', '')
        selected_column_delete_row_condition = request.form.get('selected_column_delete_row_condition', '')
        delete_row_condition_text = request.form.get('delete_row_condition_text', '')
        selected_column_rename_column = request.form.get('selected_column_rename_column', '')
        selected_column_rename_column_new_name = request.form.get('selected_column_rename_column_new_name', '')
        selected_column_column_copy = request.form.get('selected_column_column_copy', '')
        selected_column_column_copy_name = request.form.get('selected_column_column_copy_name', '')
        selected_Column_GroupBy = request.form.get('selected_Column_GroupBy', '')
        selected_Column_Aggregation = request.form.get('selected_Column_Aggregation', '')
        aggregation_Method = request.form.get('aggregation_Method', '')
        
        #continue
        file_analysis = request.files.get('file' , '')
        selected_sheet_analysis = request.form.get('sheet','')
        #The SQL Query 
        SQL_query= request.form.get('SQL_query', '')
        #join
        left_columns_join = request.form.get('left_columns_join', '')
        right_columns_join= request.form.get('right_columns_join' , '')
        join_type = request.form.get('join_type', '')
        Convert_to_Excel = request.form.get('Convert_to_Excel', '')
        replace_dataset = request.form.get('replace_dataset', '')

        excel_file_path = decrypted_cookies("path")
        selected_sheet = decrypted_cookies("sheet")
        data = utils.Show_data_file(excel_file_path, selected_sheet)
        columns = utils.extract_column_names(excel_file_path, selected_sheet)
                
        if (selected_column_max or selected_column_min or selected_column_sum or selected_column_count 
            or selected_column_mean or selected_column_median or selected_column_nunique or selected_column_mode or selected_column_std 
            or selected_column_prod or selected_column_idxmax or selected_column_idxmin):
            one_data_analysis_name, one_data_analysis_value = utils.One_data_analysis(data , selected_column_max, selected_column_min , selected_column_sum, selected_column_count, selected_column_mean, selected_column_median
                                                                                      , selected_column_nunique , selected_column_mode , selected_column_std , selected_column_prod , selected_column_idxmax , selected_column_idxmin)
            return render_template('analysis.html', data = data, columns = columns, one_data_analysis_name=one_data_analysis_name   ,one_data_analysis_value = one_data_analysis_value )
#selected_Column_GroupBy or selected_Column_Aggregation or aggregation_Method
        elif (SQL_query or selected_column_name or selected_column_1_operation or selected_operation or selected_column_2_operation or selected_column_describe or selected_column_drop
                      or selected_column_dropna or selected_column_head or selected_column_tail or selected_column_sort_type or selected_column_sort or current_column_name or new_column_name
                      or selected_column_pivot_index or selected_column_pivot_column or selected_column_pivot_value or selected_column_fillna or selected_column_fillna_text or selected_column_operations_on_columns 
                      or selected_operation_on_column or selected_operation_on_column_number or selected_column_replace or old_value_of_replace or new_value_of_replace or selected_column_duplicated or duplicate_occurrence 
                      or selected_column_drop_duplicates or drop_duplicate_occurrence or selected_column_cross_tabulation_row or selected_column_cross_tabulation_column or selected_column_stacking_and_unstacking or selected_column_cumulative_sum 
                      or selected_column_cumulative_product or selected_column_cumulative_maximum or selected_column_cumulative_minimum or selected_column_column_update_condition or column_update_condition_text or selected_column_column_update_set 
                      or column_update_set_text or selected_column_delete_row_condition or delete_row_condition_text or selected_column_rename_column or selected_column_rename_column_new_name or selected_column_column_copy or selected_column_column_copy_name
                      or selected_Column_GroupBy or selected_Column_Aggregation or aggregation_Method):
                # apply here data 1 to data
            try:
                result = utils.Table_data_analysis(data, SQL_query , selected_column_name , selected_column_1_operation , selected_operation , selected_column_2_operation, selected_column_describe, selected_column_drop 
                                                   ,selected_column_dropna , selected_column_head , selected_column_tail , selected_column_sort_type , selected_column_sort , current_column_name , new_column_name , 
                                                   selected_column_pivot_index, selected_column_pivot_column , selected_column_pivot_value , selected_column_fillna ,selected_column_fillna_text, selected_column_operations_on_columns , 
                                                   selected_operation_on_column , selected_operation_on_column_number,selected_column_replace ,old_value_of_replace , new_value_of_replace , selected_column_duplicated , duplicate_occurrence , 
                                                   selected_column_drop_duplicates , drop_duplicate_occurrence , selected_column_cross_tabulation_row , selected_column_cross_tabulation_column , selected_column_stacking_and_unstacking , 
                                                   selected_column_cumulative_sum , selected_column_cumulative_product , selected_column_cumulative_maximum , selected_column_cumulative_minimum , selected_column_column_update_condition , 
                                                   column_update_condition_text , selected_column_column_update_set , column_update_set_text, selected_column_delete_row_condition , delete_row_condition_text , selected_column_rename_column , 
                                                   selected_column_rename_column_new_name , selected_column_column_copy,  selected_column_column_copy_name , selected_Column_GroupBy , selected_Column_Aggregation , aggregation_Method )
                second_data = 1
                return render_template('analysis.html',data =data, data1 = result , columns = columns, second_data=second_data)
            except Exception as e:
                    return render_template("error-message.html" , error = e)


        elif file_analysis and allowed_file(file_analysis.filename):
            filename = secure_filename(file_analysis.filename)
            if filename.endswith('.xls'):
                filename = filename.replace('.xls', '.xlsx')
                unique_number = int(time.time() * 1000)  # Convert to milliseconds
                excel_file_path_analysis = f"uploads/{unique_number}_{filename}"
                file_analysis.save(excel_file_path_analysis)
                new_file = FileStorage(stream=open(excel_file_path_analysis, 'rb'), filename=filename, content_type=file_analysis.content_type)
                file_analysis = new_file
            else:    
                unique_number = int(time.time() * 1000) # Convert to milliseconds
                excel_file_path_analysis = f"uploads/{unique_number}_{filename}"  # Store the uploaded file in a directory named 'uploads'
                file_analysis.save(excel_file_path_analysis)
                new_file = FileStorage(stream=open(excel_file_path_analysis, 'rb'), filename=filename, content_type=file_analysis.content_type)
                file_analysis = new_file

            sheet_names_analysis = utils.extract_sheet_names(excel_file_path_analysis)

            excel_file_path_analysis_cookie = serializer.dumps(excel_file_path_analysis)
            sheet_names_analysis_cookie = serializer.dumps(sheet_names_analysis)
            set_cookie = make_response(render_template('analysis.html',data=data, sheet_names=sheet_names_analysis, 
                                                       excel_file_path=excel_file_path_analysis))
            set_cookie.set_cookie('excel_file_analysis' , excel_file_path_analysis_cookie)
            set_cookie.set_cookie('sheet_analysis' , sheet_names_analysis_cookie)
            return set_cookie


        elif selected_sheet_analysis:
            excel_file_path_analysis = decrypted_cookies("excel_file_analysis")
            sheet_names_analysis = decrypted_cookies("sheet_analysis")
            data_analysis = utils.Show_data_file(excel_file_path_analysis, selected_sheet_analysis)
            second_data = 1
            join_show = 1
            columns_analysis = utils.extract_column_names(excel_file_path_analysis,selected_sheet_analysis)
            
            selected_sheet_analysis_cookie = serializer.dumps(selected_sheet_analysis)
            set_cookie = make_response(render_template ('analysis.html',data =data, data1 = data_analysis , second_data=second_data, join_show= join_show ,
                                     columns_analysis=columns_analysis, columns= columns))
            set_cookie.set_cookie('selected_sheet_analysis_cookie' , selected_sheet_analysis_cookie)
            #session['sheet_analysis'] = selected_sheet_analysis
            return set_cookie
            
        elif right_columns_join and left_columns_join and join_type:
            excel_file_path_analysis = decrypted_cookies("excel_file_analysis")
            selected_sheet_analysis_cookie = decrypted_cookies("selected_sheet_analysis_cookie")
            data_analysis = utils.Show_data_file(excel_file_path_analysis, selected_sheet_analysis_cookie)
            data, data_analysis , right_columns_join , left_columns_join, join_type
            columns_analysis = utils.extract_column_names(excel_file_path_analysis,selected_sheet_analysis_cookie)
            second_data = 1
            data = pd.merge(data, data_analysis, left_on=left_columns_join, right_on=right_columns_join, how=join_type)
           
            return render_template('analysis.html', data =data, columns = columns,columns_analysis=columns_analysis,
                            data1 = data_analysis, second_data=second_data )
        elif Convert_to_Excel:
            try:
                processed_data = utils.process_html_data(Convert_to_Excel)
                html_io = StringIO(processed_data)
                df = pd.read_html(html_io)[0]
                df = df.iloc[:, 1:]
                # Parse the JSON data
                data1 = pd.DataFrame(df)
                # Create a new Excel workbook and save the DataFrame to it
            
                
                unique_number = int(time.time() * 1000)
                filename = f"uploads/{unique_number}_replace_dataset1.xlsx"
                excel_filename = os.path.join('uploads', filename)
                data1.to_excel(filename, index=False)
                #workbook.save(filename)
                auto_selected_sheet = utils.auto_selected_sheet_name(filename)
                columns_replace_dataset = utils.extract_column_names(filename, auto_selected_sheet)
                
                serialized_filename = serializer.dumps(filename)
                serialized_auto_selected_sheet = serializer.dumps(auto_selected_sheet)
                serialized_columns_replace_dataset = serializer.dumps(columns_replace_dataset)
                
                set_cookie = make_response(redirect('/analysis'))
                set_cookie.set_cookie('path' , serialized_filename, max_age=3600)
                set_cookie.set_cookie('sheet' , serialized_auto_selected_sheet, max_age=3600)
                set_cookie.set_cookie('columns' , serialized_columns_replace_dataset, max_age=3600)
                return set_cookie
            except Exception as e:
                return render_template("error-message.html" , error = e)
                
        elif replace_dataset:
            processed_data = utils.process_html_data(replace_dataset)
            html_io = StringIO(processed_data)
            df = pd.read_html(html_io)[0]
            df = df.iloc[:, 1:]
            for col in df.columns:
                if isinstance(col, tuple) and col[0].startswith('Unnamed'):
                    # Handle the case where the column name is a tuple
                    df.rename(columns={col: ('', col[1])}, inplace=True)
                elif isinstance(col, str) and col.startswith('Unnamed'):
                    # Handle the case where the column name is a string
                    df.rename(columns={col: ''}, inplace=True)
            data1 = pd.DataFrame(df)
            return render_template('analysis.html',data = data1, columns = columns )


    excel_file_path_analysis = decrypted_cookies("excel_file_analysis")
    selected_sheet_analysis = decrypted_cookies("selected_sheet_analysis_cookie")
    if (selected_sheet_analysis != '' and excel_file_path_analysis != ''):
            excel_file_path = decrypted_cookies("path")
            selected_sheet = decrypted_cookies("sheet")
            columns = decrypted_cookies("columns")
            data = utils.Show_data_file(excel_file_path, selected_sheet) 
            data_analysis = utils.Show_data_file(excel_file_path_analysis, selected_sheet_analysis)
            columns_analysis = utils.extract_column_names(excel_file_path_analysis,selected_sheet_analysis)
            second_data = 1
            return render_template('analysis.html', data =data, columns = columns ,columns_analysis=columns_analysis,
                            data1 = data_analysis, second_data=second_data )
    
    excel_file_path = decrypted_cookies("path")
    selected_sheet = decrypted_cookies("sheet")
    columns = decrypted_cookies("columns")
    data = utils.Show_data_file(excel_file_path, selected_sheet)
    return render_template('analysis.html', data =data, columns = columns)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    try:
        if request.method == 'POST':
            file = request.files.get('file' , '')
            selected_sheet = request.form.get('sheet','')
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                if filename.endswith('.xls'):
                    filename = filename.replace('.xls', '.xlsx')
                    unique_number = int(time.time() * 1000)  # Convert to milliseconds
                    excel_file_path = f"uploads/{unique_number}_{filename}"
                    file.save(excel_file_path)
                    new_file = FileStorage(stream=open(excel_file_path, 'rb'), filename=filename, content_type=file.content_type)
                    file = new_file
                else:    
                    unique_number = int(time.time() * 1000) # Convert to milliseconds
                    excel_file_path = f"uploads/{unique_number}_{filename}"  # Store the uploaded file in a directory named 'uploads'
                    file.save(excel_file_path)
                    new_file = FileStorage(stream=open(excel_file_path, 'rb'), filename=filename, content_type=file.content_type)
                    file = new_file
                sheet_names = utils.extract_sheet_names(excel_file_path)
                session['sheet_name'] = sheet_names
                session['path'] = excel_file_path
                return render_template('upload.html', sheet_names=sheet_names, excel_file_path=excel_file_path)
            elif file and not allowed_file(file.filename):
                return "file invalied"
            if selected_sheet:
                excel_file_path = session.get('path', '')
                sheet_names = session.get('sheet_name', '')
                session.pop('path' , '')
                session.pop('sheet_name' , '')
                columns = utils.extract_column_names(excel_file_path, selected_sheet)
                x_axis,y_axis, z_axis = "","",""

                serialized_x_axis = serializer.dumps(x_axis)
                serialized_y_axis = serializer.dumps(y_axis)
                serialized_z_axis = serializer.dumps(z_axis)
                serialized_excel_path = serializer.dumps(excel_file_path)
                serialized_excel_selected_sheet = serializer.dumps(selected_sheet)
                serialized_excel_columns = serializer.dumps(columns)
                set_cookie = make_response(render_template('upload.html',columns=columns, sheet_names=sheet_names))
                set_cookie.set_cookie('x_axis' , serialized_x_axis)
                set_cookie.set_cookie('y_axis' , serialized_y_axis)
                set_cookie.set_cookie('z_axis' , serialized_z_axis)
                set_cookie.set_cookie('path' , serialized_excel_path, max_age=3600)
                set_cookie.set_cookie('sheet' , serialized_excel_selected_sheet, max_age=3600)
                set_cookie.set_cookie('columns' , serialized_excel_columns, max_age=3600)
                return set_cookie
    except Exception as e:
                return render_template("error-message.html" , error = e)

         
    return render_template('upload.html')

if __name__ == "__main__":
    #, host='192.168.1.108, Command = sudo ufw allow 5001'
    app.run(port = 5000 , debug=True )
    
