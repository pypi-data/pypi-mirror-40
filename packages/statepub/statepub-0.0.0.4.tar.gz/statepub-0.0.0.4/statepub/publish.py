# Std library imports
import os
import time
# Third party imports
import paho.mqtt.client as mqtt
# in-package imports
from statepub.state import StateInterface


class StatePublisher:
    """
    This object is used to publish the information contained within state objects to the mqtt network.

    A word on the topics:
    The final topic to publish to will consist of three "path pieces". The base path being dictated by the initial
    parameters given during the creation of the object, the further path being given as parameter to this function
    and the top most topic being the key string of the given dictionary

    {object wide base path}/{method wide base path}/{dictionary key}

    CHANGELOG

    Added 29.12.2018
    """
    # The mqtt client object expects an ID. This static field will keep track of how many Publisher objects have been
    # created and supplies each one with a new ID.
    id_counter = 0

    def __init__(self, topic_base, broker_ip, broker_port=1883):
        """
        The Constructor.

        CHANGELOG

        Added 29.12.2018

        :param str topic_base:  The string which is to be used as the "base path" of the topic to which the info
                                should be published.
        :param str broker_ip:   The string of the IP of the machine on which the mqtt broker is running
        :param int broker_port: The port on which the mqtt is running. DEFAULT is 1883 for mosquitto mqtt broker
        """
        self.topic_base = topic_base

        # We get the ID of the current object by using the current state of the static id counter which always provides
        # a new unique integer ID. then of course we have to increment that so that the next object to be created will
        # also have a unique ID.
        self.id = StatePublisher.id_counter
        StatePublisher.id_counter += 1
        print(self.id_counter)

        # We need to create a MQTT client object, which we will store as a attribute of the publisher object, so it can
        # be used in every method.
        self.client = mqtt.Client("Publisher{}".format(self.id))

        # Now we just need to connect the client to the broker(server) and it is ready to go.
        self.client.connect(broker_ip, broker_port)
        self.client.loop_start()

    def publish(self, *states, topic=''):
        """
        Given multiple State objects this method will publish all the information/values contained within the attributes
        of those objects.
        A base topic path of the publishing can be given.

        CHANGELOG

        Added 29.12.2018

        :param StateInterface states:   A List of all the states to be published to the network
        :param str topic:               A base path for the topics to be published to
        :return:
        """
        # What we do here is we get the dictionary representations of all states and then merge them together into one
        # big dictionary and then call the method which publishes the dictionary.
        combined_dict = {
            'timestamp': time.time()
        }
        for state in states:  # type: StateInterface

            # Obviously we want the new state information, so we call the acquire on each of the states
            state.acquire()
            combined_dict.update(state.to_dict())

        self.publish_dict(combined_dict, topic)

    def publish_dict(self, dictionary, topic):
        """
        Takes a dictionary and publishes all values as values to the MQTT network, with the keys of the dict being the
        topics to publish to.

        A word on the topics:
        The final topic to publish to will consist of three "path pieces". The base path being dictated by the initial
        parameters given during the creation of the object, the further path being given as parameter to this function
        and the top most topic being the key string of the given dictionary

        {object wide base path}/{method wide base path}/{dictionary key}

        CHANGELOG

        Added 29.12.2018

        :param dictionary:
        :param topic:
        :return:
        """
        for key, value in dictionary.items():
            # Creating the topic to publish the value to by joining the actual name of the topic, which is the key
            # string in this dict with the base path given to the publisher object and the base path given to this
            # method
            topic_string = os.path.join(self.topic_base, topic, key)

            self.client.publish(topic_string, str(value))

    def close(self):
        """
        This method properly closes down the MQTT client object, which is used for network communication.

        CHANGELOG

        Added 29.12.2018

        :return:
        """
        self.client.disconnect()
        self.client.loop_stop()
