import os
import time
import hashlib
import argparse


def seed_generator():
    """
        seed_generator takes the time, the python process id,
        the current proccess's effective user id, the time
        the python program has been running and creates a string.
    """
    return str(time.time()) + str(os.getpid()) + str(os.geteuid()) +\
        str(time.perf_counter())


def hash_generator(entropy, seed):
    """
        hash_generator takes a 64 char string from the entropy pool
        and adds that with our seed. Then it creats a sha256 hash
        and prints a hexidecimal number.
    """
    print(hashlib.sha256((seed + entropy).encode('utf-8')).hexdigest())


def generate_entropy():
    """
        generate_entropy will create our entropy pool. To do this we read
        all available log files from /var/log/ and create one large string
        of data to be read from.
    """
    string = ''
    list = os.listdir('/var/log/')
    for path in list:
        if path.find('.log') != -1:
            with open('/var/log/'+path, 'rb') as file:
                string += str(file.read().hex())
    return string


def dev_random(limit):
    """
        dev_random takes an input - limit which is the amount of hashes to
        be generated. First, we create our seed and generate our entropy pool.
        Then, we start creating our hashes by working down our entropy pool in
        64 character blocks and inputing that with our seed to generate our hashs.
        In the chance the limit is greater then the entropy pool we will recursively
        call the dev_random function with the limit being the remaining hashes and
        regenerate the entropy and seeds.
    """
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
            dev_random(limit - max_entropy)
            return


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Generate random number hashes.")
    parser.add_argument(
        '--limit', "-L", help="Amount of hashes required. Must be a positive integer",
        required=True, type=int)
    args = vars(parser.parse_args())

    dev_random(args['limit'])
