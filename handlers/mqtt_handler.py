import paho.mqtt.client as mqtt
import json
from config.database import get_db_connection
from config.settings import logger

MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "medical/reports"

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    report_id = data["report_id"]
    disease = data["disease"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE reports SET disease=? WHERE id=?", (disease, report_id))
    conn.commit()
    conn.close()

    logger.info(f"Updated Report {report_id} with Disease: {disease}")

mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, 1883, 60)
mqtt_client.subscribe(MQTT_TOPIC)
mqtt_client.loop_start()
