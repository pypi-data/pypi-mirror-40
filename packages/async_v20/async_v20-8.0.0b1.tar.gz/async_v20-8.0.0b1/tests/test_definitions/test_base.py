import logging
import ujson as json

import numpy as np
import pandas as pd
import pytest
from pandas import DataFrame

from async_v20.definitions.base import Model, Array, create_attribute
from async_v20.definitions.helpers import flatten_dict
from async_v20.definitions.primitives import TradeID, AccountID
from async_v20.definitions.types import Account
from async_v20.definitions.types import ArrayInstrument
from async_v20.definitions.types import ArrayOrder
from async_v20.definitions.types import ArrayPosition
from async_v20.definitions.types import ArrayStr
from async_v20.definitions.types import ArrayTrade
from async_v20.definitions.types import ArrayTransaction
from async_v20.definitions.types import Order
from async_v20.definitions.types import Position
from async_v20.definitions.types import Trade
from async_v20.definitions.types import TradeSummary
from async_v20.exceptions import InstantiationFailure, IncompatibleValue
from ..data.json_data import GETAccountID_response, example_trade_summary, example_changed_trade_summary
from ..data.json_data import account_example
from ..data.json_data import example_transactions, example_positions, example_instruments, example_trade_array
from ..fixtures.client import client
from ..fixtures.server import server

logger = logging.getLogger('async_v20')
logger.disabled = True

client = client
server = server

from pandas import Timestamp


@pytest.fixture
def account():
    result = Account(**GETAccountID_response['account'])
    yield result
    del result


def test_account_has_correct_methods(account):
    assert hasattr(account, 'dict')
    assert hasattr(account, 'data')
    assert hasattr(account, 'series')


@pytest.fixture
def test_kwargs():
    kwargs = {'type': 'LIST', 'value': 'TEST_VALUE'}
    yield kwargs
    del kwargs


@pytest.fixture
def test_class():
    class TestClass(Model):
        _dispatch = {'type': 'LIST'}

    test_cls = TestClass
    yield test_cls
    del test_cls


def test_base_dispatch_works_correctly():
    pass


def test_json_dict_returns_correct_data_structure(account):
    """Test the result is formatted correctly. There is a requirement for
    json_dict to be able to cast floats to strings, this is necessary when
    serializing objects to send to OANDA. Though when used internally is it more
    natural to leave floats as floats."""

    result = account.dict(json=True, datetime_format='UNIX')
    # Test result is a dict
    assert type(result) == dict
    flattened_result = flatten_dict(result)
    # Test that all values have the correct data type
    for value in flattened_result:
        assert isinstance(value, (dict, str, int, list))

    result = account.dict(json=False, datetime_format='UNIX')
    assert type(result) == dict
    flattened_result = flatten_dict(result)
    # Test that all values have the correct data type. Specifically that
    # all floats have not been casted to a string.
    for value in flattened_result:
        assert isinstance(value, (dict, float, str, int, list))
        if isinstance(value, str):
            with pytest.raises(ValueError):
                float(value)


def test_json_data(account):
    result = account.json(datetime_format='UNIX')
    assert type(result) == str
    assert json.loads(result) == account.dict(json=True, datetime_format='UNIX')


def test_data(account):
    result = account.data(json=True, datetime_format='UNIX')
    for value in result:
        assert isinstance(value, (str, int, list))

    result = account.data(json=False)
    for value in result:
        assert isinstance(value, (float, str, int, list))
        if isinstance(value, str):
            with pytest.raises(ValueError):
                float(value)


def test_series_doesnt_convert_datetime(account):
    result = account.series(datetime_format='UNIX')
    for value in result:
        assert isinstance(value, (float, str, int, list, type(None)))
        if isinstance(value, str):
            # All values in a series object should be a float if they can be
            with pytest.raises(ValueError):
                float(value)


def test_series_converts_time_to_datetime(account):
    result = account.series()
    with pytest.raises(AssertionError):
        for value in result:
            assert isinstance(value, (float, str, int, list, type(None)))

    for value in result:
        assert isinstance(value, (float, str, int, list, type(None), Timestamp))


