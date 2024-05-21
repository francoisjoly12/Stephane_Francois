import sys

import paho.mqtt.client as paho


def message_handling(client, userdata, msg):
    print(f"{msg.topic}: {msg.payload.decode()}")


client = paho.Client()
client.on_message = message_handling

if client.connect("localhost", 1883, 60) != 0:
    print("Couldn't connect to the mqtt broker")
    #sys.exit(1)
    mqtt_topic_gas = 'gas'
    mqtt_topic_hum = 'hum'
    mqtt_topic_alarm = 'alarm'
    mqtt_topic_door= 'door'
    mqtt_topic_fan= 'fan'
    client.subscribe(mqtt_topic_hum)

    client.subscribe(mqtt_topic_gas)

    client.subscribe(mqtt_topic_alarm)

    client.subscribe(mqtt_topic_door)

    client.subscribe(mqtt_topic_fan)
        
try:
    print("Press CTRL+C to exit...")
    client.loop_forever()
except Exception:
    print("Caught an Exception, something went wrong...")
finally:
    print("Disconnecting from the MQTT broker")
    client.disconnect()