import os
import sys
import pytest
import requests

sys.path.append(os.getcwd())
from src.parsing import engines as core


@pytest.mark.parametrize(("job", "city", "salary_from", "salary_to", "engines"),
                         [("бухгалтер", "Київ", 2000, 10000, [core.WorkUA()]),
                         ("backend", "Одеса", 15000, 30000, [core.WorkUA(), core.JobsUA()]),
                         ("Швея", "", 7000, 16000, [core.JobsUA()])])
def test_query_class(job, city, salary_from, salary_to, engines):
    query = core.Query(
        job=job,
        city=city,
        salary_from=salary_from,
        salary_to=salary_to)
    urls = query.urls(engines)
    assert isinstance(urls, tuple)
    assert len(urls) == len(engines)
    for url in urls:
        print(url)
        rq = requests.get(url)
        assert rq.status_code == 200
