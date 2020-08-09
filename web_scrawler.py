'''
CoderSchool Week 2 Project

Date: 08/08/2020
Name: Lan Nguyen
Email: chi.lan1601@gmail.com

'''
import pandas as pd
import requests
import sqlite3
import re

from bs4 import BeautifulSoup
from pandas import DataFrame

#connect to sql server
conn = sqlite3.connect('SQL_TIKI_DATA.db')  
c = conn.cursor()

#main link to tiki
TIKI_URL = 'https://tiki.vn'

def get_url(url):

    '''
    This get_url() functions reads a url string and check via requests
    '''
    try:
        response = requests.get(url).text
        soup = BeautifulSoup(response, 'html.parser')
        return soup
    except Exception as err:
        print('ERROR BY REQUEST:', err)

def create_categories_table():
    
    '''
    create an sql table to store list of categories from tiki.vn
    '''

    #create new table
    query = """
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255),
            url TEXT, 
            parent_id INTEGER
        )
    """
    try:
        c.execute(query)
        conn.commit()
    except Exception as err:
        print('ERROR BY CREATE TABLE', err)

def create_tiki_table():
    
    '''
    create an sql table to store list of product from tiki.vn
    '''

    #create new table
    query = '''CREATE TABLE IF NOT EXISTS TIKI (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Seller_ID integer, 
                    Product_Brand text, 
                    Product_ID integer,
                    Product_Title text,
                    Price integer,
                    Sale_Percentage text,
                    Price_Pre_Sale text,
                    Category_id text
                    )              
                    '''
    try:
        c.execute(query)
        conn.commit()
    except Exception as err:
        print('ERROR BY CREATE TABLE', err)

def drop_categories_table():
    query = '''DROP TABLE CATEGORIES'''
    try:
        c.execute(query)
        conn.commit()
    except Exception as err:
        print('ERROR BY DROP TABLE', err)

def drop_tiki_table():
    query = '''DROP TABLE TIKI'''
    try:
        c.execute(query)
        conn.commit()
    except Exception as err:
        print('ERROR BY DROP TABLE', err)

def get_main_categories(save_db=False):
    
    '''
    It scrapes the homepage of tiki.vn and extracts the main categories of item
    '''

    soup = get_url(TIKI_URL)

    result = []
    counter_id = 1
    for a in soup.find_all('a', {'class': 'MenuItem__MenuLink-sc-181aa19-1 fKvTQu'}):
        name = a.find('span', {'class': 'text'}).text
        name = re.sub(r'[\ufeff\n\r\t]', " ", name)
        url = a['href']
        main_cat = Category(name = name, url = url, cat_id = counter_id)
        
        if save_db:
            main_cat.save_into_db()
        result.append(main_cat)
    return result

def get_sub_categories(parent_category, save_db=False):

    '''
    get_sub_categories() given a parent category
    '''

    parent_url = parent_category.url
    result = []

    try:
        soup = get_url(parent_url)
        div_containers = soup.find_all('div', {'class':'list-group-item is-child'})
        for div in div_containers:
            name = div.a.text

            # replace more than 2 spaces with one space
            name = re.sub('\s{2,}', ' ', name)

            sub_url = TIKI_URL + div.a['href']
            cat = Category(name, sub_url, parent_category.cat_id)
            if save_db:
                cat.save_into_db()
            result.append(cat)
    except Exception as err:
        print('ERROR BY GET SUB CATEGORIES:', err)
    return result

def get_all_categories(categories):
    
    '''
    get_all_categories() given a list of main categories (This is a recusion function)
    '''

    if len(categories) == 0:
        return
    for cat in categories:
        sub_categories = get_sub_categories(cat, save_db = True)
        get_all_categories(sub_categories)

