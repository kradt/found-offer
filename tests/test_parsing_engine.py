import os
import sys

from src.parsing import engines as core


def test_class_JobsUA_iterable():
    engine = core.JobsUA()
    offers = next(engine)
    assert engine.current_page == 1
    for offer in offers:
        assert offer.title
        assert offer.city
        assert isinstance(offer.title, str)
        assert isinstance(offer.city, str)
        assert isinstance(offer, core.OfferModel)

    next(engine)
    assert engine.current_page == 2
