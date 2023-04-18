import os
import sys

from src.parsing import engines as core


def test_class_JobsUA_iterable():
    engine = core.JobsUA()
    offers = next(engine)
    print(offers)
    for offer in offers:
        assert offer.title
        assert isinstance(offer.title, str)
