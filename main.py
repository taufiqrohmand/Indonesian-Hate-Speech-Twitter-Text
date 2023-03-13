import re
import os
import pandas as pd
import sqlite3 as sql3

from flask import Flask, jsonify, send_from_directory, make_response, request
from flasgger import Swagger, LazyString, LazyJSONEncoder, swag_from
from datetime import datetime
from fileinput import filename
from werkzeug.utils import secure_filename
from Cleansing import cleansing

#conect to database
conn = sql3.connect("Dataset/dataset_processing.db", check_same_thread=False)
c = conn.cursor()
#Create table data for query
conn.execute('''CREATE TABLE IF NOT EXISTS text_output (Original varchar(255), Clean_File varchar(255));''')
conn.execute('''CREATE TABLE IF NOT EXISTS file_output (Original varchar(255), Clean_File varchar(255));''')

app = Flask(__name__)

app.json_encoder = LazyJSONEncoder
swagger_template = dict(
    info = {
    'title': LazyString(lambda:'Challenge GOLD API Documentation and Modelling'),
    'version' : LazyString(lambda: '2.0.0'),
    'description' : LazyString(lambda: 'Data Documentation API for Gold Challenge'),
    },
    host = LazyString(lambda: request.host)
)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json'
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}

swagger = Swagger(app,template = swagger_template, config = swagger_config)

#Route Home Page
@app.route('/')
def hello():
    return """<h1>Home Page API Data Cleansing</h1>
    <p>Silakan untuk masuk ke fitur API bisa dengan  
    <a href = 'http://127.0.0.1:5000/docs'>klik disini</a> </p>"""


#API Text Processing
@swag_from("docs/text_processing.yml", methods=['POST'])
@app.route('/text-processing', methods=['POST'])
def text_processing():
    ori = request.form.get('text')
    replace = cleansing(ori)
     
    #insert text input and output to database table data
    conn.execute('''INSERT INTO text_output(Original, Clean_File) VALUES (? , ?);''',(ori, replace))
    conn.commit()

    json_respon = {
        'input' : ori,
        'output' : replace,
    }
    response_data = jsonify(json_respon)
    return response_data
  

#enable extension
allowed_extensions = set(['csv'])
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed_extensions


# API File Processing
@swag_from("docs/file_processing.yml", methods = ['POST'])
@app.route("/upload_csv", methods=["POST"])
def upload_csv():
    file = request.files['file']

    if file and allowed_file(file.filename):
        #Rename file with original name + date time process
        filename = secure_filename(file.filename)
        time_stamp = (datetime.now().strftime('%d-%m-%Y_%H%M%S'))
        new_filename = f'{filename.split(".")[0]}_{time_stamp}.csv'
        
        #save file input to INPUT folder on local
        save_location = os.path.join('input', new_filename)
        file.save(save_location)
        filepath = 'input/' + str(new_filename)

        #Load data file input
        data = pd.read_csv(filepath, encoding='latin-1')
        first_column_pre_process = data.iloc[:, 0]

        #empety array
        cleaned_file = []

        for text in first_column_pre_process:
            file_clean = cleansing(text)

            #insert file input and output to database table data
            with conn:
                c.execute('''INSERT INTO file_output(Original, Clean_File) VALUES (? , ?);''',(text, file_clean))
                conn.commit()

            cleaned_file.append(file_clean)
        
         #save file after clean to OUTPUT folder on local
        new_data_frame = pd.DataFrame(cleaned_file, columns= ['Cleaned_Text'])
        outputfilepath = f'output/{new_filename}'
        new_data_frame.to_csv(outputfilepath)

    json_response = {
        'status_code' : 200,
        'description' : "Silakan dicek di Folder OUTPUT yang ada di local",
        'data' : "File Berhasil di proses",
    }

    response_data = jsonify(json_response)
    return response_data


if __name__ == '__main__' :
    app.run(debug=True)


