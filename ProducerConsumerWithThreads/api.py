from ProducerConsumerWithThreads import execution_manager as em


def db_item_handler(item):
    """
    The function gets an item and publish it to 
    o.g. non-relational database like MongoDB, etc.
    
    How to use? README.txt will surely help you (I hope so ;) )
    Or contact rozacek@gmail.com  
    :param data: 
    :return: 
    """
    print("Update object for item: {}".format(item))


def publish_item(item):
    em.publish_data_with_queue(item=item,
                               db_handler=db_item_handler)
