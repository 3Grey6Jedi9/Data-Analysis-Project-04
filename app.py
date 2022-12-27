from sqlalchemy import (create_engine, Column, Integer, String, ForeignKey, Date)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker, relationship

import csv, datetime, sys, statistics


engine = create_engine("sqlite:///inventory.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Open files and put them into the repo; Put the functions inside app() and try all


def add_brand_csv():
    with open('brands.csv') as csvfile:
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



def unclean_price(cents):
    '''Take a price given in cents of a dollar and returns a price in this format --> $4.44'''
    dollars = cents/100
    fdollars = '$'+str(dollars)
    return fdollars

def unclean_date():
    pass






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
    with open('inventory.csv') as csvfile:
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



def most_valuable():
    product_names = []
    prices = []
    amounts = []
    value = []
    for p in session.query(Product):
        product_names.append(p.product_name)
        prices.append(p.product_price)
        amounts.append(p.product_quantity)
        value.append(p.product_price * p.product_quantity)
    most = max(value)
    idx = ''
    j = 0
    for i in value:
        if i == most:
            idx = j
        else:
            j += 1
            continue
    s = sum(value)/100
    print(f'''\nThe most valuable item in the inventory is {product_names[idx]} with a total value of ${value[idx]/100}
    \rWhich means that this item represents a {((value[idx]/100)/s)*100}% of the total value of the assets of the inventory''')









def app():
    b_verify = []
    p_verify = []
    for p in session.query(Product):
        p_verify.append(p.product_name)
    for b in session.query(Brands):
        b_verify.append(b.brand_name)
    if len(b_verify) == 0:
        add_brand_csv()
    if len(p_verify) == 0:
        add_invent_csv()
    next = True
    while next:
        print('''\n\t\t\t\t\033[1m*** MENU ***\033[0m\r\n
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
                                    action = input('\nWould you like to modify[M] or delete[D] this product?: ').lower()
                                    if action == 'm':
                                        T = True
                                        while T:
                                            try:
                                                quantity = int(input('Enter the new amount: '))
                                                if type(quantity) != int:
                                                    raise TypeError('Please enter an Integer')
                                            except:
                                                print(f'Please you must enter an Integer')

                                            else:
                                                T = False
                                        ep = True
                                        while ep:
                                            try:
                                                price = int(input('Now I need you to enter the new price in cents of a dollar so $4.44 would be --> 444: '))
                                            except:
                                                print('Enter an Integer please')
                                            else:
                                                ep = False
                                        date = datetime.datetime.now()
                                        brand = input('Eventually, enter the new Brand please: ')
                                        product.product_quantity = quantity
                                        product.product_price = price
                                        product.date_updated = date
                                        product.brand_name = brand
                                    elif action == 'd':
                                        sure = input('Are you sure you want to delete this product (enter "yes" to delete or press any other key to continue)? ').lower()
                                        if sure == 'yes':
                                            session.delete(product)
                                        else:
                                            break
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
                    eq = True
                    while eq:
                        try:
                            quantity = int(input('Enter the quantity: '))
                        except:
                            print('You must enter an Integer please')
                        else:
                            eq = False
                    erp = True
                    while erp:
                        try:
                            price = int(input('Now I need you to enter the price in cents of a dollar so $4.44 would be --> 444: '))
                        except:
                            print('You must enter an Integer please')
                        else:
                            erp = False
                    date = datetime.datetime.now()
                    brand = input('Eventually, enter the Brand please: ')
                    B = []
                    for b in session.query(Brands.brand_name):
                        B.append(b.brand_name)
                    if brand in B:
                        continue
                    else:
                        new_brand = Brands(brand_name=brand)
                        session.add(new_brand)
                    pro = []
                    for p in session.query(Product.product_name):
                        pro.append(p.product_name)
                    if name in pro:
                        for p in session.query(Product):
                            if p.product_name == name:
                                p.product_name = name
                                p.product_quantity = quantity
                                p.product_price = price
                                p.date_updated = date
                                p.brand_name = brand
                                break
                            else:
                                continue
                    else:
                        new_product = Product(product_name=name, product_quantity=quantity, product_price=price, date_updated=date, brand_name=brand)
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
                    # THE MAIN ASSET
                    most_valuable()
                elif choice == 'b':
                    with open('inventory_backup.csv', 'w') as csvfile:
                        fieldnames = ['Name', 'Price','Quantity','Last Update', 'Brand']
                        productwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        productwriter.writeheader()
                        data = []
                        for p in session.query(Product):
                            data.append({'Name':p.product_name,
                                         'Price':unclean_price(p.product_price),
                                         'Quantity':p.product_quantity,
                                         'Last Update':p.date_updated,
                                         'Brand':p.brand_name})
                        productwriter.writerows(data)
                    with open('brands_backup.csv', 'w') as csvfile:
                        fieldnames = ['Brand Name']
                        productwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        productwriter.writeheader()
                        data = []
                        for p in session.query(Brands):
                            data.append({'Brand Name':p.brand_name})
                        productwriter.writerows(data)
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

#START EXECUTING THE add_brand_csv() & add_invent_csv() FUNCTIONS TO ADD CONTENT INTO THE DATABASE AND THEN DISABLE THOSE FUCNTIONS
# AND ACTIVATE THE APP() FUNCION TO RUN THE APP

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    #app()


