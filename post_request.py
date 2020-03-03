import requests, json, urllib, cookiejar, os
import pandas as pd
import http.client
import mimetypes

def read_file(file_name, save = False):
    ''' This function creates URL queries based on a text file of keywords input

    Inputs:
        file_name: path to the file containing the keywords
        save: boolean, default is false
    
    Outputs:
        df: dataframe of keywords and their encoded urls
        if save: outputs the df into a csv
    '''
    urls = []
    keywords = []
    f = open(file_name,'r', encoding = "ISO-8859-1")

    for _, line in enumerate(f):
        url = urllib.parse.quote(line.encode("ISO-8859-1").decode('utf8').strip('\n')).replace('%', '%25') #For some reason '%' needs to be replaced with '%25'
        keywords.append(line[18:].encode("ISO-8859-1").decode('utf-8').strip('\n'))
        urls.append(url)

    df = pd.DataFrame(list(zip(keywords, urls)), columns =['keyword', 'url']) 
    
    if save:
        output_path = os.path.join("data", "keywords_url.csv")
        df.to_csv(output_path)
    
    return df

def post_req(query, id, save = False):
    """ This function makes the POST request to Greatfire.Org

    Input:
        query: a URL to add into the referer header
        id: the id for a given keyword
        save: boolean, whether to save the JSON response

    Output:
        json_data: the JSON from the post request
    """
    # For debugging purposes use the sample query below.
    # sample_query = 's.weibo.com/weibo/%25E4%25B9%25A0%25EF%25BC%258B%25E5%25BE%25AE%25E8%2596%2584'
    
    conn = http.client.HTTPSConnection("en.greatfire.org")
                        
    payload = 'limit=80&url=http%3A//' + query
    headers = {
    'Accept': '*/*',
    'DNT': '1',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    conn.request("POST", "/backend/GetTestsLimit", payload, headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    json_data = json.loads(data)
    # print(json_data["urlTests"][0]["verdict"])

    if save:
        outfile_path = os.path.join('data', 'raw_data', str(id) + '.json')
        with open(outfile_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4, ensure_ascii=False) # ensure_ascii False is needed to save Chinese characters

    return json_data

if __name__ == "__main__":
    keywords_path = os.path.join('data', 'keyword_query', 'keywords_first_100.txt')
    query_df = read_file(keywords_path, save = True)
    
    for i in range(len(query_df)):
        post_req(query_df.url[i], i, save = True)
        if i == 1:
            break
