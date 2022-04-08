from flask import Flask, request, jsonify, make_response,render_template
import os,json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('audio.html')
 
#lame --silent --decode  /home/ec2-user/audiocompare/AudioCompare/hello1.wav /tmp/tmptLpr7X/1649042747.37
@app.route('/res', methods=['POST'])
def res():
    header = request.headers
    data = request.data
    filename = header['user']
    with open('static/{}.wav'.format(filename),'wb') as f:
        f.write(data)
    print('header: {}'.format(header['user']))
    print(data)
    return header['user']
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, ssl_context='adhoc')