def get_product(cat, no_page, save_db = False):

    '''
    The function takes a url from tiki.vn that contains a list of product,
    It takes the product information and rolls over the specified number of pages.
    It returns a list of product data
    '''

    url = cat.url

    #for rolling over pages, check if end of url contains "&page=1"
    page_roller = '&page=1'
    if page_roller not in url:
        url = url + page_roller 

    for i in range (1, no_page+1):
        url = list(url)
        url[-1] = str(i)
        url = ''.join(url)

        soup = get_url(url)
        print(f"Scraping page {url}")
                
        #Loop through all products
        product_data = []
        products = soup.find_all('div', {'class':'product-item'})

        for product in products:
            
            #try-except block to handle errors
            try:
                seller_id = product['data-seller-product-id']
                product_brand = product['data-brand']
                product_id = product['product-sku']
                product_title = product['data-title']
                price = product['data-price'] 

                #check if the price include sale or not
                sale_tag = product.find('span', {'class':'sale-tag sale-tag-square'}).text
                price_tag = product.find('span', {'class':'price-regular'}).text
                
                if sale_tag:
                    sale_tag = re.sub(r'[^0-9]+', '', sale_tag)
                    price_tag = re.sub(r'[^0-9]+', '', price_tag)
                else:
                    sale_tag = None
                    price_tag = None
                pro = Product(seller_id, product_brand, product_id, product_title, price, cat.cat_id, sale_tag, price_tag)
                
                if save_db:
                    pro.save_into_db()

                product_data.append(pro)
            except:
                # Skip if error and print error message
                print("Error reading product")

    return product_data

def import_csv_to_sql(path):

    #import csv file
    print(f'Importing csv file {path}...')
    data = pd.read_csv(path)
    df = pd.DataFrame(data, columns= ['id','name','url','parent_id'])

    #read into sqlite table
    df.to_sql(name="categories", con=conn, index=False, index_label="id")

def import_csv_into_class(path, cat_id):
    data = pd.read_csv()
    df = pd.DataFrame(data, columns= ['id','name','url','parent_id'])

    print(df.loc[0].at['name'])

def do_some_sql_query(save_csv = False,path = None):
    #make some sql query
    query = '''
            SELECT m.id, m.name, m.url, m.parent_id
            FROM categories AS m 
            LEFT JOIN categories AS e ON e.parent_id = m.id 
            WHERE e.name IS NULL;
            '''
    df = pd.read_sql_query(query, conn)
    print(df)

    if save_csv:
        df.to_csv(path, index=False)

class Category:

    '''
    This object stores the information of category item from tiki
    '''

    def __init__(self, name, url, parent_id=None, cat_id=None):
        self.name = name
        self.url = url
        self.parent_id = parent_id
        self.cat_id = cat_id

    def __repr__(self):
        return f"ID: {self.cat_id}, Name: {self.name}, URL: {self.url}, Parent: {self.parent_id}"

    def save_into_db(self):
        query = """
            INSERT INTO categories (name, url, parent_id)
            VALUES (?, ?, ?);
        """
        val = (self.name, self.url, self.parent_id)
        try:
            c.execute(query, val)
            self.cat_id = c.lastrowid
            conn.commit()
        except Exception as err:
            print('ERROR BY INSERT:', err)

class Product:

    '''
    This object stores the information of product item from tiki
    '''

    def __init__(self, seller_id, product_brand, product_id, product_title, price, category_id, sale_percentage = None, price_pre_sale = None):
        self.seller_id = seller_id
        self.product_brand = product_brand
        self.product_id = product_id
        self.product_title = product_title
        self.price = price
        self.sale_percentage = sale_percentage
        self.price_pre_sale = price_pre_sale
        self.category_id = category_id

    def __repr__(self):
        return f"ID: {self.product_id}, Name: {self.product_title}"

    def save_into_db(self):
        
        query = """
            INSERT INTO tiki (seller_id, product_brand, product_id, product_title, price, category_id, sale_percentage, price_pre_sale)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """
        
        val = (self.seller_id, self.product_brand, self.product_id, self.product_title, self.price, self.category_id, self.sale_percentage, self.price_pre_sale)
        try:
            c.execute(query, val)
            conn.commit()
        except Exception as err:
            print('ERROR BY INSERT:', err)

def main():
    
    '''
    Main function to execute
    '''

    # 1.create new sql table

    #create_categories_table() #only call this table if 
    create_tiki_table()

    # 2. get all the main categories off tiki
    #main_categories = get_main_categories(save_db=True)

    # 3. get all the categories (saved in categories.csv)
    #get_all_categories(main_categories)

    # 4. get the lowest ranking categories  (lowest_rank_categories.csv)
    #import_csv_to_sql(path = './categories.csv')
    #do_some_sql_query(save_csv= True, path = './lowest_rank_categories.csv')

    # 4. choose a random sub-category to scrape
    #import_csv_into_class(path = './lowest_rank_categories.csv', cat_id = 12)
    #get_product(main_categories[2], no_page = 1 , save_db= True)

    # 5. do some query
    

    # 6. drop table after reading data
    #drop_categories_table()
    drop_tiki_table()

    #close sql server
    conn.close()

if __name__ == "__main__":
    main()







