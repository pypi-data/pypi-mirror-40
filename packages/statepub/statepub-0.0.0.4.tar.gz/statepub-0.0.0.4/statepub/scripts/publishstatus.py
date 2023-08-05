import time

import click

from statepub.state import ComputingState
from statepub.publish import StatePublisher


@click.command(name='publish-status', short_help='Publish the status of this machine to the MQTT network')
@click.option('--interval', default=2, help='Amount of seconds between two publishes')
@click.option('--broker_port', default=1883, help='The port on which the MQTT broker operates')
@click.argument('broker_ip', metavar='<broker ip>')
@click.argument('topic', metavar='<topic>')
def cli(interval, broker_port, broker_ip, topic):
    """
    After invoking this command, it will repeatedly after set intervals sent the status of this machine to the MQTT
    network
    """
    click.echo('hello')

    publisher = StatePublisher(topic, broker_ip, broker_port=broker_port)

    try:
        while True:
            time_seconds = round(time.time() * 1000)
            if time_seconds % interval:

                # Actually execute the relevant code for the publishing here
                computing_state = ComputingState()
                publisher.publish(computing_state)

            time.sleep(0.1)

    except KeyboardInterrupt:
        publisher.close()
        raise KeyboardInterrupt()
