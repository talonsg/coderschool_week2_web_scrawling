'''
CoderSchool Week 1 Project

Date: 02/08/2020
Name: Lan Nguyen
Email: chi.lan1601@gmail.com

'''
import argparse
import pandas as pd
import requests
from bs4 import BeautifulSoup

#define arguments input to run on bash here
parser = argparse.ArgumentParser()

parser.add_argument('-o', 
                    dest = 'output_file_name',
                    default = 'results.csv',
                    required = False,
                    help = 'Name of output csv file')

parser.add_argument('-loc', 
                    dest = 'file_location',
                    default = "./",
                    required = False,
                    help = 'Output location of csv file')

parser.add_argument('-u', 
                    dest = 'url',
                    required = True,
                    help = 'Input url for web scrawler')

parser.add_argument('-n',
                    dest = 'no_page',
                    default = 1,
                    required = False,
                    type = int,
                    help = 'Number of pages to roll over')
options = parser.parse_args()

#define functions here:

def web_scrawler(   file_name = options.output_file_name,
                    file_location = options.file_location,
                    url = options.url,
                    no_page = options.no_page):

    '''

    The web_scraweler() function takes a url from tiki.vn that contains a list of product,
    It takes the product information and rolls over the specified number of pages.
    The product data is exported as csv file.

    '''
    
    #for rolling over pages, check if end of url contains "&page=1"
    page_roller = '&page=1'
    if page_roller not in url:
        url = url + page_roller
    
    for i in range (1, no_page+1):
        url = list(url)
        url[-1] = str(i)
        url = ''.join(url)

        print(f'Scraping page {url}')

        try:
            page = requests.get(url)
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
    file_path = file_location + file_name
    print(f'Saving file to {file_path}...')
    product_data.to_csv(file_path, index=False)


#main code run here
if __name__ == '__main__':
    web_scrawler()
