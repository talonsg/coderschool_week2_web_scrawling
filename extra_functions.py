def web_scrawler(url, no_page):

    '''
    The web_scraweler() function takes a url from tiki.vn that contains a list of product,
    It takes the product information and rolls over the specified number of pages.
    It returns a list of product data
    '''
    
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
            #make a dictionary containing neccesary information
            d = {
                'seller_id':'',
                'product_brand':'',
                'product_id':'',
                'product_title':'',
                'price':'',
                'sale_percentage':'',
                'price_pre_sale': '',
                'category':''
            }

            #try-except block to handle errors

            try:
                d['seller_id'] = product['data-seller-product-id']
                d['product_brand'] = product['data-brand']
                d['product_id'] = product['product-sku']
                d['product_title'] = product['data-title']
                d['price'] = product['data-price'] 
                d['category'] = soup.find('div',{'class':'product-box-list'})['data-impress-list-title'].split(' | ')[1]

                #check if the price include sale or not
                sale_tag = product.find('span', {'class':'sale-tag sale-tag-square'}).text
                price_tag = product.find('span', {'class':'price-regular'}).text
                
                if sale_tag:
                    sale_tag = re.sub(r'[^0-9]+', '', sale_tag)
                    price_tag = re.sub(r'[^0-9]+', '', price_tag)
                    d['sale_percentage'] = sale_tag
                    d['price_pre_sale'] = price_tag
                               
                #add to product_data array:
                product_data.append(d)

            except:
                # Skip if error and print error message
                print("Error reading product")

    return product_data

def multi_scrawler(web_list, no_page, file_name, file_location):

    '''
    The multi_scrawler() function takes a list url from tiki.vn,
    calls the web_scrawler() function to extract the data
    and adds it into a csv file
    '''

    product_data = []

    for i in range(len(web_list)):
        product_data.extend(web_scrawler(web_list[i], no_page))

    #save product data to dataframe
    product_data = pd.DataFrame(data = product_data, columns = product_data[0].keys())
    file_path = file_location + file_name
    print(f'Saving file to {file_path}...')
    product_data.to_csv(file_path, index=False)

def csv_to_sql(csv_path):

    '''
    The csv_to_sql function reads the path to a csv file containing tiki data
    and reads into a sqlite table
    '''

    # Create table - TIKI
    try:
        query = '''CREATE TABLE IF NOT EXISTS TIKI (
                    [generated_id] INTEGER PRIMARY KEY,
                    [Seller_ID] integer, 
                    [Product_Brand] text, 
                    [Product_ID] integer,
                    [Product_Title] text,
                    [Price] integer,
                    [Sale_Percentage] text,
                    [Price_Pre_Sale] text,
                    [Category] text
                    )              
                    '''
        c.execute(query)
        conn.commit()
    except Exception as err:
        print('ERROR BY CREATE TABLE', err)
                
    #import csv file
    print(f'Importing csv file {csv_path}...')
    data = pd.read_csv ("./tiki_data.csv")

    #read into sqlite table
    try:
        data.to_sql('TIKI', conn, if_exists='append', index = False)
        conn.commit()
    except:
        print('ERROR BY IMPORT CSV INTO TABLE', err)
