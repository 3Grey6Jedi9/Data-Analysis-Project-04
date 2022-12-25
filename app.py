from sqlalchemy import (create_engine, Column, Integer, String, ForeignKey, Date)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker, relationship

import csv, datetime, sys, statistics


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
                new_product = Product(product_name=name, product_quantity=quantity, product_price=price, date_updated=date, brand_name= brand_name, brand_id=brand_id)
                session.add(new_product)
            session.commit()









def app():
    next = True
    while next:
        print('''\n\t\t\t\t*** MENU ***\r\n
        Welcome, please select an option (letter) of the following list:\r\n
        V - Details of a single product
        N - Add a new product 
        A - Analysis 
        B - Make a BACKUP of the current Database
        Q - Quit 
        ''')
        while ValueError:
            try:
                choice = input().lower()
                if choice not in ('v','n','a','b', 'q'):
                    raise ValueError('Please you must enter a valid option')
            except ValueError as err:
                print(f'{err}')
            else:
                if choice == 'v':
                    for product in session.query(Product):
                        print(f'{product.product_id}. {product.product_name}')
                    L = []
                    for p in session.query(Product.product_id):
                        L.append(p.product_id)
                    while ValueError:
                        try:
                            id = int(input('\nPlease enter the ID of the Product you want to know more about: '))
                            if id not in L:
                                raise ValueError('Please you must select a valid ID')
                            for product in session.query(Product):
                                if id == product.product_id:
                                    print(f'''\nProduct's name: {product.product_name}
                                    \rProduct's price: {product.product_price}\r
                                    \rProduct Quantity: {product.product_quantity}\r
                                    \rLast Update: {product.date_updated}
                                    \rBrand: {product.brand_name}''')
                                else:
                                    continue
                        except ValueError as err:
                            print(f'{err}')
                        else:
                            next = input('\nEnter "q" if you want to quit or any other key to going back to the MENU: ')
                            if next == 'q':
                                sys.exit()
                            else:
                                next = True
                        break
                elif choice == 'n':
                    name = input('Enter the name of the product you want to add: ')
                    quantity = int(input('Enter the quantity: '))
                    price = input('Now I need you to enter the price using this format --> $4.44: ')
                    date = datetime.datetime.now()
                    brand = input('Eventually, enter the Brand please: ')
                    B = []
                    for b in session.query(Brands.brand_name):
                        B.append(b.brand_name)
                    if brand in B:
                        continue
                    else:
                        new_brand = Brands(brand_name=brand)
                    new_product = Product(product_name=name, product_quantity=quantity, product_price=clean_price(price), date_updated=date, brand_name=brand)
                    session.add(new_brand)
                    session.add(new_product)
                    session.commit()
                elif choice == 'a':
                    # THE MOST EXPENSIVE PRODUCTS
                    P = []
                    expensive = []
                    for p in session.query(Product):
                        P.append(p.product_price)
                    highest_price = max(P)
                    for p in session.query(Product):
                        if highest_price == p.product_price:
                            expensive.append(p.product_name)
                    print(f'''\nThese are the most expensive products: ''')
                    for e in expensive:
                        print(f'{e}: ${highest_price/100}')
                    # THE CHEAPEST PRODUCTS
                    cheap = []
                    lowest_price = min(P)
                    for p in session.query(Product):
                        if lowest_price == p.product_price:
                            cheap.append(p.product_name)
                    print(f'''\nThese are the cheapest products: ''')
                    for e in cheap:
                        print(f'{e}: ${lowest_price/100}')
                    # THE MOST POPULAR BRAND
                    all_brands = []
                    for b in session.query(Product):
                        all_brands.append(b.brand_name)
                    popular = statistics.multimode(all_brands)
                    print(f'''\nThe most popular brand is {popular[0]}''')
                elif choice == 'b':
                    pass
                elif choice == 'q':
                    sys.exit()
                else:
                    pass
            break









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
    app()
    #add_brand_csv()
    #add_invent_csv()











