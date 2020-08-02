The web_scraweler() function takes a url from tiki.vn that contains pages of list of product,
It takes the product information and rolls over the specified number of pages.
The product data is exported as csv file with the following information:
    'seller_id'
    'product_brand'
    'product_id'
    'product_title'
    'price_included_sale'
    'image_url'
    'sale_percentage'

The code auto-assume the product page start at the first page, so the ending of url input must be strictly as following:
1. "https://tiki.vn/laptop-may-vi-tinh-linh-kien/c1846?src=c.1846.hamburger_menu_fly_out_banner"
2. "https://tiki.vn/laptop-may-vi-tinh-linh-kien/c1846?src=c.1846.hamburger_menu_fly_out_banner&page=1"

To run the code: 
python  web_scrawler.py -loc "output file path" -o "output csv file" -n "number of rolling pages" -u "url"

Set by default:
-loc = "./"
-o = "results.csv"
-n = 1
-u is required 

Example:
python web_scrawler.py -loc "./" -o "results.csv" -n "5" -u "https://tiki.vn/laptop-may-vi-tinh-linh-kien/c1846?src=c.1846.hamburger_menu_fly_out_banner"




