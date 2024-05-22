from rmworker.rmworker import worker_run
from rmworker.connection_params import connection_params, queue_name

if __name__=="__main__":
    worker_run(connection_params, queue_name)