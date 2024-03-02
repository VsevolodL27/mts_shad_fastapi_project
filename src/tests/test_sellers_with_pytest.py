import pytest
from fastapi import status
from sqlalchemy import select

from src.models import books, sellers


@pytest.mark.asyncio
async def test_register_seller(async_client):
    data = {
        "first_name": "John",
        "last_name": "Johnson",
        "email": "jj13@gmail.com",
        "password": "johnLov13"
    }

    response = await async_client.post("/api/v1/sellers/", json=data)

    assert response.status_code == status.HTTP_201_CREATED

    result_data = response.json()

    assert "id" in result_data
    assert result_data["first_name"] == "John"
    assert result_data["last_name"] == "Johnson"
    assert result_data["email"] == "jj13@gmail.com"
    assert "password" not in result_data 


@pytest.mark.asyncio
async def test_get_all_sellers(db_session, async_client):
    response = await async_client.get("/api/v1/sellers/")

    start_len = len(response.json()["sellers"])

    seller_1 = sellers.Seller(first_name= "John",
        last_name ="Johnson",
        email = "jj13@gmail.com",
        password = "london99$$")
    
    seller_2 = sellers.Seller(first_name = "Vasiliy",
        last_name = "Terkin",
        email = "vasya_winner@yandex.ru",
        password = "Berlin1945Win")

    db_session.add_all([seller_1, seller_2])
    await db_session.flush()


    response = await async_client.get("/api/v1/sellers/")
    assert response.status_code == status.HTTP_200_OK

    result_data = response.json()

    assert "sellers" in result_data
    assert len(result_data["sellers"]) == start_len + 2

    expected_seller_1 = {
            "first_name": "Vasiliy",
            "last_name": "Terkin",
            "email": "vasya_winner@yandex.ru",
            "id": seller_2.id
        }
    
    expected_seller_2 ={
            "first_name": "John",
            "last_name": "Johnson",
            "email": "jj13@gmail.com",
            "id": seller_1.id
        }
    

    assert expected_seller_1 in result_data["sellers"] 
    assert expected_seller_2 in result_data["sellers"] 


@pytest.mark.asyncio
async def test_get_seller(db_session, async_client):
    seller_data = {
        "first_name": "Max",
        "last_name": "Kotov",
        "email": "kotov_m@yandex.ru",
        "password": "best12345"
    }

    response = await async_client.post("/api/v1/sellers/", json=seller_data)
    seller_id = response.json()["id"]
    book = books.Book(author="M. A. Bulgakov", title="White guardia", year=1924, count_pages=200, seller_id = seller_id)

    db_session.add(book)
    await db_session.flush()
    response = await async_client.get(f"/api/v1/sellers/{seller_id}")

    assert response.status_code == status.HTTP_200_OK

    result_data = response.json()


    assert "id" in result_data
    assert result_data["first_name"] == "Max"
    assert result_data["last_name"] == "Kotov"
    assert result_data["email"] == "kotov_m@yandex.ru"
    assert result_data["books"] == [
        {
            "id": book.id,
            "title": "White guardia",
            "author": "M. A. Bulgakov",
            "count_pages": 200,
            "year": 1924,
            "seller_id": seller_id
        }
    ]

    assert "password" not in result_data  

@pytest.mark.asyncio
async def test_update_seller(db_session, async_client):
    seller = sellers.Seller(first_name= "Ivan",
        last_name ="Ivanov",
        email = "ivanov@mail.ru",
        password = "pa$$word"
    )
    
    db_session.add(seller)
    await db_session.flush()

    
    new_data = {
        "first_name": "Igor",
        "last_name": "Michailov",
        "email": "i_mich00@yandex.ru",
        "id": seller.id
    }

    response = await async_client.put(f"/api/v1/sellers/{seller.id}", json=new_data)

    assert response.status_code == status.HTTP_200_OK

    result_data = response.json()

    assert "id" in result_data
    assert result_data["first_name"] == "Igor"
    assert result_data["last_name"] == "Michailov"
    assert result_data["email"] == "i_mich00@yandex.ru"
    assert "password" not in result_data  

@pytest.mark.asyncio
async def test_delete_seller(db_session, async_client):
    seller = {
        "first_name": "Petr",
        "last_name": "Petrov",
        "email": "petrov_petr@google.com",
        "password": "87654321"
    }
    
    all_sellers = await db_session.execute(select(sellers.Seller))
    before_sellers = len(all_sellers.unique().scalars().all()) 

    all_books = await db_session.execute(select(books.Book))
    before_books =  len(all_books.scalars().all())

    response= await async_client.post("/api/v1/sellers/", json=seller)
    seller_id = response.json()["id"]
    book = books.Book(author="M. A. Bulgakov", title="Master and Margarita", year=1930, count_pages=198, seller_id = seller_id)

    db_session.add(book)
    await db_session.flush()
    

    response = await async_client.delete(f"/api/v1/sellers/{seller_id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    await db_session.flush()

    all_sellers = await db_session.execute(select(sellers.Seller))
    assert len(all_sellers.unique().scalars().all()) == before_sellers

    all_books = await db_session.execute(select(books.Book))
    assert len(all_books.scalars().all()) == before_books
