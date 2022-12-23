from sqlalchemy import (create_engine, Column, Integer, String, ForeignKey, Date)

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

    product_id = Column(Integer, primary_key = True)
    product_name = Column(String)
    product_quantity = Column(Integer)
    product_price = Column(Integer)
    date_updated = Column(Date)
    brand_id = Column(Integer, ForeignKey("brands.brand_id"))

    def __repr__(self):
        return f'''Product Name: {self.product_name}\r
        Product Quantity: {self.product_quantity}\r
        Product Price: {self.product_price}\r
        Last Updated: {self.date_updated}\r
         '''



if __name__ == '__main__':
    Base.metadata.create_all(engine)


