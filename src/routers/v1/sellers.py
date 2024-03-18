from typing import Annotated
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.configurations.database import get_async_session
from src.schemas.sellers import ReturnedAllSellers, ReturnedSeller
from src.schemas.sellers import IncomingSeller, ReturnedAllSellers, ReturnedSeller, ReturnedSellerWithBooks
from src.schemas.books import ReturnedBookForSeller
from src.models.sellers import Seller
from src.models.books import Book
from sqlalchemy import select
from icecream import ic

sellers_router = APIRouter(tags=["sellers"], prefix="/sellers")

DBSession = Annotated[AsyncSession, Depends(get_async_session)]


@sellers_router.post("/", response_model=ReturnedSeller, status_code=status.HTTP_201_CREATED)
async def create_seller(seller: IncomingSeller, session: DBSession):
    new_seller = Seller(
        first_name=seller.first_name,
        last_name=seller.last_name,
        email=seller.email,
        password=seller.password,
    )
    session.add(new_seller)
    await session.flush()

    return new_seller


@sellers_router.get("/", response_model=ReturnedAllSellers)
async def get_all_sellers(session: DBSession):
    query = select(Seller)
    res = await session.execute(query)
    sellers = res.scalars().all()
    return {"sellers": sellers}


@sellers_router.get("/{seller_id}", response_model=ReturnedSellerWithBooks)
async def get_seller(seller_id: int, session: DBSession):
    seller = await session.get(Seller, seller_id)
    if seller is None:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    query = select(Book).filter(Book.seller_id==seller_id)
    books_ = await session.execute(query)
    books_ = books_.scalars().all()

    books_ = [ReturnedBookForSeller(id=book.id, title=book.title, author=book.author, year=book.year, count_pages=book.count_pages, seller_id = seller_id)
          for book in books_]

    seller_response = {
        "first_name": seller.first_name,
        "last_name": seller.last_name,
        "email": seller.email,
        "id": seller.id,
        "books": books_
    }

    return seller_response




@sellers_router.put("/{seller_id}")
async def update_seller(seller_id: int, new_data: ReturnedSeller, session: DBSession):
    if updated_seller := await session.get(Seller, seller_id):
        updated_seller.first_name = new_data.first_name
        updated_seller.last_name = new_data.last_name
        updated_seller.email = new_data.email

        await session.flush()

        return updated_seller

    return Response(status_code=status.HTTP_404_NOT_FOUND)

@sellers_router.delete("/{seller_id}")
async def delete_seller(seller_id: int, session: DBSession):
    deleted_seller = await session.get(Seller, seller_id)
    ic(deleted_seller)  
    if deleted_seller:
        await session.delete(deleted_seller)

    return Response(status_code=status.HTTP_204_NO_CONTENT) 
