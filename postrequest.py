from multiprocessing.dummy import Pool as ThreadPool
import requests, json, urllib, cookiejar, os
import pandas as pd
import http.client
import mimetypes
import numpy as np

from tqdm import tqdm
from datetime import datetime

class PostRequest:
    def __init__(self):
        self.key_error = 0
        self.request_error = 0
        self.num_keywords = 0

    def read_file(self,file_name, save = False):
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

    def post_req(self, query, id, save = False):
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

        # Only Proceed if response is OK 200
        if res.status == 200:
            data = res.read().decode("utf-8")
            json_data = json.loads(data)
        else:
            self.request_error += 1
            return None

        # Check if the JSON has urlTests
        try:
            json_data["urlTests"]
        except KeyError:
            self.key_error += 1
            return None

        # Only save if previous errors do not occur
        if save:
            outfile_path = os.path.join('data', 'raw_data', str(id) + '.json')
            with open(outfile_path, 'w') as json_file:
                json.dump(json_data, json_file, indent=4, ensure_ascii=False) # ensure_ascii False is needed to save Chinese characters

        return json_data
        
    def vectorize(self, json, today = False):
        """ This function creates a numpy vector representation from the JSON file based on verdicts

        Inputs:
            json: the JSON file containing the verdicts
            today: boolean, whether to count the start day as today, default is False (March 1, 2020)

        Outputs:
            vector: vector representation of the verdicts on a given day
        """       
        num_days = 365 * (2020 - 2015) + 1 # Number of Days that we care about (including leap days)
        today = datetime(2020, 3, 1) # We count March 1 as the start of the times we care about
        vector = np.zeros(num_days)

        for _, url_test in enumerate(json["urlTests"]):
            verdict = url_test["verdict"]
            date = datetime.fromtimestamp(url_test["created"] * 1/1000)
            days_ago = (today - date).days
            
            # Only record verdicts for the past num_days that we care about
            if days_ago < num_days:
                vector[days_ago] = verdict
        
        self.num_keywords += 1
        
        return vector

    def verbose(self):
        """ This function prints out the number of successfully vectorized keywords,
            key errors, and request errors.
        """
        print("Num keywords: {} \t Key errors: {} \t Request errors: {}".format(self.num_keywords,
                                                                            self.key_error,
                                                                            self.request_error))

if __name__ == "__main__":


    # Debugging code
    keywords_path = os.path.join('data', 'keyword_query', 'keywords_all.txt')
    Scraper = PostRequest()
    query_df = Scraper.read_file(keywords_path, save = True)
    vector_list = []
    label_list = []

    vector_file_path = os.path.join("data", "train", "verdicts.npy")
    label_file_path = os.path.join("data", "train", "labels.csv")

    label_file = open("./data/train/test_label.csv", "a")
    verdict_file = "./data/train/test_verdict.npy"

    for i in tqdm(range(len(query_df))):
        json_data = Scraper.post_req(query_df.url[i], i, save = False)
        if json_data:
            label_file.write(query_df.keyword[i]+'\n')
            vector = Scraper.vectorize(json_data)
            np.save(verdict_file, vector)
            # vector_list.append(vector)
            # label_list.append(query_df.keyword[i])

    Scraper.verbose()

    label_series = pd.Series(label_list)
    # label_series.to_csv(label_file_path)
    # np.save(vector_file_path, np.array(vector_list))


    
