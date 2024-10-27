from datetime import datetime

def clean_currency(item: str) -> float:
    '''
    remove anything from the item that prevents it from being converted to a float
    '''    
    for i in item:
        if i not in '0123456789.':
            item = item.replace(i, '')
    return float(item)

def extract_year_mdy(timestamp):
    '''
    use the datatime.strptime to parse the date and then extract the year
    '''
    date = datetime.strptime(timestamp, "%m/%d/%Y %H:%M:%S")
    year = date.year
    return year

def clean_country_usa(item: str) ->str:
    '''
    This function should replace any combination of 'United States of America', USA' etc.
    with 'United States'
    '''
    possibilities = [
        'united states of america', 'usa', 'us', 'united states', 'u.s.'
    ]
    if item.strip().lower() in possibilities:
        item = "United States"
    
    return item


if __name__=='__main__':
    print("""
        Add code here if you need to test your functions
        comment out the code below this like before sumbitting
        to improve your code similarity score.""")

    country = "us" 
    cleaned = clean_country_usa(country)
    print(cleaned)
    date = "06/17/27"
    
