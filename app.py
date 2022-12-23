from sqlalchemy import (create_engine, Column, Integer, String, ForeignKey)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker, relationship


engine = create_engine("sqlite:///inventory.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Brands(Base):
    __tablename__ = "brands"

    brand_id = Column(Integer, primary_key = True)
    brand_name = Column(String)

    def __repr__(self):
        return f'''Brand Name: {self.brand_name}'''


class Product(Base):
    __tablename__ = "products"




if __name__ == '__main__':
    pass

