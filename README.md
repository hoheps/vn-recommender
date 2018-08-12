# vn_recommender
Recommender system for visual novels

### Introduction:
The data was sourced from VNDB. I also used the VNDB (non-REST) API to call user-data and allow for predictions.

Visual novels (VNs) are a type of game that's sort of like a CYOA (choose-your-own-adventure) game, where you make decisions that affect the course of the game. Like the name implies, the games are mostly narrative. The origin of VNs are in Japanese media, and therefore many of the games are Japanese.

### EDA:
Initially, I found that the sparsity of the vote dataset was very high, in the range of 0.00001 dense matrix. To reduce the sparsity of the matrix, I decided to take the group of users who had voted for more than 15 games, and games which had more than 20 votes. This increased the density to 0.01, which, while still being higher than the MovieLens dataset, was still at a level that was workable with.

### Technique:
I divided the category of users into mainly 2 categories and 3 subcategories of both. Users who were in the dataset with no/some/all votes and users who were not in the dataset with no/some/all votes.
- Users in the dataset:
  - No items voted - this person would not be in the dataset
  - Some items voted - likely
  - Everything voted - there isn't anything to predict to someone who's watched everything.
- Users not in the dataset:
  - No items voted - somewhat likely
  - Some items voted - most likely
  - Everything voted - this person would be in the dataset

To create the predictions for the data, I decided to use co-clustering collaborative filtering, which is a combination of item-to-item as well as user-to-user clustering, creating a user-cluster to item-cluster system. I used the scikit-surprise implementation of co-clustering CF.
Co-clustering CF was chosen because of the performance advantage over SVD and other matrix factorization techniques. I planned to run this off Flask on a Raspberry Pi, therefore I had to optimize in favor of time (since I don't want users to wait three minutes for a response). The Flask app uses an Ajax jquery call to pull the predictions from the model.

### Future Path:
One thing scikit-surprise does not do is allow incremental training of online data, which is one of the biggest performance advantages of CF. Currently, I have to add the new user to the dataset, and refit the data to the model. I plan on implementing this feature to the model at a future date.
