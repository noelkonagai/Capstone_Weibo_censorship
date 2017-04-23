import json, csv

def import_exceptions():

	'''
	the function imports the KeyError exceptions saved in a txt file
	'''
	
	with open('exceptions.txt', 'r') as infile:
		data = list(csv.reader(infile))[0]

	results = list(map(int, data))

	return(results)

def test_key_errors(errors):

	'''
	the function creates a list of keys that are valid to be valed and checks whether they give a KeyError
	'''

	key_list = []

	for i in range(31963):
		if i + 1 not in errors:
			try:
				data[str(i + 1)]
				key_list.append(str(i + 1))
			except KeyError:
				print("key error at ", i + 1)

	return key_list

def change_dict_keys(data, key_list):

	'''
	changes the dictionary keys, which contain the original json file names, to ordered key integers
	'''

	new_data = {}

	for i in range(len(data) - 1):
		new_data[i] = data[key_list[i]]

	with open('verdicts_ordered_keys.json','w') as f:
		json.dump(new_data, f)

	return new_data

def save_to_csv(new_data):

	'''
	this function converts the json file into csv file
	'''

	with open('verdicts.csv', 'w') as f:
		fieldnames = ['Unique_ID','Word_ID', 'Word', 'Time', 'Verdict']

		writer = csv.DictWriter(f, fieldnames=fieldnames)

		writer.writeheader()

		counter = 0

		for i in range(len(new_data)):
			for key, value in new_data[i]['verdicts'].items():

				row = {'Unique_ID': counter, 'Word_ID': i, 'Word': new_data[i]['url'][25:], 'Time': float(key), 'Verdict': int(value)}

				counter += 1

				writer.writerow(row)

	return 0


with open('verdicts.json', 'r') as infile:
	data = json.load(infile)

errors = import_exceptions()
key_list = test_key_errors(errors)
new_data = change_dict_keys(data, key_list)
save_to_csv(new_data)

