from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from .schemas import BookCreateSchema, BookUpdateSchema
from .models import BookModel

class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(BookModel).order_by(desc(BookModel.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_book(self, book_uid: str, session: AsyncSession):
        statement = select(BookModel).where(BookModel.uid == book_uid)
        result = await session.exec(statement)
        return result.first()

    async def create_book(self, book_data: BookCreateSchema, session: AsyncSession):
        book_data_dict = book_data.model_dump()
        new_book = BookModel(**book_data_dict)
        session.add(new_book)
        await session.commit()
        return new_book 

    async def update_book(self, book_uid: str, update_data: BookUpdateSchema, session: AsyncSession):
        book_to_update = await self.get_book(book_uid, session)
        update_data_dict = update_data.model_dump()
        for k, v in update_data_dict.items():
            setattr(book_to_update, k, v)
        await session.commit()
        return book_to_update

    async def delete_book(self, book_uid: str, session: AsyncSession):
        book_to_delete = await self.get_book(book_uid, session)
        if book_to_delete:
            await session.delete(book_to_delete)
            await session.commit()
            return book_to_delete
        return None