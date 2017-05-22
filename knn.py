# Kth nearest neighbor

# pseudocode: User_based knn
# 1. Create a dict of pairwise similarity between users (use cosine similarity)
### cosine similarity: between two users, take out the common animes they watched and calculate cosine similarity of the ratings of those movies
# 2. Take k nearest neighbors of a user, and make the list of movies that the user haven't watched but neighbors have. Average the ratings of the neighbors for each movie.
# 3. Sort the movies by highest rate

import numpy as np
import random

K = 10
user_test = [20.0, 24.0, 79.0, 226.0, 241.0, 355.0, 356.0, 442.0, 487.0, 846.0, 936.0, 1546.0, 1692.0, 1836.0, 2001.0, 2025.0, 2144.0, 2787.0, 2993.0, 3455.0, 4063.0, 4214.0, 4224.0, 4581.0, 4744.0, 4898.0, 4999.0, 5034.0, 5277.0, 5667.0, 5781.0, 5958.0, 6163.0, 6205.0, 6324.0, 6500.0, 6547.0, 6682.0, 6707.0, 6747.0, 6773.0, 6793.0, 7088.0, 7148.0, 7593.0, 7739.0, 7858.0, 8074.0, 8407.0, 8424.0, 8525.0, 8630.0, 8841.0, 9041.0, 9062.0, 9136.0, 9181.0, 9330.0, 9367.0, 9515.0, 9581.0, 9675.0, 9750.0, 9790.0, 9919.0, 10067.0, 10073.0, 10076.0, 10079.0, 10080.0, 10209.0, 10578.0, 10604.0, 10719.0, 10790.0, 10793.0, 10794.0, 10805.0, 10897.0, 11161.0, 11266.0, 11617.0, 11737.0, 11757.0, 11759.0, 11771.0, 12293.0, 12549.0, 12729.0, 13357.0, 13367.0, 13411.0, 13561.0, 13663.0, 13759.0, 14749.0, 14813.0, 14833.0, 14967.0, 15117.0, 15437.0, 15451.0, 15583.0, 15609.0, 16011.0, 16498.0, 16706.0, 17265.0, 17729.0, 18247.0, 18277.0, 18753.0, 18897.0, 19163.0, 19221.0, 19285.0, 19429.0, 19815.0, 20045.0, 20785.0, 20787.0, 21033.0, 21881.0, 22147.0, 22199.0, 22319.0, 22535.0, 22547.0, 22663.0, 22877.0, 23233.0, 23321.0, 23847.0, 24133.0, 24455.0, 24873.0, 25099.0, 25157.0, 25159.0, 25283.0, 25397.0, 26243.0, 27775.0, 27899.0, 28121.0, 28677.0, 29093.0, 29095.0, 30015.0]
user_test = [str(int(anime_id)) for anime_id in user_test]
######################Taken from online####################
def quicksort(anime_list, attri_index):
    #anime_list looks like [diff, anime_name, anime_rating]
    quicksort_helper(anime_list,0,len(anime_list)-1,attri_index)

def quicksort_helper(lst,first,last,attri_index):
    if first < last:
        splitpoint = partition(lst,first,last,attri_index)
        quicksort_helper(lst,first,splitpoint-1,attri_index)
        quicksort_helper(lst,splitpoint+1,last,attri_index)

def partition(lst,first,last,attri_index):
    pivotvalue = lst[first][attri_index]
    leftmark = first + 1
    rightmark = last
    done = False
    while not done:
        while leftmark <= rightmark and lst[leftmark][attri_index] <= pivotvalue:
            leftmark += 1
        while leftmark <= rightmark and lst[rightmark][attri_index] >= pivotvalue:
            rightmark -= 1
        if rightmark < leftmark:
            done = True
        else:
            tmp = lst[leftmark]
            lst[leftmark] = lst[rightmark]
            lst[rightmark] = tmp

    tmp = lst[rightmark]
    lst[rightmark] = lst[first]
    lst[first] = tmp

    return rightmark

###########################################################

################# Parse functions ####################
def parse_users(filename):
    #returns dictionary
    #{user_id:[array of anime_id]}
    infile = open(filename)
    lines = infile.readlines()
    users = {}
    for line in lines[:50000]:
        arr = line.replace('\r\n','').split(',')
        user_id = arr[0]
        anime_id = arr[1]
        if user_id not in users:
            users[user_id] = [anime_id]
        else:
            users[user_id].append(anime_id)
    return users

def parse_string(line):
    words = []
    word = ''
    in_quote = False
    for i in range(len(line)):
        #outside quote entering inside quote
        if not in_quote and line[i] == '"':
            in_quote = True
            continue
        #inside quote entering outside
        elif in_quote and line[i] == '"':
            in_quote = False
            words.append(word)
            word = ''
        elif line[i] == ',' and line[i-1] == '"':
            continue
        #outside quote encountered ,
        elif not in_quote and line[i] == ',':
            words.append(word)
            word = ''
        #outside/inside quote
        else:
            word = word + line[i]
    words.append(word)
    return words

def get_all_genres(filename):
    genre_list = []
    infile = open(filename)
    lines = infile.readlines()
    for line in lines[1:]:
        lst = parse_string(line.replace('\n',''))
        genres = lst[2].split(",")
        for genre in genres:
            genre = genre.replace(' ','')
            if genre and genre not in genre_list:
                genre_list.append(genre)
    genre_list.sort()
    infile.close()
    return genre_list

