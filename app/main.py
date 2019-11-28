from flask import Flask
from flask import render_template

import images
 
app = Flask(__name__)
 
@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/get_random_image')
def get_random_image():
    link = images.get_random_file()
    return link
 
if __name__ == '__main__':
    print('Server Started!')
    
    t1 = images.ThreadClass()

    app.run(debug=True, threaded=True, host='0.0.0.0', port=8081)