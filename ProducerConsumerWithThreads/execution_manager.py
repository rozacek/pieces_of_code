import ProducerConsumerWithThreads.config as config
from ProducerConsumerWithThreads import ProducerQueues as pq
from ProducerConsumerWithThreads import ConsumerThreads as ct


def produce_data(item):  # Producer
    """
    Method as e.g. Django webservice entry point.

    Handles data and puts it to Queue.
    Data should have the same id, if must be handled
    by the same queue.    
    :param item:
    :return:
    queue_id - needed for event_consumer
    """
    # extract queue_id from data
    queue_id = pq.get_queue_id(item)
    # create or get Queue instance and put element
    queue = pq.ProducerQueues(item).instances.get(queue_id).queue
    try:
        # Main part of function - put to Queue
        queue.put_nowait(item)
    except Exception as e:
        # Place for logging
        print("Exception {} occured while putting "
              "to queue with id: {}".format(e, queue_id))
    return queue_id, queue


def publish_data_with_queue(item, db_handler):
    """
    This method is used to invoke event publishing
    procedure via the queue <-> thread mechanism
    :param event_data:
    :return:
    """

    # Put item to Queue
    queue_id, queue = produce_data(item)

    # Check if queue is serviced by thread, if no then start new
    if not ct.ConsumerThreads.instances.get(queue_id):
        th = ct.ConsumerThreads(queue_id, data_consumer,
                                **{
                                    config.queue: queue,
                                    config.db_handler: db_handler
                                })
        th.instances[queue_id].start()
    return True


def data_consumer(consumer_args):
    """
    Gets queue reference, gets item from queue and publishes
    this item via db_handler.
    
    When queue is empty, method checks if queue_id exists
    in ProducerQueues.instances and deletes it.

    :param 
    :return:
    """
    queue = consumer_args.get(config.queue)
    publish_function = consumer_args.get(config.db_handler)
    if queue is not None:
        queue_id = queue.queue_id
        while not queue.empty():
            item = queue.get()
            try:
                publish_function(item)
            except Exception as e:
                print("Log that item publishing failed due to {}".format(e))
        else:
            if pq.ProducerQueues.instances.get(queue_id):
                del pq.ProducerQueues.instances[queue_id]
                print("Delete Queue: {}".format(queue_id))


