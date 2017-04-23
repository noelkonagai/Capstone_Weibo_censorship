import requests, json, urllib, cookiejar

queries = {}

### below is the code for reading in the censored keywords
def read_file():

    f = open('censored_keywords_100.csv','r', encoding = "ISO-8859-1")
    i = 0

    for line in f:
        query = urllib.parse.quote(line.encode('utf8'))
        queries[i] = query
        i += 1

    print(i)
    
    return queries

### below is the code for making the post requests

def post_req(query, i):
    url = "https://en.greatfire.org/backend/GetTestsLimit"

    body = {
        "url" : "http://" + query,
        "limit" : '80',
        }

    headers = {
    'accept': "*/*",
    'origin': "https://en.greatfire.org",
    'x-devtools-emulate-network-conditions-client-id': "a5adc3d0-539d-4a31-a640-df5888f9ab3d",
    'x-requested-with': "XMLHttpRequest",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    'content-type': "application/x-www-form-urlencoded",
    'referer': "https://en.greatfire.org/" + query,
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "en-US,en;q=0.8,hu;q=0.6",
    'cookie': "__cfduid=db83a804b42f11f8c572f0eaeecac62961486457327; __uvt=; _ga=GA1.2.2005229289.1486457336; __atuvc=84%7C6%2C28%7C7%2C4%7C8; __atuvs=58a9937ce00f8257003; __utmt=1; __utma=146067563.2005229289.1486457336.1486967185.1487508314.14; __utmb=146067563.5.10.1487508314; __utmc=146067563; __utmz=146067563.1486697085.8.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); uvts=5d2yG9D0jQHGD9xE; has_js=1; __uvt=; _ga=GA1.2.2005229289.1486457336; __utmt=1; __atuvc=84%7C6%2C28%7C7%2C8%7C8; __atuvs=58aa6f5ccb59633a002; __utma=146067563.2005229289.1486457336.1487508314.1487564637.15; __utmb=146067563.4.10.1487564637; __utmc=146067563; __utmz=146067563.1486697085.8.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); uvts=5d2yG9D0jQHGD9xE; __cfduid=df4608ed2faa9a5f31c8b78dccd1d36e81487564736; has_js=1",
    'cache-control': "no-cache",
    'postman-token': "80eefb18-4368-5504-d5c2-91462a8f3544"
    }

    r = requests.post(url, data = body, headers=headers)

    JSON_response = r.json()

    with open(str(i) + '.json', 'w') as outfile:
        json.dump(JSON_response, outfile)

    return JSON_response

read_file()
# post_req()

# for i in range(3):
#     post_req(queries[i], i)
