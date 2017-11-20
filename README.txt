Welcome in rozacek's github repostory: pieces_of_code

Here you have pieces of code, that in my opinion are worthy to share.
---------------------------------------------------------------------------

>>> 1. ProducerConsumerWithThreads <<<


PRODUCER / CONSUMER with Threads...
I'd like to present you the mechanism od Producer / Consumer (Python 3.4)
that allowed me to publish a lot of events via Django webservice to
non-relational database (MongoDB) without any race condition.

Let me present a piece of story.

I had some Django webservice for reporting test cases results
from Jenkins. So, when Jenkins executed much Jobs in parallel
then I came across obstacle named: race condition... explanation.

The architecture was:
---------------------
Every job had its representation in Database and consisted of many testcases.
When for example two testcases from same Job came via webservice it was scenario:

1. tc1 picked JobA from DB
2. tc2 picked JobA from DB

3. tc1 updated JobA
4. tc2 updated JobA (and didn't know anything about tc1)

5. tc1 stored JobA in DB
6. tc2 stored JobA in DB

Result:
-------
In DB it was only information about tc2, because it had NO information
about tc1 and was saved as the last testcase.
Information WERE LOST.
The worst was I had much such naughty Jenkins Jobs.


Solution:
---------
For every Job prepare a separate Queue (this is obvious).
To not loose performance for many Jobs, every Queue got it's
own Thread.

As a PRODUCER role, there are webservices (like Django managed urls).
When a testcase gets via Django webservice, it puts to properly created Queue (for Job id)
and then checks for Thread executor (to use created or to create new one) - CONSUMER role.


How to use?
-----------

Just import:

# 1. In api change method 'db_item_handler' to your own db interface.

# 2. In ProducerConsumerWithThreads\ProducerQueues.py define how method 'get_queue_id' should extract ID from items.

# 3. from .ProducerConsumerWithThreads import api

# 4. publish your items/events/data (as you name it) via api.publish_item()
