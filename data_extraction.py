iport numpy as np
import csv
import bisect


def load_data():
	data = np.array(np.genfromtxt('rating.csv', delimiter = ','))
	x = data[:,0:2]
	print(np.shape(x))
	return x

def data_dict(data):
	user_dict = {}
	for row in data:
		if user_dict.has_key(row[1]):
			bisect.insort_left(user_dict[row[1]],row[0])
		else:
			user_dict[row[1]] = [row[0]]
	return user_dict


def 

# def data_to_excel(user_dict):
# 	with open('dict.csv','wb') as f:
# 		w = csv.writer(f)
# 		w.writerows(user_dict.items())


data = load_data()

dict = data_dict(data)

# data_to_excel(dict)


