import pytest

from app.database.requests import db





@pytest.mark.asyncio
async def test_add_user():
    await db.add_user(user_id=1, available_generations=5)
    await db.add_user(user_id=2, available_generations=5)


@pytest.mark.asyncio
async def test_add_available_generations():
    await db.add_available_generations(1, 3)


@pytest.mark.asyncio
async def test_remove_available_generation():
    await db.remove_available_generation(1)


@pytest.mark.asyncio
async def test_add_payment():
    await db.add_payment(user_id=1, total_amount=179, generations=10)
    await db.add_payment(user_id=1, total_amount=279, generations=30)
    await db.add_payment(user_id=2, total_amount=379, generations=50)


@pytest.mark.asyncio
async def test_get_user_data():
    res = await db.get_user_data(user_id=1)
    assert res == {'id': 1, 'available_generations': 7, 'used_generations': 1, 'datetime_registration': res['datetime_registration']}


@pytest.mark.asyncio
async def test_get_payments():
    res = await db.get_payments_of_user(user_id=1)
    assert len(res) == 2



@pytest.mark.asyncio
async def test_remove_user():
    await db.remove_user(1)
