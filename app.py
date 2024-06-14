from flask import Flask, jsonify
import threading
import paho.mqtt.client as mqtt

app = Flask(__name__)

# Data storage
sensor_data = {
    "temperature": None,
    "humidity": None
}

# MQTT settings
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC_TEMPERATURE = "/sensor/data/temperature"
MQTT_TOPIC_HUMIDITY = "/sensor/data/humidity"

# MQTT client setup
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    client.subscribe(MQTT_TOPIC_TEMPERATURE)
    client.subscribe(MQTT_TOPIC_HUMIDITY)

def on_message(client, userdata, msg):
    global sensor_data
    topic = msg.topic
    payload = msg.payload.decode('utf-8')
    if topic == MQTT_TOPIC_TEMPERATURE:
        sensor_data["temperature"] = payload
    elif topic == MQTT_TOPIC_HUMIDITY:
        sensor_data["humidity"] = payload
    print(f"Received message: {payload} on topic: {topic}")

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

def mqtt_loop():
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_forever()

mqtt_thread = threading.Thread(target=mqtt_loop)
mqtt_thread.start()

# Flask API routes
@app.route('/api/temperature', methods=['GET'])
def get_temperature():
    return jsonify({"temperature": sensor_data["temperature"]})

@app.route('/api/humidity', methods=['GET'])
def get_humidity():
    return jsonify({"humidity": sensor_data["humidity"]})

@app.route('/api/sensor_data', methods=['GET'])
def get_sensor_data():
    return jsonify(sensor_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
