# Kth nearest neighbor

# pseudocode: User_based knn
# 1. Create a dict of pairwise similarity between users (use cosine similarity)
### cosine similarity: between two users, take out the common animes they watched and calculate cosine similarity of the ratings of those movies
# 2. Take k nearest neighbors of a user, and make the list of movies that the user haven't watched but neighbors have. Average the ratings of the neighbors for each movie.
# 3. Sort the movies by highest rate

import numpy as np

def parse_users(filename):
    users = {}
    for line in open(filename):
        lst = line.replace('\n','').split(',')
        user_id = lst[0]
        anime_id = lst[1]
        rating = lst[2]
        if user_id not in users.keys():
            users[user_id] = {anime_id: rating}
        else:
            users[user_id][anime_id] = rating
    print users
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
    animes = []
    genre_list = get_all_genres(filename)
    infile = open(filename)
    lines = infile.readlines()
    for line in lines[1:]:
        lst = parse_string(line.replace('\n',''))
        anime_name = lst[1]
        rating = lst[-2]
        if rating == '':
            rating = -1.0
        else:
            rating = float(rating)
        genres = parse_genre_string(lst[2])
        vec = make_vec(genres, genre_list)
        animes.append([anime_name,vec,rating])
    infile.close()
    return animes

def abs_diff(vec1,vec2):
    assert len(vec1) == len(vec2)
    diff = 0
    for i in range(len(vec1)):
        diff += abs(vec1[i] - vec2[i])
    return diff

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
        #return k_nearest_anime[0:10]
        #for anime in self.Xtr:
        #    diff = abs_diff(vec,anime[1])
        #    if diff < min_diff:
        #        min_diff = diff
        #        nearest_anime = anime[0]
        #return nearest_anime
        
def knn_training():
    #takes in an dictionary of users in format {user_id: {anime: rating}}
    return

def main():
    #parse_users("rating.csv")
    #line = '32615,Youjo Senki,"Magic, Military",TV,Unknown,,6652'
    #parse_string(line)
    #['32615', 'Youjo Senki', 'Magic, Military', '', 'TV', 'Unknown', '']
    animes = parse_anime("anime.csv")
    all_genres = get_all_genres("anime.csv")
    nn = NearestNeighbor()
    nn.train(animes,all_genres)
    genre_string = input("Choose from following genres: " + str(all_genres) + ':\n')
    recommended_animes = nn.predict(genre_string)
    print "Here are my recommendations based on your favorite genres: "
    for anime in recommended_animes:
        print anime[1] + ' ---> ' + 'rating: ' + str(anime[2])
    #print recommended_animes

if __name__=="__main__":
    main()
