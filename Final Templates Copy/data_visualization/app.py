import matplotlib
from werkzeug.datastructures import FileStorage
matplotlib.use('Agg')
from flask import Flask, render_template, request, jsonify, redirect,url_for,make_response, session, send_from_directory, abort,send_file
from itsdangerous import URLSafeTimedSerializer
import time
from bokeh.resources import INLINE
import utils
from werkzeug.utils import secure_filename


app = Flask(__name__)
ALLOWED_EXTENSIONS = {'xlsx','xls'}
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'zishani'
app.config['SESSION_TYPE'] = 'filesystem'


app.config['SECRET_KEY'] = 'z5d54d54d51d15#dddddddddd'
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
     return redirect(url_for('upload_file'))

@app.route('/upload_file', methods=['GET', 'POST'])
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

@app.route('/columns', methods=['GET', 'POST'])
def columns():
    excel_file_path = decrypted_cookies("path")
    selected_sheet = decrypted_cookies("sheet")
    if (excel_file_path == None or selected_sheet == None or excel_file_path == '' or selected_sheet == ''):
            return redirect(url_for('upload_file'))
    color_name = ['aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'black', 'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow', 'grey', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgreen', 'lightgrey', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'loralwhite', 'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'rebeccapurple', 'red', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellow', 'yellowgreen']
    columns = decrypted_cookies("columns")
    if request.method == 'POST':
        
        text_02 = request.form.get('text_02', '')
        position_label = request.form.get('position_label', '')
        Title_of_label = request.form.get('Title_of_label', '')
        legend_title_size = request.form.get('legend_title_size', '')
        legend_title_weight = request.form.get('legend_title_weight', '')
        legend_Title_color = request.form.get('legend_Title_color', '')
        legend_text_color = request.form.get('legend_text_color', '')
        legend_opacity = request.form.get('legend_opacity', '')
        legend_box_style = request.form.get('legend_box_style', '')
        legend_box_size = request.form.get('legend_box_size', '')
        face_color_legend = request.form.get('face_color_legend', '')
        edge_color_legend = request.form.get('edge_color_legend', '')
        legend_line_style = request.form.get('legend_line_style', '')
        legend_line_width = request.form.get('legend_line_width', '')
        layout_axis_spines = request.form.get('layout_axis_spines', '')
        Plot_bg_color = request.form.get('Plot_bg_color', '')
        layout_theme_style = request.form.get('layout_theme_style', '')
        layout_xtick_color = request.form.get('layout_xtick_color', '')
        layout_ytick_color = request.form.get('layout_ytick_color', '')
        layout_xlabel_title = request.form.get('layout_xlabel_title', '')
        layout_xlabel_color = request.form.get('layout_xlabel_color', '')
        layout_xlabel_background_color = request.form.get('layout_xlabel_background_color', '')
        layout_xlabel_border_color = request.form.get('layout_xlabel_border_color', '')
        layout_xlabel_box_style = request.form.get('layout_xlabel_box_style', '')
        layout_xlabel_Box_Style_pad = request.form.get('layout_xlabel_Box_Style_pad', '')
        layout_ylabel_title = request.form.get('layout_ylabel_title', '')
        layout_ylabel_color = request.form.get('layout_ylabel_color', '')
        layout_ylabel_background_color = request.form.get('layout_ylabel_background_color', '')
        layout_ylabel_border_color = request.form.get('layout_ylabel_border_color', '')
        layout_ylabel_box_style = request.form.get('layout_ylabel_box_style', '')
        layout_ylabel_Box_Style_pad = request.form.get('layout_ylabel_Box_Style_pad', '')
        layout_plot_title = request.form.get('layout_plot_title', '')
        layout_title_color = request.form.get('layout_title_color', '')
        layout_title_background_color = request.form.get('layout_title_background_color', '')
        layout_title_border_color = request.form.get('layout_title_border_color', '')
        layout_title_box_style = request.form.get('layout_title_box_style', '')
        layout_title_Box_Style_pad = request.form.get('layout_title_Box_Style_pad', '')
        marker_color = request.form.get('marker_color', '')
        marker_size = request.form.get('marker_size', '')
        marker_line_width = request.form.get('marker_line_width', '')
        marker_categorization = request.form.get('marker_categorization', '')
        marker_palette = request.form.get('marker_palette', '')
        marker_alpha = request.form.get('marker_alpha', '')
        marker_edge_colors = request.form.get('marker_edge_colors', '')
        arr_set = [position_label, Title_of_label, legend_title_size, legend_title_weight, legend_Title_color, legend_text_color, legend_opacity, legend_box_style, legend_box_size, face_color_legend, edge_color_legend, legend_line_style, legend_line_width, layout_axis_spines,Plot_bg_color, layout_theme_style, layout_xtick_color, layout_ytick_color, layout_xlabel_title, layout_xlabel_color, layout_xlabel_background_color, layout_xlabel_border_color, layout_xlabel_box_style, layout_xlabel_Box_Style_pad, layout_ylabel_title, layout_ylabel_color, layout_ylabel_background_color, layout_ylabel_border_color, layout_ylabel_box_style, layout_ylabel_Box_Style_pad, layout_plot_title, layout_title_color, layout_title_background_color, layout_title_border_color, layout_title_box_style, layout_title_Box_Style_pad, marker_color, marker_size,marker_line_width, marker_categorization, marker_palette, marker_alpha, marker_edge_colors]
        x_axis = decrypted_cookies("x_axis")
        y_axis = decrypted_cookies("y_axis")
        z_axis = decrypted_cookies("z_axis")
        excel_file_path = decrypted_cookies("path")
        selected_sheet = decrypted_cookies("sheet")
        if (excel_file_path == None or selected_sheet == None or excel_file_path == '' or selected_sheet == ''):
                return redirect(url_for('upload_file'))
        if columns:
            if (utils.is_array(x_axis) or utils.is_array(y_axis) or utils.is_array(z_axis)):
                    if (len(x_axis) >= 1 or len(y_axis) >= 1 or len(z_axis) >= 1):
                        x_string = utils.arrayintostring(x_axis)
                        if x_string == "":
                            x_string = "Null"
                        y_string = utils.arrayintostring(y_axis)
                        if y_string == "":
                            y_string = "Null"
                        z_string = utils.arrayintostring(z_axis)
                        if z_string == "":
                            z_string = "Null"
                        serialized_arr_set = serializer.dumps(arr_set)
                        #return redirect('/columns/' + x_string + "/" + y_string + "/" + z_string)
                        set_cookie = make_response(redirect('/columns/' + x_string + "/" + y_string + "/" + z_string))
                        set_cookie.set_cookie('arr_set' , serialized_arr_set)
                        return set_cookie
                
        else:
            x_axis = ""
            y_axis = ""
            z_axis = ""
    return render_template('tags.html',columns = columns , color_name = color_name)

