from sqlalchemy import (create_engine, Column, Integer, String, ForeignKey, Date)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker, relationship

import csv


engine = create_engine("sqlite:///inventory.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# brandcsv = with open (...file path...) as brandcsv

# inventorycsv = with open (...) as inventorycsv

# def add_csv(file):
    # with open (file) as ...:
    # .....


def add_csv():
    with open('/Users/danielmulatarancon/Desktop/Documents/HACKING TIME/*DATA ANALYSIS /Unit 04/Project 04/store-inventory/brands.csv') as csvfile:
        data = csv.reader(csvfile)
        i = 0
        for row in data:
            if i == 0:
                i += 1
                continue
            else:
                name = row[0]
                new_brand = Brands(brand_name=name)
                session.add(new_brand)
            session.commit()





def inventory_cleaner():
    pass


def app():
    pass






class Brands(Base):
    __tablename__ = "brands"

    brand_id = Column(Integer, primary_key = True)
    brand_name = Column('Brand Name',String)

    def __repr__(self):
        return f'''Brand Name: {self.brand_name}'''


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key = True)
    product_name = Column('Name', String)
    product_quantity = Column('Product Quantity', Integer)
    product_price = Column('Product Price',Integer)
    date_updated = Column('Last Updated',Date)
    brand_id = Column(Integer, ForeignKey("brands.brand_id"))

    def __repr__(self):
        return f'''Product Name: {self.product_name}\r
        Product Quantity: {self.product_quantity}\r
        Product Price: {self.product_price}\r
        Last Updated: {self.date_updated}\r
         '''



if __name__ == '__main__':
    Base.metadata.create_all(engine)
    #app()
    add_csv()

    for p in session.query(Brands.brand_name):
        print(p.brand_name)


