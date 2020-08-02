The web_scraweler() function takes a url from tiki.vn that contains a list of product and returns a pandas dataframe.
It exports a csv with the following information:
    'seller_id'
    'product_brand'
    'product_id'
    'product_title'
    'price_included_sale'
    'image_url'
    'sale_percentage'

To run the code: 
python  web_scrawler.py -loc "output file path" -o "output csv file" -u "url"

Set by default:
-loc = "./"
-o = "results.csv"
-u is required 

Example:
python web_scrawler.py web_scrawler -loc "./" -o "results.csv" -u "https://tiki.vn/do-ngu-be-trai/c5284/unifriend"
