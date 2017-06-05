# Anime Recommendation Software


## Purpose
We wanted to create a software that can help anime users find the next good anime to watch. As most people have experienced, after finishing a good drama, tv, or anime series, it leaves the people with longing feelings. People want recommendations similar to the animes that they have liked. So, we decided to build a system for that.

## Data
Our data consists of one user based data that lists the animes that the user has watched, the other one lists the anime title, anime id genres, popularity, ratings, casts, and year released.

## Approach
Initially experimenting with collaborative filtering and an attempt at figuring out which users are similar to each other resulted in accuracy of 15% after extensive experiments. Thus, we have decided to leave the users, and instead work with different anime data in constructing our recommendation system. 
Our assumption is that a person who watched a lot of animes in the similar genres, let’s say Action and Adventure, is likely to watch animes in a similar genre. After analyzing the dataset of 12295 animes, we compiled a total of 44 different genres. We used this 44 genres as our reference vector in alphabetical order. Then for each anime, we assigned a vector of length 44 where if anime has a genre we assign 1 on the respective position and 0 otherwise.

We considered other distance metric such as cosine similarity but we found hammington distance metric to be the most appropriate since it tells us that not only two animes need to share the same genres but also one anime belonging to additional genres that other anime does not also adds on to the difference.

### Example/Figure 1: Hamming distance metric implementation

All genres:

['Action', 'Adventure', 'Cars', 'Comedy', 'Dementia', 'Demons', 'Drama', 'Ecchi', 'Fantasy', 'Game', 'Harem', 'Hentai', 'Historical', 'Horror', 'Josei', 'Kids', 'Magic', 'MartialArts', 'Mecha', 'Military', 'Music', 'Mystery', 'Parody', 'Police', 'Psychological', 'Romance', 'Samurai', 'School', 'Sci-Fi', 'Seinen', 'Shoujo', 'ShoujoAi', 'Shounen', 'ShounenAi', 'SliceofLife', 'Space', 'Sports', 'SuperPower', 'Supernatural', 'Thriller', 'Vampire', 'Yaoi', 'Yuri']
Say, an anime has genres “Action, Adventure, Fantasy.”

Then the anime has a vector of [1,1,0,0,0,0,0,0,1,0,0,...0]

Then we used a hammington distance metric to calculate the similarity between the two animes (its respective vectors)
Hammington distance between two equal-length vectors is the number of positions where the values in corresponding position are different.

For example, the hammington distance between the following two vectors is 3, where it differs in position 2, 4, and 5, where 1 denotes the first position and 6 last. 

[1,0,0,1,0,0]

[1,1,0,0,1,0]


## Final Program
One can use our program in one of two ways:

Input your favorite combination of genres

Input the list of animes you watched so far (or selectively the ones that you liked)


First method provides the 10 nearest anime to a user, additionally sorted by its rating.

Second method finds the two favorite combination of genres that the user likes the most by voting method and use those combinations to recommend 10 nearest anime to a user, also additionally sorted by rating.

## KNN Performance/Accuracy

Due to the nature of recommendation system, we had limitations on our choice of accuracy metric. Companies like Netflix use its recommendation software to generate new data to test the performance. In doing so, Netflix has the isolated testing dataset available for recommendation software. For example, Netflix would give you a list of recommended shows/movies and when user clicks on it and watches it and gives rating, it would evaluate the software performance based on the difference between predicted rating and user rating. However, we cannot use the same metric because we do not use the recommendation software we made to gather new data. This imposes serious limitation on our accuracy metric because even if we split the data of users and the animes they watched into training and testing, the testing data are too arbitrary and is not based on the suggestions by recommendation software. Given enormous list of all animes out there, this approach on dividing training and testing dataset without basing it on the use of recommendation software itself seriously undermines the likelihood of accurately measuring the performance of recommendation software. Therefore, we decide to use alternative approach which is still limited but gives us a better sense of its performance. 

In order to measure the performance/accuracy of recommendation system, we need a testing dataset acquired by using the recommendation system itself. However, this wasn’t possible because we could not acquire new dataset using our recommendation system in a given time. Thus, conventional way of dividing the original data set into training and testing data set would not be very appropriate for two reasons. First, the testing dataset doesn’t really reflect the performance of recommendation system because it was not acquired by using recommendation system. Second, given so many different animes out there that a user can watch, the chances of predicting it even with the help of recommendation system are very low and do not accurately measure the performance.

Due to these limitations, we decided to use an accuracy metric which is still limited but gives a better sense of performance. Given a list of animes that user watched, each anime in the list will vote on the combination of genres. Then we pick the top two combination of genres with the highest votes. Then using those two combination of genres, we use our KNN algorithm to pick 5 nearest animes for each combination, total of 10. Then we see how many animes out of those 10 suggested animes that the user have watched, which is our accuracy. Then we repeat the process for all the users and return the average accuracy which reflects the performance of our KNN recommendation software.
 
Note on accuracy measure:

1. Take a user and the list of watched anime

2. Vote on the genres

3. One with highest vote -> find similar animes (about 10)

4. Test
 
Accuracy metric:

Given user's list of watched anime, deduce the user's favorite genre

Then recommend animes based on that genre up to 10

Then use hit-10 metric to see how many animes in the recommended list the user have watched
 
### Example/Figure 2: How voting works given a user who watched animes (in anime id)

