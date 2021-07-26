import os
import secrets
import flask
import json
import codecs
from zipfile import ZipFile
from flask import send_file
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

app=flask.Flask(__name__)

app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')
DOWNLOAD_FOLDER = os.path.join(path, 'encrypt_files')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.isdir(DOWNLOAD_FOLDER):
    os.mkdir(DOWNLOAD_FOLDER)

app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER


ALLOWED_EXTENSIONS = set(['yaml'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            random_key = secrets.token_hex(16)
            metodo = flask.request.form.get("method_cipher")
            if metodo == "Encrypt":
                fileresult = random_key + ".yaml"
                destpath = '.\\encrypt_files\\' + random_key + '\\'
                os.mkdir(destpath)
                command = 'java -cp secure-properties-tool.jar com.mulesoft.tools.SecurePropertiesTool file encrypt AES CBC {0} .\\uploads\\{1} {3}{2}'.format(random_key,filename,fileresult,destpath)
                os.system(command)
                instrucciones = destpath + 'instrucciones.txt'
                with open(instrucciones, "a") as textfile:
                    textfile.write("la clave de encriptacion es: " + random_key)
                path = '.\\encrypt_files\\' + random_key
                zipfile1 = destpath + 'ejemplo.zip'
                archivofinal = destpath + fileresult
                with ZipFile(zipfile1, 'a') as archivozip:
                    archivozip.write(instrucciones)
                    archivozip.write(archivofinal)
                #filefinal = codecs.open(path, 'rb').read()
                #jsonfile = json.loads(filefinal)
                #flash(filefinal)
            if metodo == "Decrypt":
                clave = request.form['ek']
                fileresult = filename
                destpath = '.\\encrypt_files\\' + clave + '\\'
                os.mkdir(destpath)
                command = 'java -cp secure-properties-tool.jar com.mulesoft.tools.SecurePropertiesTool file decrypt AES CBC {0} .\\uploads\\{1} {3}{2}'.format(clave,filename,fileresult,destpath)
                os.system(command)
                instrucciones = destpath + 'instrucciones.txt'
                with open(instrucciones, "a") as textfile:
                    textfile.write("la clave de encriptacion es: " + clave)
                path = '.\\encrypt_files\\' + clave
                zipfile1 = destpath + 'ejemplo.zip'
                archivofinal = destpath + fileresult
                with ZipFile(zipfile1, 'a') as archivozip:
                    archivozip.write(instrucciones)
                    archivozip.write(archivofinal)
                #filefinal = codecs.open(path, 'rb').read()
                #jsonfile = json.loads(filefinal)
                #flash(filefinal)
            if metodo == "Encrypt2":
                clave = request.form['ek']
                fileresult = filename
                destpath = '.\\encrypt_files\\' + clave + '\\'
                os.mkdir(destpath)
                command = 'java -cp secure-properties-tool.jar com.mulesoft.tools.SecurePropertiesTool file encrypt AES CBC {0} .\\uploads\\{1} {3}{2}'.format(clave,filename,fileresult,destpath)
                os.system(command)
                instrucciones = destpath + 'instrucciones.txt'
                with open(instrucciones, "a") as textfile:
                    textfile.write("la clave de encriptacion es: " + clave)
                path = '.\\encrypt_files\\' + clave
                zipfile1 = destpath + 'ejemplo.zip'
                archivofinal = destpath + fileresult
                with ZipFile(zipfile1, 'a') as archivozip:
                    archivozip.write(instrucciones)
                    archivozip.write(archivofinal)
            return send_file(zipfile1, as_attachment=True) #redirect('/') 
        else:
            flash('Allowed file type are only "yaml"')
            return redirect(request.url)

if __name__ == "__main__":
    app.run(host = '127.0.0.1',port = 5000, debug = True)
