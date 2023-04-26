import datetime
import multiprocessing
import mongoengine
from typing import Iterator
from loguru import logger
from src.parsing import engines
from src.database import models
from src.config import Config
from src.parsing.models import OfferModel


def save_offers_to_base(offers: list) -> int:
    """
    Function saving offers to base and return amount of saved offers
    """
    added_to_base_offers = 0
    for offer in offers:
        if not models.Vacancy.objects(
                title=offer.title, city=offer.city,
                salary_from=offer.salary_from, company=offer.company):
            models.Vacancy(**offer.dict()).save()
            added_to_base_offers += 1

    return added_to_base_offers


def write_offer_to_base(offers_engine: Iterator, interval: datetime.timedelta):
    logger.debug(f"{multiprocessing.current_process().name} was start")
    mongoengine.connect(host=Config.MONGODB_SETTINGS["host"])

    start_time = datetime.datetime.now()
    while True:
        total_sum_offers = 0
        pass_time = datetime.datetime.now()
        if pass_time - start_time >= interval:
            start_time = pass_time
        else:
            continue
        for offers in offers_engine:
            start = datetime.datetime.now()
            len_saved_offers = save_offers_to_base(offers)
            total_sum_offers += len_saved_offers
            #logger.debug(f"{total_sum_offers} offers from {offers_engine} were saved in base")
        #logger.debug(f"{total_sum_offers} offers from {offers_engine} Successfully added to base")


def start_parse_data_to_base():
    parsers: list = [engines.JobsUA()]#, engines.WorkUA()]
    interval = datetime.timedelta(seconds=10)
    for engine in parsers:
        process = multiprocessing.Process(
            target=write_offer_to_base,
            args=(engine, interval),
            name=f"{engine} Process")
        process.start()
    logger.debug("All processes were start!")