def test_array_returns_instantiation_error():
    class ArrayTest(Array, contains=int):
        pass

    with pytest.raises(InstantiationFailure):
        instance = ArrayTest('ABC', 'DEF')
        result = instance[0]


def test_array_with_no_dict_does_not_error_when_attempting_get_id():
    class ArrayTest(Array, contains=int):
        pass

    instance = ArrayTest('ABC', 'DEF')
    result = instance.get_id(1)


def test_create_attribute_returns_incompatible_error():
    with pytest.raises(IncompatibleValue):
        create_attribute(AccountID, TradeID(123))

    with pytest.raises(IncompatibleValue):
        create_attribute(ArrayStr, TradeID(123))


def test_model_update():
    trade_summary = TradeSummary(**example_trade_summary)
    changed_trade_summary = TradeSummary(**example_changed_trade_summary)
    result = trade_summary.replace(**changed_trade_summary.dict(json=False))
    merged = trade_summary.dict()
    merged.update(changed_trade_summary.dict())
    assert all(map(lambda x: x in merged, result.dict().keys()))
    assert result.dict() == TradeSummary(**merged).dict()


def test_array_get_id_returns_id():
    data = json.loads(example_transactions)

    transactions = ArrayTransaction(*json.loads(example_transactions))
    assert transactions.get_id(6607).id == 6607
    assert transactions.get_id(123) == None


def test_array_get_instrument_returns_instrument():
    positions = ArrayPosition(*json.loads(example_positions))

    assert positions.get_instrument('AUD_USD').instrument == 'AUD_USD'
    assert positions.get_instrument('EUR_USD') == None

    instruments = ArrayInstrument(*json.loads(example_instruments))
    assert instruments.get_instrument('AUD_USD').name == 'AUD_USD'
    assert instruments.get_instrument('EUR_USD').name == 'EUR_USD'


def test_array_in_returns_true_when_instrument_is_present():
    positions = ArrayPosition(*json.loads(example_positions))
    assert 'AUD_USD' in positions


def test_array_in_returns_true_when_id_is_present():
    trades = ArrayTrade(*example_trade_array)
    assert 7105 in trades


def test_array_in_returns_true_when_object_is_present():
    trades = ArrayTrade(*example_trade_array)
    trade = Trade(**example_trade_array[0])
    assert trade in trades


def test_model_raises_not_implemented_when_checking_equality():
    assert (Trade(0) == '0') == False


def test_same_arrays_are_equal():
    assert ArrayTrade(*example_trade_array) == ArrayTrade(*example_trade_array)


def test_array_returns_false_checking_equality():
    assert (ArrayTrade(*example_trade_array) == 'ERROR') == False


def test_array_negative_indexing_works():
    array = ArrayTrade(*example_trade_array)
    assert array[-1] == array[len(array) - 1]


def test_array_items_cannot_be_modified():
    array = ArrayTrade(*example_trade_array)
    with pytest.raises(TypeError):
        array[0] = None


def test_array_items_cannot_be_assigned_to():
    array = ArrayTrade(*example_trade_array)
    with pytest.raises(NotImplementedError):
        array.test = 'ERROR'


def test_array_items_cannot_be_deleted_to():
    array = ArrayTrade(*example_trade_array)
    with pytest.raises(NotImplementedError):
        del array.items


def test_array_raises_index_error():
    array = ArrayTrade(*example_trade_array)
    with pytest.raises(IndexError):
        r = array[100]


def test_array_hash_returns_same_hash():
    array_1 = ArrayTrade(*example_trade_array)
    array_2 = ArrayTrade(*example_trade_array)
    assert hash(array_1) == hash(array_2)
    assert array_1 == array_2


def test_slicing_array_allows_for_equality_checking():
    array_1 = ArrayInstrument(*json.loads(example_instruments))
    array_2 = array_1[2:6:2]
    assert array_1[2] == array_2[0]
    assert array_1[4] == array_2[1]


