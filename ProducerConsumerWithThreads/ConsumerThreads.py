import threading

from threading import Lock


class ConsumerThreads:
    """
    Multiton class that holds Thread instances by thread_id.
    Each Thread instance executes function defined when
    Thread is created.
    """
    instances = {}

    def __init__(self,
                 thread_id,
                 worker_func,
                 **worker_args):
        with Lock():  # Lock for thread that creates the Thread
            if not ConsumerThreads.instances.get(thread_id):
                print("Create Thread: {}".format(thread_id))
                ConsumerThreads.instances[thread_id] = \
                    ConsumerThreads.__ConsumerThreads(thread_id,
                                                      worker_func,
                                                      **worker_args)

    class __ConsumerThreads(threading.Thread):
        """
        Single Thread instance.
        """

        def __init__(self,
                     thread_id,
                     worker_func,
                     **worker_args):
            threading.Thread.__init__(self)
            self.thread_id = thread_id
            self.worker_func = worker_func  # define Thread's function
            self.worker_args = worker_args  # define Thread's function's arguments

        def run(self):
            """
            Function executor when Thread is started.
            """
            # execute Thread's function while it has some work
            self.worker_func(self.worker_args)
            # remove Thread instance when it ended its work
            remove_exited_thread(self.thread_id)


def get_list_of_instances():
    """
    Static method returning list of existing Producer queues.
    :return: 
    """
    return list(ConsumerThreads.instances.values())


def remove_exited_thread(thread_id):
    """
    Static method that deletes executed Thread from instances.
    :param thread_id:
    :return:
    """
    del ConsumerThreads.instances[thread_id]
    print("Delete Thread: {}".format(thread_id))
