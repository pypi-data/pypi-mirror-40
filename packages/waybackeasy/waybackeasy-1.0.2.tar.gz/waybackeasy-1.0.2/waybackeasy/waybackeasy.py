# Waybackeasy - The insanely simple way to interface with the Waybackmachine
import requests, json, random

class FormatError(Exception):
	pass

def get(target_site, target_date):
	""" get WB-machine snapshot of target site on target day """

	# checking user inputs
	# checking availability of target site
	response = requests.get("http://archive.org/wayback/available?url={}".format(target_site))
	availability = json.loads(response.text)
	if not availability["archived_snapshots"]:
		raise FormatError("There maybe something off with the URL you passed in. Have a close look.")

	# checking date format
	date_split = target_date.split(".")
	if len(date_split[0]) != 2 or len(date_split[1]) != 2 or len(date_split[2]) != 4:
		raise FormatError("There maybe something off with the DATE you passed in. Have a close look.")

	# retrieving snapshot from target day
	# format date to use with WB-machine dateformat
	date = target_date.split(".")
	day, month, year = date[0], date[1], date[2]
	formatted_date = year + month + day

	# get all timestamps available for target day and choose one
	wayback_api = "http://web.archive.org/cdx/search/cdx?url={}&fl=timestamp&output=json&from={}&to={}".format(target_site, formatted_date, formatted_date)
	response = requests.get(wayback_api)
	all_timestamps = json.loads(response.text)
	timestamp_list = [each[0] for each in all_timestamps]
	target_timestamp = random.choice(timestamp_list)

	# get html corresponding to chosen timestamp
	res = requests.get("http://web.archive.org/web/{}/{}".format(target_timestamp, target_site))
	return res.text.encode('utf-8')


result = get("news.ycombinator.com/", "27.05.2016")
print(result)