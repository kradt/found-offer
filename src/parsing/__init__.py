import multiprocessing
import os
from typing import Iterator
import time
from src.parsing import engines


def write_offer_to_base(offers_engine: Iterator):
    while True:
        print(1)
        time.sleep(1)
        print(os.getpid(), "sleep")
    # for offer in offers_engine:
    #     print(offer)
    #     pass
    print(f"Offers from {offers_engine} Successfully added to base")

def start_parse_data_to_base():
    p = multiprocessing.Process(target=write_offer_to_base, args=(engines.WorkUA(),))
    p.start()
