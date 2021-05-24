from flask import Flask, render_template, request, redirect, url_for
from ocr import Date_pattern, ImagetoText, ImagetoCharBoxes, ImagetoWordBoxes, PinCode_pattern, Email_pattern
import os
import pathlib

#folder to upload
upload_folder = '/static/uploads/'
save_dir = '/home/lucifer/NHAI/ocr_pdf/flask1/static/uploads/'  #to save images
word_result_dir = '/static/word_updated/'
char_result_dir = '/static/char_updated/'

#Extension to be allowed
allowed_extension = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['save_dir'] = save_dir

def allowed_file(filename):
    """ Checks the filename is allowed or not. Check the image is from given format or not """

    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed_extension

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index')
def helper():
    #check is there file in the request
    if 'file' not in request.files:
        return render_template('index.html', msg="No file selected, Please select file.")
        

    file = request.files['file']   

    #if no file is selected
    if file.filename == '':
        return render_template('index.html', msg="No file selected, Please select file.")
    
    #save image in directory to show on webpage
    file.save(os.path.join(app.config['save_dir'], file.filename))

    return file

@app.route('/text', methods=['GET', 'POST'])
def text():
    if request.method == 'POST':

        file = helper()

        if file and allowed_file(file.filename):

            extracted_text = ImagetoText(file)



            return render_template('text.html',
                                    msg = "Succesfully Proccessed!",
                                    extracted_text=extracted_text,
                                    img_src= upload_folder + file.filename)

    elif request.method == 'GET':
        return render_template('text.html')


@app.route('/word', methods=['GET', 'POST'])
def word():
    # if request.method == 'POST':
    if request.method == 'POST':

        file = helper()
        
        if file and allowed_file(file.filename):
            BoxedImage = ImagetoWordBoxes(file)
            
            return render_template('word.html',
                                    msg = "Succesfully Proccessed!",
                                    BoxedImage= word_result_dir+BoxedImage,
                                    img_src= upload_folder + file.filename)

    elif request.method == 'GET':
        return render_template('word.html')


@app.route('/char', methods=['GET', 'POST'])
def char():
        # if request.method == 'POST':
    if request.method == 'POST':

        file = helper()
        
        if file and allowed_file(file.filename):
            BoxedImage = ImagetoCharBoxes(file)
            
            return render_template('char.html',
                                    msg = "Succesfully Proccessed!",
                                    BoxedImage= char_result_dir+BoxedImage,
                                    img_src= upload_folder + file.filename)

        # elif request.form['Data'] == 'Date':
        #     DateImage = Date_pattern(file)
            
        #     return render_template('char.html',
        #                             msg = "Succesfully Proccessed!",
        #                             DateImage= char_result_dir+DateImage,
        #                             img_src= upload_folder + file.filename)


        # elif request.form['Data'] == 'Pin Code':
        #     PinCodeImage = PinCode_pattern(file)
            
        #     return render_template('char.html',
        #                             msg = "Succesfully Proccessed!",
        #                             PinCodeImage= char_result_dir+PinCodeImage,
        #                             img_src= upload_folder + file.filename)

        # elif request.form['Data'] == 'Email':
        #     EmailImage = Email_pattern(file)
            
        #     return render_template('char.html',
        #                             msg = "Succesfully Proccessed!",
        #                             EmailImage= char_result_dir+EmailImage,
        #                             img_src= upload_folder + file.filename)


    elif request.method == 'GET':
        return render_template('char.html')

if __name__ == '__main__':
    app.run(port=8080, debug=True)