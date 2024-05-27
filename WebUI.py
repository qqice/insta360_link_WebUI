from flask import Flask, request, render_template
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


# 创建一个MQTT客户端对象
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

# 连接到MQTT服务器
client.connect("127.0.0.1", 1883, 60)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/control', methods=['POST'])
def control():
    direction = request.form.get('direction')
    event = request.form.get('event')
    print("button pressed: " + direction + " " + event)

    if event == 'up':
        client.publish("camera/control", "{\"control\":1}")
    elif direction == 'center':
        client.publish("camera/control", "{\"control\":2}")
    elif direction == 'right':
        client.publish("camera/control", "{\"control\":0,\"horizontal_direction\":1,\"horizontal_speed\":4,"
                                         "\"vertical_direction\":0,\"vertical_speed\":1}")
    elif direction == 'left':
        client.publish("camera/control", "{\"control\":0,\"horizontal_direction\":255,\"horizontal_speed\":4,"
                                         "\"vertical_direction\":0,\"vertical_speed\":1}")
    elif direction == 'down':
        client.publish("camera/control", "{\"control\":0,\"horizontal_direction\":0,\"horizontal_speed\":1,"
                                         "\"vertical_direction\":1,\"vertical_speed\":4}")
    elif direction == 'up':
        client.publish("camera/control", "{\"control\":0,\"horizontal_direction\":0,\"horizontal_speed\":1,"
                                         "\"vertical_direction\":255,\"vertical_speed\":4}")
    else:
        pass

    return 'OK'


@app.route('/slider', methods=['POST'])
def slider():
    position = request.form.get('position')
    print("slider moved: " + position)

    client.publish("camera/control", "{\"control\":3,\"zoom\":%d}" % int(100 * (1 + int(position) / 100 * 3)))

    return 'OK'


@app.route('/pause', methods=['POST'])
def pause():
    print("pause button pressed")

    client.publish("camera/control", "{\"control\":1}")

    return 'OK'


if __name__ == '__main__':
    client.loop_start()
    app.run(host="0.0.0.0", debug=False)
    client.loop_stop()
