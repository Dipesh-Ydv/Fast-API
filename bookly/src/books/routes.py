from fastapi import APIRouter, status, HTTPException, Depends
from typing import List
from src.books.schemas import BookSchema, BookUpdateSchema, BookCreateSchema
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import BookService

book_router = APIRouter()
book_service = BookService()

@book_router.get('/', response_model=List[BookSchema], status_code=status.HTTP_200_OK)
async def get_all_books(session: AsyncSession = Depends(get_session)):
    books = await book_service.get_all_books(session)
    return books


@book_router.post('/', response_model=BookSchema, status_code=status.HTTP_201_CREATED)
async def add_book(book_data: BookCreateSchema, session: AsyncSession = Depends(get_session)):
    new_book = await book_service.create_book(book_data, session)
    return new_book


@book_router.get('/{book_uid}', response_model=BookSchema, status_code=status.HTTP_200_OK)
async def get_book(book_uid: str, session: AsyncSession = Depends(get_session)) -> dict:
    book = await book_service.get_book(book_uid, session)
    if book:
        return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@book_router.patch('/{book_uid}', response_model=BookSchema, status_code=status.HTTP_200_OK)
async def update_book(book_uid: str, book_update_data: BookUpdateSchema, session: AsyncSession = Depends(get_session)) -> dict:
    updated_book = await book_service.update_book(book_uid, book_update_data, session)
    if updated_book:
        return updated_book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@book_router.delete('/{book_uid}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid: str, session: AsyncSession = Depends(get_session)):
    deleted_book = await book_service.delete_book(book_uid, session)
    if deleted_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found") 
    return {}