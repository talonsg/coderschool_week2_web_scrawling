import pandas as pd
import requests
from bs4 import BeautifulSoup

'''
 #Not all products on sale
        if products.find('span', {'class':'sale-tag sale-tag-square'}):
            d['sale_percentage'] = products.find('span', {'class':'sale-tag sale-tag-square'}).text 
'''
#read URL
page = requests.get('https://tiki.vn/do-ngu-be-trai/c5284/unifriend')

#parse the html
soup = BeautifulSoup(page.text, 'html.parser')

#Loop through all products
product_data = []
products = soup.find_all('div', {'class':'product-item'})
#print(products)

for product in products:
    #make a dictionary containing neccesary information
    d = {
        'seller_id':'',
        'product_brand':'',
        'product_id':'',
        'product_title':'',
        'price_included_sale':'',
        'image_url':'',
        'sale_percentage':''
    }

    #try-except block to handle errors

    try:
        
        d['seller_id'] = product['data-seller-product-id']
       
        d['product_brand'] = product['data-brand']
        
        d['product_id'] = product['product-sku']
        
        d['product_title'] = product['data-title']
                
        d['price_included_sale'] = product['data-price'] 
                
        d['image_url'] = product.find('span', {'class':'image'}).img['src']
                
        #add to product_data array:
        product_data.append(d)

    except:
        # Skip if error and print error message
        print("Error reading product")

#save product data to dataframe
product_data = pd.DataFrame(data = product_data, columns = product_data[0].keys())
product_data.to_csv("./product_results.csv", index=False)