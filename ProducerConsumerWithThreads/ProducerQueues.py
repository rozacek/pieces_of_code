import datetime
import ProducerConsumerWithThreads.config as config

from queue import Queue
from threading import Lock  # no reentrant Lock


"""
Class EventsQueue

"""


class ProducerQueues:
    """
    Multiton class ProducerQueues which is responsible to handle
    instances of class __ProducerQueues. Only one instance for 
    given id can be created and stored in memory.
    """

    class __ProducerQueues:
        """
        Class holds instance of Queue and its 'queue_id'
        """
        def __init__(self, queue_id):
            self.queue = Queue(maxsize=config.MAX_QUEUE_SIZE)
            self.queue.queue_id = queue_id

        def get_queue_id(self):
            return self.queue_id

    instances = {}

    def __init__(self, item):  # Creates New only when it's key doesn't exists
        """
        Constructor creates new Queue for Producer only when
        instance with given queue_id doesn't exist.
        :param item: 
        """
        with Lock():  # Lock for thread that creates the Queue
            queue_id = get_queue_id(item)
            if not ProducerQueues.instances.get(queue_id):
                print("Create Queue: {}".format(queue_id))
                ProducerQueues.instances[queue_id] = \
                    ProducerQueues.__ProducerQueues(queue_id)


def get_list_of_instances():
    """
    Static method returning list of existing Producer queues.
    :return: 
    """
    return list(ProducerQueues.instances.values())


def get_dict_of_queues_sizes():
    """
    Getter for sizes of existing Producer queues instances.
    :return: 
    """
    queues_sizes = {}
    for queue_id, queue in ProducerQueues.instances.items():
        queues_sizes.update({
            queue_id: queue.queue.qsize()})
    return queues_sizes


def get_queue_id(item):
    """
    Gets queue_id from item's data.
    :param event:
    :return:
    """
    return item.get("id", "None")
