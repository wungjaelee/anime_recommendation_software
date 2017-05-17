import numpy as np
import csv
import bisect
import operator


def load_data():
	user_dict = {}
	with open("rating.csv", "rb") as f:
		reader = csv.reader(f, delimiter = ',')
		counter = 1
		for i, row in enumerate(reader):
			if counter == 1:
				pass
			else:
				row = map(int, row)
				if user_dict.has_key(row[0]):
					bisect.insort_left(user_dict[row[0]],row[1])
				else:
					user_dict[row[0]] = [row[1]]
			counter += 1

			# if counter == 5000000:
			# 	break

	return user_dict

	# data = np.array(np.genfromtxt('rating.csv', delimiter = ','))
	# x = data[:,0:2]
	# print(np.shape(x))
	# return x

def data_dict(data):
	user_dict = {}
	for row in data:
		if np.isnan(row[0]):
			pass
		elif user_dict.has_key(row[0]):
			bisect.insort_left(user_dict[row[0]],row[1])
		else:
			user_dict[row[0]] = [row[1]]
	return user_dict

def shorter_dict(dict):
	short = {}
	first_value = 0
	for key, value in dict:
		if first_value == 0:
			first_value = value
		elif first_value == value:
			short[key] = value
	print(short)

# def print_dict(dict):
# 	counter = 1
# 	for k, d in dict.iteritems():
# 		print(k)
# 		print(d)
# 		if counter > 3:
# 			break
# 		counter = counter + 1


def recommendation_list(dict, user):
	best_fit = []
	for key, value in dict.iteritems(): 
		overlap = set(value).intersection(user)
		overlap = len(list(overlap))
		item = [overlap, key]
		best_fit.append(item)
	best_fit = sorted(best_fit, reverse = True)
	return best_fit
	
def selections(best_fit, user):
	best = []
	for i in range(0,20):
		best.append(best_fit[i])
	return best

def non_overlapping(best, user, dict):
	temp = []
	results = {}
	for item in best:
		exists = False
		temp = list(set(user) - set(dict.get(item[0])))
		if len(temp) > 0:
			for anime in temp:
				if results.has_key(anime):
					results[anime] += 1
				else:
					results[anime] = 1
	results = sorted(results.items(), key=operator.itemgetter(1), reverse = True)
	return results



# def data_to_excel(user_dict):
# 	with open('dict.csv','wb') as f:
# 		w = csv.writer(f)
# 		w.writerows(user_dict.items())


dict = load_data()

# dict = data_dict(data)
# print_dict(dict)

user_test = [20.0, 24.0, 79.0, 226.0, 241.0, 355.0, 356.0, 442.0, 487.0, 846.0, 936.0, 1546.0, 1692.0, 1836.0, 2001.0, 2025.0, 2144.0, 2787.0, 2993.0, 3455.0, 4063.0, 4214.0, 4224.0, 4581.0, 4744.0, 4898.0, 4999.0, 5034.0, 5277.0, 5667.0, 5781.0, 5958.0, 6163.0, 6205.0, 6324.0, 6500.0, 6547.0, 6682.0, 6707.0, 6747.0, 6773.0, 6793.0, 7088.0, 7148.0, 7593.0, 7739.0, 7858.0, 8074.0, 8407.0, 8424.0, 8525.0, 8630.0, 8841.0, 9041.0, 9062.0, 9136.0, 9181.0, 9330.0, 9367.0, 9515.0, 9581.0, 9675.0, 9750.0, 9790.0, 9919.0, 10067.0, 10073.0, 10076.0, 10079.0, 10080.0, 10209.0, 10578.0, 10604.0, 10719.0, 10790.0, 10793.0, 10794.0, 10805.0, 10897.0, 11161.0, 11266.0, 11617.0, 11737.0, 11757.0, 11759.0, 11771.0, 12293.0, 12549.0, 12729.0, 13357.0, 13367.0, 13411.0, 13561.0, 13663.0, 13759.0, 14749.0, 14813.0, 14833.0, 14967.0, 15117.0, 15437.0, 15451.0, 15583.0, 15609.0, 16011.0, 16498.0, 16706.0, 17265.0, 17729.0, 18247.0, 18277.0, 18753.0, 18897.0, 19163.0, 19221.0, 19285.0, 19429.0, 19815.0, 20045.0, 20785.0, 20787.0, 21033.0, 21881.0, 22147.0, 22199.0, 22319.0, 22535.0, 22547.0, 22663.0, 22877.0, 23233.0, 23321.0, 23847.0, 24133.0, 24455.0, 24873.0, 25099.0, 25157.0, 25159.0, 25283.0, 25397.0, 26243.0, 27775.0, 27899.0, 28121.0, 28677.0, 29093.0, 29095.0, 30015.0]
best_fit = recommendation_list(dict, user_test)
best = selections(best_fit, user_test)
user_recommendation = non_overlapping(best, user_test, dict)
shorter_dict(user_recommendation)
