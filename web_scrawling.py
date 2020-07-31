'''
CoderSchool Week 1 Project

Date: 31/7/2020
Name: Lan Nguyen
Email: chi.lan1601@gmail.com

The function asks for an input of url from tiki.vn that contain a list of product and return a pandas dataframe.
It exports a csv with the following information:
    'seller_id'
    'product_brand'
    'product_id'
    'product_title'
    'price_included_sale'
    'image_url'
    'sale_percentage'

Example url: https://tiki.vn/do-ngu-be-trai/c5284/unifriend

'''

import pandas as pd
import requests
from bs4 import BeautifulSoup

def web_scrawler():

    #ask and read URL
    url_str = input()
    try: 
        page = requests.get(url_str)
    except:
        print("Error reading url")
            
    #parse the html
    soup = BeautifulSoup(page.text, 'html.parser')

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

            #check if the price include sale or not
            sale_tag = product.find('span', {'class':'sale-tag sale-tag-square'}).text
            if sale_tag:
                d['sale_percentage'] = sale_tag
                    
            #add to product_data array:
            product_data.append(d)

        except:
            # Skip if error and print error message
            print("Error reading product")


    #save product data to dataframe
    product_data = pd.DataFrame(data = product_data, columns = product_data[0].keys())
    product_data.to_csv("./product_results.csv", index=False)

web_scrawler()