import logging
import multiprocessing
import os
import time

from tasks import get_word_counts


PROCESSES = multiprocessing.cpu_count() - 1
NUMBER_OF_TASKS = 10


def process_tasks(task_queue):
    logger = multiprocessing.get_logger()
    proc = os.getpid()
    while not task_queue.empty():
        try:
            book = task_queue.get()
            get_word_counts(book)
        except Exception as ex:
            logger.error(ex)
        logger.info(f"Process {proc} completed successfully")
    return True


def add_tasks(task_queue, number_of_tasks):
    for num in range(number_of_tasks):
        task_queue.put("pride-and-prejudice.txt")
        task_queue.put("heart-of-darkness.txt")
        task_queue.put("frankenstein.txt")
        task_queue.put("drakula.txt")

    return task_queue


def run():
    empty_task_queue = multiprocessing.Queue()
    full_task_queue = add_tasks(empty_task_queue, NUMBER_OF_TASKS)
    processes = []
    print(f"Running with {PROCESSES} processes!")
    start = time.time()
    for w in range(PROCESSES):
        p = multiprocessing.Process(target=process_tasks, args=(full_task_queue, ))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    print(f"Time Taken = {time.time() - start:.10f}")


if __name__ == '__main__':
    multiprocessing.log_to_stderr(logging.ERROR)
    run()
