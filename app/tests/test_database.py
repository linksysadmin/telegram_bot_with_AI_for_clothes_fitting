import pytest

from app.database.requests import db


@pytest.mark.asyncio
async def test_init_models():
    await db.init_models()


@pytest.mark.asyncio
async def test_add_user():
    await db.add_user(1, 5)
    await db.add_user(2, 5)


@pytest.mark.asyncio
async def test_add_available_generations():
    await db.add_available_generations(1, 3)


@pytest.mark.asyncio
async def test_remove_available_generation():
    await db.remove_available_generation(1)


@pytest.mark.asyncio
async def test_add_payment():
    await db.add_payment(1, 345)
    await db.add_payment(1, 234)
    await db.add_payment(2, 2341)


@pytest.mark.asyncio
async def test_get_user_data():
    res = await db.get_user_data(1)
    assert res == {'id': 1, 'available_generations': 7, 'used_generations': 1, 'datetime_registration': res['datetime_registration']}


@pytest.mark.asyncio
async def test_get_payments():
    res = await db.get_payments_of_user(1)
    assert len(res) == 2



def test_remove_user():
    db.remove_user(1)