[20, 24, 79, 226, 241, 355, 356, 442, 487, 846, 936, 1546, 1692, 1836, 2001, 2025, 2144, 2787, 2993, 3455, 4063, 4214, 4224, 4581, 4744, 4898, 4999, 5034, 5277, 5667, 5781, 5958, 6163, 6205, 6324, 6500, 6547, 6682, 6707, 6747, 6773, 6793, 7088, 7148, 7593, 7739, 7858, 8074, 8407, 8424, 8525, 8630, 8841, 9041, 9062, 9136, 9181, 9330, 9367, 9515, 9581, 9675, 9750, 9790, 9919, 10067, 10073, 10076, 10079, 10080, 10209, 10578, 10604, 10719, 10790, 10793, 10794, 10805, 10897, 11161, 11266, 11617, 11737, 11757, 11759, 11771, 12293, 12549, 12729, 13357, 13367, 13411, 13561, 13663, 13759, 14749, 14813, 14833, 14967, 15117, 15437, 15451, 15583, 15609, 16011, 16498, 16706, 17265, 17729, 18247, 18277, 18753, 18897, 19163, 19221, 19285, 19429, 19815, 20045, 20785, 20787, 21033, 21881, 22147, 22199, 22319, 22535, 22547, 22663, 22877, 23233, 23321, 23847, 24133, 24455, 24873, 25099, 25157, 25159, 25283, 25397, 26243, 27775, 27899, 28121, 28677, 29093, 29095, 30015], the votes on the combination of genres are following. The top two highest votes are highlighted in bold.
['Action', 'Fantasy', 'Harem', 'Romance', 'School', 'Supernatural'] ---> votes: 1
['Drama', 'School', 'Supernatural'] ---> votes: 1
['Action', 'Comedy', 'Ecchi', 'Fantasy', 'Harem', 'Romance', 'School', 'Supernatural'] ---> votes: 1
['Action', 'Magic', 'Romance', 'School', 'Seinen', 'Supernatural'] ---> votes: 1
['Comedy', 'Drama', 'Romance', 'School', 'SliceofLife'] ---> votes: 1
['Action', 'Comedy', 'Ecchi', 'Fantasy', 'Harem', 'Magic', 'School', 'Shounen'] ---> votes: 1
['Action', 'Ecchi', 'Fantasy', 'Harem', 'School', 'Shounen', 'Supernatural', 'Vampire'] ---> votes: 1
['Action', 'Drama', 'Fantasy', 'Magic', 'School'] ---> votes: 1
['Comedy', 'Ecchi', 'School'] ---> votes: 1
['Comedy', 'Ecchi', 'Romance', 'School'] ---> votes: 1
['Comedy', 'Ecchi', 'Harem', 'Romance', 'School'] ---> votes: 2
['Action', 'Comedy', 'Ecchi', 'Harem', 'Magic', 'Supernatural'] ---> votes: 4
['Comedy', 'Harem', 'Mecha', 'Romance', 'School', 'Sci-Fi'] ---> votes: 2
['Action', 'Drama', 'Sci-Fi', 'SuperPower'] ---> votes: 2
['Comedy', 'Ecchi', 'Harem', 'MartialArts', 'Romance', 'Shounen'] ---> votes: 1
['Action', 'Adventure'] ---> votes: 1
['Comedy', 'Ecchi', 'Harem', 'School'] ---> votes: 1
['Comedy', 'Harem', 'Romance', 'School'] ---> votes: 2
['Comedy', 'Shounen', 'Supernatural'] ---> votes: 1
['Action', 'Comedy', 'Demons', 'Fantasy', 'Historical', 'Shounen', 'Supernatural'] ---> votes: 1
['Action', 'Comedy', 'Ecchi', 'School', 'Supernatural'] ---> votes: 1
['Comedy', 'School', 'Shounen', 'SuperPower', 'Supernatural'] ---> votes: 1
['Comedy', 'Harem', 'Mystery', 'Romance', 'School', 'Shounen', 'Supernatural'] ---> votes: 1
['Action', 'Adventure', 'Fantasy', 'Game', 'Romance'] ---> votes: 2
['Magic', 'Romance', 'School', 'Sci-Fi', 'Supernatural'] ---> votes: 1
['Comedy'] ---> votes: 1
['Comedy', 'Drama', 'Ecchi', 'Harem', 'Romance', 'Sci-Fi', 'Shounen', 'Supernatural'] ---> votes: 1
['Action', 'Comedy', 'Ecchi', 'Fantasy', 'Harem', 'Magic', 'Romance', 'School', 'Shounen', 'Supernatural'] ---> votes: 1
['Comedy', 'Ecchi', 'Supernatural'] ---> votes: 1
['Comedy', 'Ecchi', 'Harem', 'Romance', 'School', 'Seinen', 'SliceofLife'] ---> votes: 1
['Action', 'Demons', 'Ecchi', 'Fantasy', 'Harem', 'Romance'] ---> votes: 1
['Action', 'Comedy', 'Demons', 'Ecchi', 'Harem', 'Romance', 'School'] ---> votes: 1
['Action', 'Game', 'Romance', 'School', 'Sci-Fi'] ---> votes: 1
['Action', 'Drama', 'Fantasy', 'Shounen', 'SuperPower'] ---> votes: 3
['Drama', 'Harem', 'Psychological', 'Romance'] ---> votes: 1
['Comedy', 'School', 'Shounen', 'Sports'] ---> votes: 1
