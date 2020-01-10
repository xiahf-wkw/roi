import pytest

def pytest_addoption(parser):
    parser.addoption("--envopt", action="store", default="T1",
        help="my option: type1 or type2")
    parser.addoption("--db_check", action="store", default=True,
                     help="my option: type1 or type2")

@pytest.fixture
def envopt(request):
    return request.config.getoption("--envopt")


@pytest.fixture
def db_check(request):
    return request.config.getoption("--db_check")

#生成html时候加入描述


from datetime import datetime
from py.xml import html
import pytest


@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(2, html.th('Description'))
    cells.insert(1, html.th('Time', class_='sortable time', col='time'))
    cells.pop()


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(2, html.td(report.description))
    cells.insert(1, html.td(datetime.utcnow(), class_='col-time'))
    cells.pop()


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)