@app.route('/columns/<xaxis>/<yaxis>/<zaxis>')
def columns_show(xaxis = [],yaxis=[],zaxis=[]):
    color_name = ['aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'black', 'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow', 'grey', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgreen', 'lightgrey', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'loralwhite', 'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'rebeccapurple', 'red', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellow', 'yellowgreen']
    #check
    error =""
    script, script1,script2 = "" , "",""
    div, div1, div2 = "", "",""
    x = utils.stringintoarray(xaxis)
    if x == ['Null']:
        x = []
    y = utils.stringintoarray(yaxis)
    if y == ['Null']:
        y = []
    z = utils.stringintoarray(zaxis)
    if z == ['Null']:
        z = []
    style_plot = decrypted_cookies("arr_set") #pass style plot 
    excel_file_path = decrypted_cookies("path")
    selected_sheet = decrypted_cookies("sheet")
    if (excel_file_path == None or selected_sheet == None or excel_file_path == '' or selected_sheet == ''):
            return redirect(url_for('upload_file'))
    check = utils.checkcolumnsindataset(excel_file_path, selected_sheet , x,y,z)
    if check:
         return redirect("/set_null_columns")
    error, script , div,script1, div1, script2, div2 = utils.testplot(excel_file_path,selected_sheet,x,y,z)
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()


    image_base1, image_base2, image_base3,image_base4, image_base5, image_base6, image_base7, image_base8, image_base9,image_base10, image_base11, image_base12, image_base13, image_base14, image_base15, image_base16, image_base17 = "","","","","","","","","","","","","","","","",""
    image_base1, image_base2, image_base3 ,image_base4, image_base5, image_base6, image_base7, image_base8, image_base9,image_base10, image_base11, image_base12, image_base13, image_base14, image_base15, image_base16, image_base17 = utils.Simple_plot(excel_file_path,selected_sheet,x,y,z, style_plot)
    
    columns = decrypted_cookies("columns")
    x_axis,y_axis, z_axis = "","",""
    serialized_x_axis = serializer.dumps(x_axis)
    serialized_y_axis = serializer.dumps(y_axis)
    serialized_z_axis = serializer.dumps(z_axis)
    set_axis_cookie = make_response(render_template('tags.html',x =x,y=y,z=z,e = error, columns=columns ,
                           js_resources=js_resources,css_resources=css_resources, script =script ,div = div, 
                           script1 =script1 ,div1 = div1, script2 =script2, div2 = div2, color_name = color_name,
                            image_base1 = image_base1 , image_base2 =image_base2, image_base3 = image_base3,
                            image_base4 = image_base4, image_base5 = image_base5, image_base6 = image_base6,
                            image_base7 = image_base7 , image_base8 = image_base8 , image_base9 = image_base9,
                            image_base10 = image_base10, image_base11 = image_base11, image_base12 = image_base12,
                            image_base13 = image_base13, image_base14 = image_base14, image_base15 = image_base15,
                            image_base16 = image_base16, image_base17 = image_base17 ))
    set_axis_cookie.set_cookie('x_axis' , serialized_x_axis)
    set_axis_cookie.set_cookie('y_axis' , serialized_y_axis)
    set_axis_cookie.set_cookie('z_axis' , serialized_z_axis)
    return set_axis_cookie
    



@app.route('/x_axis', methods=['POST'])
def x_axis():
    data = request.json
    serialized_x_axis = serializer.dumps(data)
    x_axis_cookie = make_response(jsonify({'message': 'Tags updated successfully'}))
    x_axis_cookie.set_cookie('x_axis' , serialized_x_axis)
    return x_axis_cookie


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



@app.route('/y_axis', methods=['POST'])
def y_axis():
    data = request.json
    serialized_y_axis = serializer.dumps(data)
    y_axis_cookie = make_response(jsonify({'message': 'Tags updated successfully'}))
    y_axis_cookie.set_cookie('y_axis' , serialized_y_axis)
    return y_axis_cookie


    

@app.route('/z_axis', methods=['POST'])
def z_axis():
    data = request.json
    serialized_z_axis = serializer.dumps(data)
    z_axis_cookie = make_response(jsonify({'message': 'Tags updated successfully'}))
    z_axis_cookie.set_cookie('z_axis' , serialized_z_axis)
    return z_axis_cookie


if __name__ == "__main__":
    app.run(port = 5001 , debug=True )