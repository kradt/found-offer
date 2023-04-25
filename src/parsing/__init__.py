import datetime
import multiprocessing
import mongoengine
from typing import Iterator
from loguru import logger
from src.parsing import engines
from src.database import models
from src.config import Config


def write_offer_to_base(offers_engine: Iterator, interval: datetime.timedelta):
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
            saved_offers = (models.Vacancy(**offer.dict()).save() for offer in offers)
            total_sum_offers += len(list(saved_offers))
            logger.debug(f"{total_sum_offers} offers from {offers_engine} were saved in base")
        logger.debug(f"Offers from {offers_engine} Successfully added to base")


def start_parse_data_to_base():
    parsers: list = [engines.WorkUA(), engines.JobsUA()]
    interval = datetime.timedelta(seconds=10)
    for engine in parsers:
        process = multiprocessing.Process(
            target=write_offer_to_base,
            args=(engine, interval),
            name=f"{engine} Process")
        process.start()
    logger.debug("All processes were start!")
