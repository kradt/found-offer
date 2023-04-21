import multiprocessing
import mongoengine
from typing import Iterator
from src.parsing import engines
from src.database import models
from src.config import Config


def write_offer_to_base(offers_engine: Iterator):
    mongoengine.connect(host=Config.MONGODB_SETTINGS["host"])
    while True:
        total_sum_offers = 0
        for offers in offers_engine:
            saved_offers = (models.Vacancy(**offer.dict()).save() for offer in offers)
            total_sum_offers += len(list(saved_offers))
            print(f"{total_sum_offers} offers from {offers_engine} were saved in base")
        print(f"Offers from {offers_engine} Successfully added to base")


def start_parse_data_to_base(parsers: list = [engines.WorkUA(), engines.JobsUA()]):
    for engine in parsers:
        p = multiprocessing.Process(target=write_offer_to_base, args=(engine,))
        p.start()
    print("All processes were start!")
