"""Database tables description (ORM)
"""
from sqlalchemy import Column, ForeignKey, Integer, SmallInteger, String
from sqlalchemy.orm import relationship

from .database import Base


class Author(Base):
    __tablename__ = 'author'
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True)
    fullname = Column(String(150))

    def to_dict(self) -> dict:
        """Convert row-object from "author" table to dict

        Returns:
            row-object from "author" table as dict
        """
        return {
            'author_id': self.id,
            'fullname': self.fullname
        }

    @classmethod
    def fromdict(cls, author_info: dict) -> 'Author':
        """Create row-object of "author" table from dict

        Args:
            author_info: info about author

        Returns:
            Row-object of "author" table
        """
        return cls(fullname=author_info.get('fullname'))


class Book(Base):
    __tablename__ = 'book'
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    publication_year = Column(SmallInteger)
    author_id = Column(Integer, ForeignKey('author.id'))
    author = relationship('Author', backref='books', lazy='joined')

    def to_dict(self, all_data=True) -> dict:
        """Convert row-object from "book" table to dict

        Args:
            all_data: add data from linked tables

        Returns:
            row-object from "book" table as dict
        """
        book = {
            'book_id': self.id,
            'title': self.title,
            'pub_year': self.publication_year,
            'author_id': self.author_id
        }

        if all_data:
            book.update(self.author.to_dict()
                        if self.author_id else {'fullname': None})

        return book

    @classmethod
    def fromdict(cls, book_info: dict) -> 'Book':
        """Create row-object of "book" table from dict

        Args:
            book_info: info about book

        Returns:
            Row-object of "book" table
        """
        return cls(title=book_info.get('title'),
                   publication_year=book_info.get('pub_year'),
                   author_id=book_info.get('author_id'))
