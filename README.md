# Python3 Flask project

Get a service account token and grant that account access to your sheet

save the contents of the service token in a file 

    .data/api_credentials.json
    
Grand the email in this file access to your spreadsheets to allow it to read/write

add these to .env

    secret_key="SOMETHING"


generate secret key with:

    openssl rand -base64 24

----
    
# Requests

    GET
    /getCategories
    
    HEADER
    required args:
    secret_key (str)
    sheet_id (str)
    
Returns list of the categories which you've defined

----

    GET
    /recentInvoices
    
    HEADER
    required args:
    secret_key (str) 
    sheet_id (str)
    
    optional:
    invoice_count (int)
    
List of recent invoices that you've submitted


-----

    POST
    /submitInvoice
    
    JSON
    secret_key (str)
    sheet_id (str)
    
    data (list)
        [
            item (str),
            date (MM/dd/YYYY),
            cost (int or str),
            category (str)
        ]
        
