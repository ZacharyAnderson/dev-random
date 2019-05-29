import os
import time


def seed_generator():
    return str(time.time()) + str(os.getpid()) + str(os.geteuid()) +\
        str(time.perf_counter())


if __name__ == "__main__":
    print(seed_generator())
