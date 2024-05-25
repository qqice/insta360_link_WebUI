from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/control', methods=['POST'])
def control():
    direction = request.form.get('direction')
    event = request.form.get('event')
    print("button pressed: " + direction + " " + event)
    # 在这里添加你的摄像头控制代码
    return 'OK'


@app.route('/slider', methods=['POST'])
def slider():
    position = request.form.get('position')
    print("slider moved: " + position)
    # 在这里添加你的摄像头控制代码
    return 'OK'


@app.route('/pause', methods=['POST'])
def pause():
    print("pause button pressed")
    # 在这里添加你的摄像头控制代码
    return 'OK'


if __name__ == '__main__':
    app.run(debug=True)
