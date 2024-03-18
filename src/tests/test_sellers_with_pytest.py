import pytest
from fastapi import status
from sqlalchemy import select

from src.models import books
from src.models import sellers


# Тест на ручку создающую продавца
@pytest.mark.asyncio
async def test_create_seller(async_client):
    data = {"first_name": "Tatyana", "last_name": "Mikheeva", "email": "tanya@mail.ru", "password": "tanyaqwerty"}
    response = await async_client.post("/api/v1/sellers/", json=data)

    assert response.status_code == status.HTTP_201_CREATED

    result_data = response.json()

    assert result_data == {
        "first_name": "Tatyana",
        "last_name": "Mikheeva",
        "email": "tanya@mail.ru",
        "id": result_data["id"]
    }

    result_data = response.json()

# Тест на ручку получения списка продавцов
@pytest.mark.asyncio
async def test_get_sellers(db_session, async_client):
    seller_1 = sellers.Seller(first_name="Pushkin", last_name="Onegin", email="hehe@mail.ru", password='qwerty')
    seller_2 = sellers.Seller(first_name="Ruslan", last_name="Puskiv", email="oneg@mail.ru", password='dfgh')

    db_session.add_all([seller_1, seller_2])
    await db_session.flush()

    response = await async_client.get("/api/v1/sellers/")

    assert response.status_code == status.HTTP_200_OK

    assert response.json() == {
        "sellers": [
            {"first_name":"Pushkin", "last_name":"Onegin", "email":"hehe@mail.ru", "id": seller_1.id},
            {"first_name":"Ruslan", "last_name":"Puskiv", "email":"oneg@mail.ru","id": seller_2.id},
        ]
    }


# Тест на ручку получения одного продавца со всеми его книгами
@pytest.mark.asyncio
async def test_get_single_seller_with_books(db_session, async_client):
    seller = sellers.Seller(first_name="Pushkin", last_name="Onegin", email="hehe@mail.ru", password='qwerty')

    db_session.add(seller)
    await db_session.flush()

    book = books.Book(author="Pushkin", title="Eugeny Onegin", year=2001, count_pages=104, seller_id=seller.id)
    book_2 = books.Book(author="Lermontov", title="Mziri", year=1997, count_pages=104, seller_id=seller.id)

    db_session.add_all([book, book_2])
    await db_session.flush()

    response = await async_client.get(f"/api/v1/sellers/{seller.id}")

    assert response.status_code == status.HTTP_200_OK

    # Проверяем интерфейс ответа, на который у нас есть контракт.
    assert response.json() == {
                                    "first_name": "Pushkin",
                                    "last_name": "Onegin",
                                    "email": "hehe@mail.ru",
                                    "id": seller.id,
                                    "books": [
                                        {
                                            "id": book.id,
                                            "title": "Eugeny Onegin",
                                            "author": "Pushkin",
                                            "year": 2001,
                                            "count_pages": 104
                                        },
                                        {
                                            "id": book_2.id,
                                            "title": "Mziri",
                                            "author": "Lermontov",
                                            "year": 1997,
                                            "count_pages": 104
                                        }
                                    ]
                                }



# Тест на ручку удаления продавца
@pytest.mark.asyncio
async def test_delete_seller(db_session, async_client):
    seller = sellers.Seller(first_name="Pushkin", last_name="Onegin", email="hehe@mail.ru", password='qwerty')

    db_session.add(seller)
    await db_session.flush()

    response = await async_client.delete(f"/api/v1/sellers/{seller.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    await db_session.flush()

    all_sellers = await db_session.execute(select(sellers.Seller))
    res = all_sellers.scalars().all()
    assert len(res) == 0


# Тест на ручку обновления продавца
@pytest.mark.asyncio
async def test_update_seller(db_session, async_client):

    seller_1 = sellers.Seller(first_name="Pushkin", last_name="Onegin", email="hehe@mail.ru", password='qwerty')
    db_session.add(seller_1)
    await db_session.flush()

    response = await async_client.put(
        f"/api/v1/sellers/{seller_1.id}",
        json={"first_name":"Ruslan", "last_name":"Puskiv", "email":"oneg@mail.ru", "id": seller_1.id},
    )

    assert response.status_code == status.HTTP_200_OK
    await db_session.flush()

    # Проверяем, что обновились все поля
    res = await db_session.get(sellers.Seller, seller_1.id)
    assert res.first_name == "Ruslan"
    assert res.last_name == "Puskiv"
    assert res.email == "oneg@mail.ru"
    assert res.id == seller_1.id