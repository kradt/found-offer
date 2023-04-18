import pytest

from src.parsing import engines as core


@pytest.mark.parametrize(("engine"),
                         [
                             (core.JobsUA()),
                             (core.WorkUA())
                         ])
def test_class_jobs_ua_iterable(engine):
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
