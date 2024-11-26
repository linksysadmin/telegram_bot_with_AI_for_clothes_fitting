import asyncio
import logging
from typing import Dict, Sequence

import sqlalchemy
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import DATABASE
from app.database.models import UsersORM, Base, PaymentsORM


class Database:

    def __init__(self):
        self.__async_engine = create_async_engine(
            url=DATABASE,
            # echo=True,
        )
        self.__async_session_factory = async_sessionmaker(self.__async_engine)
        asyncio.run(self._init_models())

    async def _init_models(self) -> None:
        """
        Создает базу данных с таблицами
        :return:
        """
        async with self.__async_engine.begin() as conn:
            # await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    async def add_user(self, user_id: int, available_generations: int = 4) -> None:
        """
        Добавляет пользователя в БД с определенным количеством генераций
        :param user_id: ID пользователя
        :param available_generations: Доступные генерации
        :return: None
        """

        try:
            async with self.__async_session_factory() as session:
                user = UsersORM(
                    id=user_id,
                    available_generations=available_generations,
                    used_generations=0
                )
                session.add(user)
                # session.add_all([user, ])
                await session.commit()
        except sqlalchemy.exc.IntegrityError:
            logging.error('Уже есть пользователь в Базе Данных')
        except sqlalchemy.exc.OperationalError:
            logging.error('Базы Данных или таблицы не существует')


    async def remove_user(self, user_id: int) -> None:
        """
        Удаляет пользователя из БД
        :param user_id: ID пользователя
        :return: None
        """
        async with self.__async_session_factory() as session:
            user = await session.get(UsersORM, user_id)
            payments = await session.execute(select(PaymentsORM).where(PaymentsORM.user_id == user_id))
            for payment in payments.scalars():
                await session.delete(payment)
            await session.delete(user)
            await session.commit()




    async def get_user_data(self, user_id: int) -> Dict:
        """
        Получает данные пользователя из Базы Данных
        :param user_id: ID пользователя
        :return: Словарь с данными пользователя по ключам согласно таблице БД.
        - id
        - available_generations
        - used_generations
        - datetime_registration
        """
        try:
            async with self.__async_session_factory() as session:
                user_data = await session.get(UsersORM, user_id)
                return {
                    'id': user_data.id,
                    'available_generations': user_data.available_generations,
                    'used_generations': user_data.used_generations,
                    'datetime_registration': user_data.datetime_registration,
                }
        except AttributeError:
            logging.error("Пользователя не существует в базе данных")
            return {}

    async def add_available_generations(self, user_id: int, num: int) -> None:
        """
        Добавляет заданное количество генераций изображений

        :param user_id: ID пользователя
        :param num: Количество генераций
        :return: None
        """
        try:
            async with self.__async_session_factory() as session:
                user_data = await session.get(UsersORM, user_id)
                user_data.available_generations += num
                await session.commit()
        except AttributeError:
            logging.error("Пользователя не существует в базе данных")

    async def remove_available_generation(self, user_id: int) -> None:
        """
        Удаляет 1 генерацию изображения из доступных (available_generations)
        и добавляет 1 в использованные (used_generations)

        :param user_id: ID пользователя
        :return: None
        """
        try:
            async with self.__async_session_factory() as session:
                user_data = await session.get(UsersORM, user_id)
                user_data.available_generations -= 1
                user_data.used_generations += 1
                await session.commit()
        except AttributeError:
            logging.error("Пользователя не существует в базе данных")

    async def add_payment(self, user_id: int, total_amount: int, generations: int) -> None:
        """
        Добавляет платеж в БД
        :param user_id: ID пользователя
        :param total_amount: Сумма платежа
        :param generations: Кол-во генераций
        :return: None
        """

        try:
            async with self.__async_session_factory() as session:
                payment = PaymentsORM(
                    user_id=user_id,
                    total_amount=total_amount,
                    generations=generations,
                )
                session.add(payment)
                await session.commit()
        except sqlalchemy.exc.OperationalError:
            logging.error('Базы Данных или таблицы не существует')


    async def get_payments_of_user(self, user_id: int) -> Sequence[PaymentsORM]:
        """
        Извлекает все платежи определенного пользователя
        :param user_id: ID пользователя
        :return: None
        """

        async with self.__async_session_factory() as session:
            query = select(PaymentsORM).where(PaymentsORM.user_id == user_id)
            result = await session.execute(query)
            payments = result.scalars().all()
            return payments


db = Database()