def make_vec(sample_genre,all_genres):
    vec = [0] * len(all_genres)
    for genre in sample_genre:
        for i in range(len(all_genres)):
            if all_genres[i] == genre:
                vec[i] = 1
    return vec

def parse_genre_string(genre_string):
    genres = genre_string.split(',')
    for index, genre in enumerate(genres):
        genre = genre.replace(' ','')
        genres[index] = genre
    return genres

def parse_anime(filename):
    """
    animes = {anime_id:[anime_name,genres,rating,members]}
    """
    animes = {}
    #genre_list = get_all_genres(filename)
    infile = open(filename)
    lines = infile.readlines()
    for line in lines[1:]:
        lst = parse_string(line.replace('\r\n',''))
        anime_id = lst[0]
        anime_name = lst[1]
        rating = lst[-2]
        if rating == '':
            rating = -1.0
        else:
            rating = float(rating)
        genres = parse_genre_string(lst[2])
        members = int(lst[-1])
        #vec = make_vec(genres, genre_list)
        animes[anime_id] = [anime_name,genres,rating,members]
        #animes.append([anime_name,vec,rating])
    infile.close()
    return animes

########################################################

def abs_diff(vec1,vec2):
    assert len(vec1) == len(vec2)
    diff = 0
    for i in range(len(vec1)):
        diff += abs(vec1[i] - vec2[i])
    return diff

class NearestNeighbor():
    def __init__(self):
        pass

    def train(self, X, genre_list):
        self.Xtr = X
        self.all_genres = genre_list

    def predict(self, test):
        genres = parse_genre_string(test)
        vec = make_vec(genres, self.all_genres)
        min_diff = len(self.all_genres) + 1
        nearest_anime = ''
        k_nearest_anime = []
        for anime in self.Xtr[0:4000]:
            diff = abs_diff(vec,anime[1])
            k_nearest_anime.append([diff,anime[0],anime[2]])
        quicksort(k_nearest_anime,0)
        k_nearest_anime = k_nearest_anime[0:10]
        quicksort(k_nearest_anime,2)
        return k_nearest_anime[::-1]

def predict(test,all_genres,training_data):
    if type(test) == str:
        genres = parse_genre_string(test)
    elif type(test) == list:
        genres = test
    else:
        print "inappropriate type"
    vec = make_vec(genres,all_genres)
    anime_by_distance = []
    return_anime = []
    for i in range(44):
        anime_by_distance.append([])
    for anime_id, anime in training_data.iteritems():
        anime_vec = make_vec(anime[1],all_genres)
        diff = abs_diff(vec,anime_vec)
        anime.append(anime_id)
        anime_by_distance[diff].append(anime)
    count = 0
    for al in anime_by_distance:
        #sort by rating
        quicksort(al,2)
        al = al[::-1]
        for anime in al:
            count += 1
            if count > K:
                break
            return_anime.append(anime)
    return return_anime

def vote(user_data,training_data):
    """
    user_data = [array of anime ids that user watched]
    training_data = {anime_id:[anime_name,genres,rating,members]}
    """
    genre_votes = {}
    #print training_data.keys()[:4]
    for anime_id in user_data:
        genres = sorted(training_data[anime_id][1])
        if str(genres) not in genre_votes:
            genre_votes[str(genres)] = [genres,1]
        else:
            genre_votes[str(genres)][1] += 1
    max_votes = 0
    max_votes_genre = ''
    for genres in genre_votes:
        if genre_votes[genres][1] > max_votes:
            max_votes = genre_votes[genres][1]
            max_votes_genre = genre_votes[genres][0]
        #print genres + " ---> votes: " + str(genre_votes[genres][1])
    return max_votes_genre


#def test(k


#def vote(anime_ids, train_data):
#    for 

def main():
    animes = parse_anime("anime.csv")
    users = parse_users("rating.csv")
    all_genres = get_all_genres("anime.csv")
    """
    #nn = NearestNeighbor()
    #nn.train(animes,all_genres)
    genre_string = input("Choose from following genres: " + str(all_genres) + ':\n')
    #recommended_animes = nn.predict(genre_string)
    recommended_animes = predict(genre_string,all_genres,animes)
    print "Here are my recommendations based on your favorite genres: "
    for anime in recommended_animes:
        #print anime[1] + ' ---> ' + 'rating: ' + str(anime[2])
        print anime[0] + ' ---> ' + 'genres: ' + str(anime[1]) + '   ' + 'rating: ' + str(anime[2])
    #print recommended_animes
    best_genre = vote(user_test,animes)
    recommended_animes = predict(best_genre,all_genres,animes)
    for anime in recommended_animes:
        #print anime[1] + ' ---> ' + 'rating: ' + str(anime[2])
        print anime[0] + ' ---> ' + 'anime_id: ' + str(anime[-1]) + '  genres: ' + str(anime[1]) + '   ' + 'rating: ' + str(anime[2])
        """
    user_count = 0
    accuracy = 0
    for user_id, anime_list in users.iteritems():
        if len(anime_list) < 10:
            continue
        else:
            user_count += 1
            print user_id
        #random.shuffle(anime_list)
        #train = anime_list[:-2]
        #test = anime_list[-2:]
        favorite_genres = vote(anime_list,animes)
        recommended_animes = predict(favorite_genres,all_genres,animes)
        count = 0
        for anime in recommended_animes:
            anime_id = anime[-1]
            if anime_id in anime_list:
                count += 1
        accuracy += float(count) / 10
    print "accuracy: " + str(accuracy/user_count) + "  number of users: " + str(user_count)

if __name__=="__main__":
    main()
