# Waybackeasy - The insanely simple way to interface with the Waybackmachine
import requests, json, random

class FormatError(Exception):
	pass

def get(target_site, target_date):
	""" get Waybackmachine snapshot of the target site on the target day """

	# Checking whether user inputs are roughly correct
	# checking availability of target_site
	response = requests.get("http://archive.org/wayback/available?url={}".format(target_site))
	availability = json.loads(response.text)
	if not availability["archived_snapshots"]:
		raise FormatError("We have the suspicion there maybe something wrong with the URL you passed in.")
	print(availability["archived_snapshots"])

	# checking date format
	date_split = target_date.split(".")
	if len(date_split[0]) != 2 or len(date_split[1]) != 2 or len(date_split[2]) != 4:
		raise FormatError("We have the suspicion there maybe something wrong with the DATE you passed in.")

	# Attempting to retrieve snapshot of target day
	# format date for use with WB-machine
	date = target_date.split(".")
	day, month, year = date[0], date[1], date[2]
	formatted_date = year + month + day

	# get all timestamps of target day from the WB-machine & choose one
	wayback_api = "http://web.archive.org/cdx/search/cdx?url={}&fl=timestamp&output=json&from={}&to={}".format(target_site, formatted_date, formatted_date)
	response = requests.get(wayback_api)
	all_timestamps = json.loads(response.text)
	timestamp_list = [each[0] for each in all_timestamps]
	target_timestamp = random.choice(timestamp_list)

	# get html corresponding to chosen timestamp
	res = requests.get("http://web.archive.org/web/{}/{}".format(target_timestamp, target_site))
	return res.text.encode('utf-8')


# # trying
# res = get("spiegel.de", "11.01.2017")
# print(res)
