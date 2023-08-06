Simple context manager so that tasks can be reflected in the process names of Celery workers.


For instance:

with ProcTitle("intense task"):
    do_something_intense()



