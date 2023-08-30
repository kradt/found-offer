import pytest
import datetime
from src.parsing.engines.jobsua import JobsUA
from src.parsing.engines.workua import WorkUA

from src.parsing.models import OfferModel


@pytest.mark.parametrize("engine",
                         [
                             (JobsUA()),
                             (WorkUA())
                         ])
def test_class_jobs_ua_iterable(engine):
    offers = next(engine)
    assert engine.current_page == 1

    for offer in offers:
        assert offer.title
        assert offer.city
        assert isinstance(offer.title, str)
        assert isinstance(offer.city, str)
        assert isinstance(offer, OfferModel)
        assert isinstance(offer.salary_from, float) or offer.salary_from is None
        assert isinstance(offer.salary_to, float) or offer.salary_to is None
        assert isinstance(offer.time_publish, datetime.datetime)

    next(engine)
    assert engine.current_page == 2
