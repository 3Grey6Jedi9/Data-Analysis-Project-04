from sqlalchemy import (create_engine, Column, Integer, String, ForeignKey, Date)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker, relationship

import csv, datetime


engine = create_engine("sqlite:///inventory.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()



def add_brand_csv():
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




def clean_price(price):
    '''$3.19 becomes 319'''
    numeric = price.split('$')[1]
    nuf = float(numeric)
    num = int(100*nuf)
    return num


def clean_date(date):
    '''This function receives a string, such as 11/1/2019, and returns a date object'''
    date_list = date.split("/")
    date_clean = datetime.datetime(int(date_list[2]),int(date_list[0]), int(date_list[1]))
    return date_clean




def add_invent_csv():
    with open('/Users/danielmulatarancon/Desktop/Documents/HACKING TIME/*DATA ANALYSIS /Unit 04/Project 04/store-inventory/inventory.csv') as csvfile:
        data = csv.reader(csvfile)
        i = 0
        for row in data:
            if i == 0:
                i += 1
                continue
            else:
                name = row[0]
                quantity = int(row[2])
                price = clean_price(row[1])
                date = clean_date(row[3])
                brand_name = row[4]
                brand_id = 0
                for p in session.query(Brands):
                    if p.brand_name == brand_name:
                        brand_id = p.brand_id
                        break
                    else:
                        continue
                new_product = Product(product_name=name, product_quantity=quantity, product_price=price, date_updated=date, brand_id=brand_id)
                session.add(new_product)
            session.commit()









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
    brand_name = Column('Brand', String)
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
    #add_brand_csv()
    #add_invent_csv()

    #for p in session.query(Brands.brand_id):
        #print(p.brand_id)
    for p in session.query(Product.brand_id):
        print(p.brand_id)







# the way of getting the brandid is by comparing brand's names first and get the associated id