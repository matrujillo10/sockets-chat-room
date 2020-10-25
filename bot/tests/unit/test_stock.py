"""Unit test for stock command"""

from urllib.parse import quote
import pytest
import requests_mock
from cmds.stock import (
    stock,
    RESULT_MSG,
    REQUEST_ERROR_MSG,
    INVALID_STOCK_CODE_ERROR_MSG,
    LESS_PARAMS_ERROR_MSG,
    MORE_PARAMS_ERROR_MSG,
)


URL = "https://stooq.com/q/l/?s={}&f=sd2t2ohlcv&h&e=csv"


@requests_mock.Mocker(kw="mock")
@pytest.mark.parametrize(
    "stock_code,exists,expected",
    [
        ("AAPL.US", True, RESULT_MSG.format("AAPL.US", "120.4")),
        ("APPL.US", True, RESULT_MSG.format("APPL.US", "120.4")),
        ("MCSF.US", True, RESULT_MSG.format("MCSF.US", "120.4")),
        ("AMZN.US", True, RESULT_MSG.format("AMZN.US", "120.4")),
        ("AAPL.US", False, INVALID_STOCK_CODE_ERROR_MSG.format("AAPL.US")),
        ("AMZN.US", False, INVALID_STOCK_CODE_ERROR_MSG.format("AMZN.US")),
    ],
)
def test_stock(stock_code, exists, expected, **kwargs):
    """Test stock function"""
    if exists:
        content = (
            "Symbol,Date,Time,Open,High,Low,Close,Volume\n"
            f"{stock_code},2020-10-23,22:00:08,116.39,116.55,114.28,120.4,82572645".encode(
                "utf-8"
            )
        )
    else:
        content = (
            "Symbol,Date,Time,Open,High,Low,Close,Volume\n"
            f"{stock_code},N/D,N/D,N/D,N/D,N/D,N/D,N/D".encode("utf-8")
        )
    kwargs["mock"].get(URL.format(quote(stock_code)), content=content)
    assert stock([stock_code]) == expected


@pytest.mark.parametrize(
    "params_len,expected",
    [
        (3, MORE_PARAMS_ERROR_MSG),
        (2, MORE_PARAMS_ERROR_MSG),
        (0, LESS_PARAMS_ERROR_MSG),
    ],
)
def test_stock_params_len_error(params_len, expected):
    """Test stock function with error in
    the number of params"""
    assert stock(list(i for i in range(params_len))) == expected


@requests_mock.Mocker(kw="mock")
@pytest.mark.parametrize(
    "stock_code,expected",
    [
        ("AAPL.US", REQUEST_ERROR_MSG),
        ("APPL.US", REQUEST_ERROR_MSG),
        ("MCSF.US", REQUEST_ERROR_MSG),
        ("AMZN.US", REQUEST_ERROR_MSG),
    ],
)
def test_stock_csv_without_header(stock_code, expected, **kwargs):
    """Test stock function when getting CSV
    without header"""
    kwargs["mock"].get(
        URL.format(quote(stock_code)),
        content=f"{stock_code},2020-10-23,114.28,120.4,82572645".encode("utf-8"),
    )
    assert stock([stock_code]) == expected


@requests_mock.Mocker(kw="mock")
@pytest.mark.parametrize(
    "stock_code,expected",
    [
        ("AAPL.US", REQUEST_ERROR_MSG),
        ("APPL.US", REQUEST_ERROR_MSG),
        ("MCSF.US", REQUEST_ERROR_MSG),
        ("AMZN.US", REQUEST_ERROR_MSG),
    ],
)
def test_stock_not_valid_csv(stock_code, expected, **kwargs):
    """Test stock function when getting
    invalid CSV"""
    kwargs["mock"].get(
        URL.format(quote(stock_code)),
        content="Symbol,Date,Time,Open,High,Low,Close,Volume\n"
        f"{stock_code},2020-10-23,22:00:08,116.55,114.28,120.4,82572645".encode(
            "utf-8"
        ),
    )
    assert stock([stock_code]) == expected


@requests_mock.Mocker(kw="mock")
@pytest.mark.parametrize(
    "stock_code,error,expected",
    [
        ("AAPL.US", 500, REQUEST_ERROR_MSG),
        ("APPL.US", 404, REQUEST_ERROR_MSG),
        ("MCSF.US", 401, REQUEST_ERROR_MSG),
        ("AMZN.US", 403, REQUEST_ERROR_MSG),
    ],
)
def test_stock_http_errors(stock_code, error, expected, **kwargs):
    """Test stock function when getting
    http errors"""
    kwargs["mock"].get(URL.format(quote(stock_code)), status_code=error)
    assert stock([stock_code]) == expected
