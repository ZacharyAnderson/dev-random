import os
import time
import hashlib


def seed_generator():
    return str(time.time()) + str(os.getpid()) + str(os.geteuid()) +\
        str(time.perf_counter())


def hash_generator(entropy, seed):
    print(hashlib.sha256((seed + entropy).encode('utf-8')).hexdigest())


def generate_entropy():
    string = ''
    list = os.listdir('/var/log/')
    for path in list:
        if path.find('.log') != -1:
            with open('/var/log/'+path, 'rb') as file:
                string += str(file.read().hex())
    return string


def dev_random(limit):
    random_count = 0
    seed = seed_generator()
    entropy = generate_entropy()
    max_entropy = len(entropy)//64
    while random_count < limit:
        if random_count == 0:
            hash_generator(entropy[random_count:random_count+64], seed)
        else:
            hash_generator(entropy[random_count*64:(random_count*64)+64], seed)
        random_count += 1
        if random_count >= max_entropy:
            seed = seed_generator()


if __name__ == "__main__":

    dev_random(24)
