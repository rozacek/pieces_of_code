from ProducerConsumerWithThreads import execution_manager as em


def db_item_handler(item):
    """
    The function gets an item and publish it to 
    o.g. non-relational database like MongoDB.
    
    Example: There is 2 or more Jenkins jobs, that every 
    executes 10 test cases (tc).
    Every tc can execute in parallel with rest of tcs.
    
    item_from_job1 = {
        "id": "job1"
        "test_case": "tc1"
    }...  e.g. about 10 items with 'job_name': tc1, tc2, tc3, ..., tc10 
               and same id "job1"
    item_from_job2 = {
        "id": "job2"
        "test_case": "worker2.1"
    }...  e.g. about 10 items with 'job_name': tc1, tc2, tc3, ..., tc10
               and same id "job2"

    When lots of test cases reports from one e.g. Jenkins job 
    in parallel they can cause some race conditions while 
    updating the same Job object e.g. in e.g. MongoDB.
    
    So, it is need to queue test cases per job id 
    and then every test case for every Jenkins job 
    is published separately in FIFO order.    
    :param data: 
    :return: 
    """
    print("Update object for item: {}".format(item))


def publish_data(item):
    em.publish_data_with_queue(item=item,
                               db_handler=db_item_handler)