@pytest.mark.asyncio
async def test_array_dataframe_returns_dataframe(client, server):
    # Easier to get a real response from the fake server than to mock a response
    async with client as client:
        rsp = await client.get_candles('AUD_USD')
    df = rsp.candles.dataframe()
    assert type(df) == DataFrame


@pytest.mark.asyncio
async def test_array_dataframe_converts_datetimes_to_correct_type(client, server):
    # Easier to get a real response from the fake server than to mock a response
    async with client as client:
        rsp = await client.get_candles('AUD_USD')
    df = rsp.candles.dataframe()
    assert type(df.time[0]) == pd.Timestamp

    df = rsp.candles.dataframe(datetime_format='UNIX')
    assert type(df.time[0]) == np.int64
    assert len(str(df.time[0])) == 19

    df = rsp.candles.dataframe(datetime_format='UNIX', json=True)
    assert type(df.time[0]) == str
    assert len(str(df.time[0])) == 20

    df = rsp.candles.dataframe(datetime_format='RFC3339')
    assert type(df.time[0]) == str
    assert len(str(df.time[0])) == 30

    assert type(df) == DataFrame


def test_create_attribute_raises_error_when_unable_to_construct_type():
    with pytest.raises(InstantiationFailure):
        attribute = create_attribute(int, 'This is not an int')


@pytest.mark.asyncio
async def test_array_get_instruments_returns_all_matching_objects(client, server):
    async with client as client:
        rsp = await client.list_open_trades()
        trades = rsp.trades.get_instruments('AUD_USD')
        assert len(trades) == 40
        assert type(trades) == ArrayTrade


@pytest.mark.asyncio
async def test_array_get_instruments_returns_default(client, server):
    async with client as client:
        rsp = await client.list_open_trades()
        trades = rsp.trades.get_instruments('NOTHING', 'DEFAULT')
        assert trades == 'DEFAULT'


@pytest.mark.asyncio
async def test_array_get_instrument_returns_single_object(client, server):
    async with client as client:
        rsp = await client.list_positions()
        position = rsp.positions.get_instrument('AUD_USD')
        assert type(position) == Position


@pytest.mark.asyncio
async def test_array_get_instrument_returns_default(client, server):
    async with client as client:
        rsp = await client.list_positions()
        position = rsp.positions.get_instrument('NOTHING', 'DEFAULT')

        assert position == 'DEFAULT'


@pytest.mark.asyncio
async def test_array_get_trade_id_returns_single_object(client, server):
    async with client as client:
        rsp = await client.list_orders()
        print(rsp.json())
        order = rsp.orders.get_trade_id(34543)
        assert type(order) == Order


@pytest.mark.asyncio
async def test_array_get_trade_id_returns_default(client, server):
    async with client as client:
        rsp = await client.list_orders()
        order = rsp.orders.get_trade_id('NOTHING', 'DEFAULT')
        assert order == 'DEFAULT'


@pytest.mark.asyncio
async def test_array_get_trade_id_returns_correct_object(client, server):
    async with client as client:
        rsp = await client.list_orders()
        order = rsp.orders.get_trade_id(34543, type='TAKE_PROFIT')
        assert order.type == 'TAKE_PROFIT'
        order = rsp.orders.get_trade_id(34543, type='STOP_LOSS')
        assert order.type == 'STOP_LOSS'
        order = rsp.orders.get_trade_id(34543, default='DEFAULT', type='INVALID')
        assert order == 'DEFAULT'

@pytest.mark.asyncio
async def test_array_get_trade_ids_returns_array_object(client, server):
    async with client as client:
        rsp = await client.list_orders()
        print(rsp.json())
        orders = rsp.orders.get_trade_ids(34543)
        assert type(orders) == ArrayOrder


@pytest.mark.asyncio
async def test_array_get_trade_ids_returns_default(client, server):
    async with client as client:
        rsp = await client.list_orders()
        print(rsp.json())
        orders = rsp.orders.get_trade_ids('NOTHING', 'DEFAULT')
        assert orders == 'DEFAULT'


def test_model_get_method():
    account = Account(**account_example['account'])
    assert account.get('id')
    assert account.get('doenstexist') == None
