The code uses sql to make query about data from tiki
In the main function, the code does the following orders:
1. Create two sql tables:
    - One to hold the list of categories of products from tiki
    - One to hold the list of products after scraping

2. Get all the main categories

3. Get the sub categories of a main category (This only gets the next-level subcatogories)

4. Get all products from a given category (The category id of the product is based on the given category)

5. Do some sql query based on the function do_some_sql_query()

6. Drop all the existing tables

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
        Category_id text)
