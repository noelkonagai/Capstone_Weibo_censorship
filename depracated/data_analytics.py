import json, csv, urllib
from pprint import pprint
from matplotlib import pyplot as plt
from datetime import datetime

num = 31162
datapoints = 0
time_series = {}

def import_exceptions():

	'''
	as exceptions have occurred during the data collection, this function handles them and creates a list of valid word_ids
	'''
	
	with open('exceptions.txt', 'r') as infile:
		data = list(csv.reader(infile))[0]

	results = list(map(int, data))

	return(results)

errors = import_exceptions()

def create_filenames(error_list):

	'''
	with the help of the error list, we create a file name list which we use to read in the 31162 JSON files
	'''

	file_names = []

	for i in range(num):
		if i not in error_list:
			file_names.append(str(i) + '.json')

	return file_names

file_names = create_filenames(errors)

time_series = {}

indices = []

def clean_data(file_name, index):

	'''
	with this function, we open each of the JSON file and extract relevant data into our dictionaries
	'''

	global datapoints, time_series

	path = "JSON Files/" + file_name

	with open(path) as f:
		data = json.load(f)

	time_series[index] = {}

	times = []
	verdicts = []
	url = urllib.parse.unquote(data["url"])

	time_series[index]["url"] = url

	sum_verdicts = 0
	num_verdicts = 0
	sum_sq_verdicts = 0

	verdict_dict = {}

	# looping through the JSON file and saving relevant data into a dictionary
	for i in range(len(data["urlTests"])):
		verdict = data["urlTests"][i]["verdict"]
		date = datetime.fromtimestamp(data["urlTests"][i]["created"] * 1/1000)

		sum_verdicts += verdict
		num_verdicts += 1
		sum_sq_verdicts += verdict * verdict
		
		times.append(date)
		verdicts.append(verdict)

		verdict_dict[data["urlTests"][i]["created"] * 1/1000] = verdict

	mean = sum_verdicts / num_verdicts
	length = abs(datetime.fromtimestamp(data["urlTests"][len(data["urlTests"]) - 1]["created"] * 1/1000) - datetime.fromtimestamp(data["urlTests"][0]["created"] * 1/1000))

	time_series[index]["avg_verdict"] = mean
	time_series[index]["stddev"] = (1 / num_verdicts * sum_sq_verdicts - (mean * mean)) ** (1/2)
	time_series[index]["num_of_measurements"] = num_verdicts
	time_series[index]["length_of_time_period"] = length.days
	time_series[index]["avg_frequency"] = length.days / num_verdicts
	time_series[index]["verdicts"] = verdict_dict
	
	datapoints += len(verdicts)

	# indices.append(index)

	return url, times, verdicts

count = 0

for name in file_names:
	index = name[:-5]
	url, times, verdicts = clean_data(name, int(index))
	count += 1

	if count % 100 == 0:
		print(str(count) + " reached")

with open('verdicts.json', 'w') as outfile:
	json.dump(time_series, outfile)

def metrics():

	'''
	this function is optional, it calculates the mean, the standard deviation of each word
	'''

	with open('verdicts.json', 'r') as file:
		data = json.load(file)

	stddevs = {}

	for i in indices:
		stddevs[i] = {"word": data[str(i)]["url"][25:], "sigma" : data[str(i)]["stddev"], "mean": data[str(i)]["avg_verdict"]}

	stddevs_descending = OrderedDict(sorted(stddevs.items(), key = lambda kv: kv[1]["sigma"], reverse=True))
	mean_increasing = OrderedDict(sorted(stddevs.items(), key = lambda kv: kv[1]["mean"], reverse=False))

	print(mean_increasing)


# metrics()

#ordered probit model, logistic regression model
#filter with stuff like gong -> politics, se -> sexual
#eliminate the words with the low counts
#manufactured error



## mean of a specific word, variance