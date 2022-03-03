import time
from importlib import util

import pytest

if util.find_spec("playwright"):
    from playwright._impl._page import Page

from taipy.gui import Gui
from taipy.gui.utils.date import _ISO_to_date


@pytest.mark.teste2e
def test_timzone_specified_1(page: "Page", gui: Gui, helpers):
    _timezone_test_template(page, gui, helpers, "Etc/GMT", "2022-03-03 00:00:00 UTC")


@pytest.mark.teste2e
def test_timzone_specified_2(page: "Page", gui: Gui, helpers):
    _timezone_test_template(page, gui, helpers, "Europe/Paris", "2022-03-03 01:00:00 GMT+1")


@pytest.mark.teste2e
def test_timzone_specified_3(page: "Page", gui: Gui, helpers):
    _timezone_test_template(page, gui, helpers, "Asia/Ho_Chi_Minh", "2022-03-03 07:00:00 GMT+7")


@pytest.mark.teste2e
def test_timzone_specified_4(page: "Page", gui: Gui, helpers):
    _timezone_test_template(page, gui, helpers, "America/Sao_Paulo", "2022-03-02 21:00:00 GMT-3")


@pytest.mark.teste2e
def test_timezone_client_side(page: "Page", gui: Gui, helpers):
    _timezone_test_template(page, gui, helpers, "client", "2022-03-03 01:00:00 GMT+1")


def _timezone_test_template(page: "Page", gui: Gui, helpers, time_zone, text):
    page_md = """
<|{t}|id=text1|>
"""
    t = _ISO_to_date("2022-03-03T00:00:00.000Z")
    gui.add_page(name="test", page=page_md)
    gui.run(run_in_thread=True, single_client=True, time_zone=time_zone)
    while not helpers.port_check():
        time.sleep(0.5)
    page.goto("/test")
    page.expect_websocket()
    page.wait_for_selector("#text1")
    text1 = page.query_selector("#text1")
    assert text1.inner_text() == text