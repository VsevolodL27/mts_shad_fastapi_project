import pytest
from fastapi import status
from sqlalchemy import select

from src.models import sellers, books


@pytest.mark.asyncio
async def test_create_seller(async_client):
    data = {
        "first_name": "dwdsqs",
        "last_name": "sadwqd", 
        "email": "wqdsdwq@mail.ru",
        "password": "dwdasdqw"
    }

    response = await async_client.post("/api/v1/sellers/", json=data)
    assert response.status_code == status.HTTP_201_CREATED

    result_data = response.json()

    assert result_data["first_name"] == data["first_name"]
    assert result_data["last_name"] == data["last_name"]
    assert result_data["email"] == data["email"]


@pytest.mark.asyncio
async def test_get_seller(db_session, async_client):
    seller = sellers.Seller(first_name="dqwdqw", last_name="dqwdqw", email="dqwdw@mail.ru", password="dwdsqws")

    db_session.add(seller)
    await db_session.flush()

    book_1 = books.Book(author="Pushkin", title="Eugeny Onegin", year=2001, count_pages=104, seller_id=seller.id)
    book_2 = books.Book(author="Lermontov", title="Mziri", year=1997, count_pages=104, seller_id=seller.id)

    db_session.add_all([book_1, book_2])
    await db_session.flush()

    response = await async_client.get(f"/api/v1/sellers/{seller.id}")
    assert response.status_code == status.HTTP_200_OK

    result_data = response.json()
    assert result_data["first_name"] == seller.first_name
    assert result_data["last_name"] == seller.last_name
    assert result_data["email"] == seller.email
    assert result_data["id"] == seller.id
    assert result_data["books"] == [
            {"id": book_1.id, "author": "Pushkin", "title": "Eugeny Onegin", "year": 2001, "count_pages": 104},
            {"id": book_2.id, "author": "Lermontov", "title": "Mziri", "year": 1997, "count_pages": 104}
        ]


@pytest.mark.asyncio
async def test_get_sellers(db_session, async_client):
    seller_1 = sellers.Seller(first_name="dwedsa", last_name="asdasd", email="asdsa@mail.ru", password="sdfs")
    seller_2 = sellers.Seller(first_name="dsvsdv", last_name="sadasd", email="asdd@mail.ru", password="sdf")

    db_session.add_all([seller_1, seller_2])
    await db_session.flush()

    response = await async_client.get("/api/v1/sellers/")

    assert response.status_code == status.HTTP_200_OK

    assert response.json() == {
        "sellers": [
            {"first_name": "dwedsa", "last_name": "asdasd", "email": "asdsa@mail.ru", "id": seller_1.id},
            {"first_name": "dsvsdv", "last_name": "sadasd", "email": "asdd@mail.ru", "id": seller_2.id}
        ]
    }


@pytest.mark.asyncio
async def test_put_seller(db_session, async_client):
    seller = sellers.Seller(first_name="dcscsd", last_name="csac", email="dsawd@mail.ru", password="wqd")

    db_session.add(seller)
    await db_session.flush()

    book_1 = books.Book(author="Pushkin", title="Eugeny Onegin", year=2001, count_pages=104, seller_id=seller.id)
    book_2 = books.Book(author="Lermontov", title="Mziri", year=1997, count_pages=104, seller_id=seller.id)

    db_session.add_all([book_1, book_2])
    await db_session.flush()
    
    response = await async_client.put(f"/api/v1/sellers/{seller.id}",
                                      json={"first_name": "sassa", "last_name": "csacas", "email": "asc@asacs.com"})
    


    assert response.status_code == status.HTTP_200_OK
    await db_session.flush()

    res = await db_session.get(sellers.Seller, seller.id)
    assert res.id == seller.id
    assert res.first_name == "sassa"
    assert res.last_name == "csacas"
    assert res.email == "asc@asacs.com"


@pytest.mark.asyncio
async def test_delete_seller(db_session, async_client):
    seller = sellers.Seller(first_name="sadas", last_name="gfbf", email="dfbfdb@dfb.com", password="bbbb")

    db_session.add(seller)
    await db_session.flush()

    book_1 = books.Book(author="Pushkin", title="Eugeny Onegin", year=2001, count_pages=104, seller_id=seller.id)
    book_2 = books.Book(author="Lermontov", title="Mziri", year=1997, count_pages=104, seller_id=seller.id)

    db_session.add_all([book_1, book_2])
    await db_session.flush()

    response = await async_client.delete(f"/api/v1/sellers/{seller.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    await db_session.flush()

    seller = await db_session.execute(select(sellers.Seller, seller.id))
    res = seller.scalars().all()
    assert len(res) == 0

    for book_id in [book_1.id, book_2.id]:
        book = await db_session.execute(select(books.Book, book_id))
        res = book.scalars().all()
        assert len(res) == 0
