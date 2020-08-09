#########################################################

The code uses sql to make query about data from tiki
In the main function, the code does the following orders:
1. Create two sql tables:
    - One to hold the list of categories of products from tiki 
    - One to hold the list of products after scraping

2. Get all the main categories and its sub categories (This step is already done and saved in categories.csv)

3. Get the lowest rank subcategories (This step is already done and saved in categories.csv)

4. Get all products from a given lowest rank subcategory

5. Do some sql query based on the function do_some_sql_query()

6. Drop all the existing tables

##############################################################

There are two existing csv file on categories of products of tiki.vn from scraping the website:

1. categories.csv : contains ALL the main and subcategories

2. lowest_rank_categories.csv: contains ONLY the lowest rank subcategories

This was acquired using the following query on the categories.csv

query =     '''
            SELECT m.id, m.name, m.url, m.parent_id
            FROM categories AS m 
            LEFT JOIN categories AS e ON e.parent_id = m.id 
            WHERE e.name IS NULL;
            '''

##############################################################

The structures of the sql table:
categories (id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255),
            url TEXT, 
            parent_id INTEGER)

TIKI (  id INTEGER PRIMARY KEY AUTOINCREMENT,
        Seller_ID integer, 
        Product_Brand text, 
        Product_ID integer,
        Product_Title text,
        Price integer,
        Sale_Percentage text,
        Price_Pre_Sale text,
        Category_id integer)
