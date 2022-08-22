import flask

from werkzeug.utils import secure_filename
app = flask.Flask(__name__)


@app.route('/', methods = ['POST'])
def handle_request():
    if flask.request.method == 'POST':
       video_file = flask.request.files['file']
       extracted_file_name = video_file.filename.split('/')[-1]
       video_file.save(secure_filename(extracted_file_name))
       return 'File uploaded to server successfully'
    
        
    return "Welcome to Flask Server"
	   
app.run(host="0.0.0.0", port=5000, debug=True)