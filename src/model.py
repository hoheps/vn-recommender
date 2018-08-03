import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import surprise
from api import VNConnection
class VNModel():
    def __init__():
        df = pd.read_csv('../data/votes2', sep=' ', names=['VN_id', 'user_id', 'vote', 'date'])
        self.user_ser = (df.groupby('user_id').count()[['VN_id']]['VN_id']>15)
        self.ser = (df.groupby('VN_id').count()[['user_id']]['user_id']>20)
        #grab users with >15 votes and games with >20 votes
        self.high_user_votes_df = df[df['VN_id'].isin(self.ser.keys()[self.ser])][df[df['VN_id'].isin(self.ser.keys()[self.ser])]['user_id'].isin(self.user_ser.keys()[self.user_ser])]
        #the problem with this is that it ends up taking around 50MB of memory, which isn't too much but it's not sustainable for multiple instances. I think I will implement with multiprocessing
        self.ccmodel = surprise.prediction_algorithms.co_clustering.CoClustering(n_cltr_u=3,n_cltr_i=5,verbose=True)
        #coclustering was chosen because of the tradeoffs of speed and useful predictions it could bring.
        #the clusters above were determined through cross-validation
        self.reader = surprise.Reader(rating_scale=(10,100))
        data = surprise.dataset.Dataset.load_from_df(self.high_user_votes_df[['user_id', 'VN_id', 'vote']], self.reader)
        self.trainset = data.build_full_trainset()
    def load_model():
        self.model = surprise.dump.load('./model.p')
    def top_predictions(ruid): #raw user id
        if ruid in self.user_ser:
            self.load_model()
            iuid = self.trainset.to_inner_uid(ruid) #inner user id
            anti_test = self.generate_anti_test(iuid, ruid)
            return sorted(self.model.test(anti_test), key=lambda x: -x.est)[:10]
        else:
            vnc = VNConnection()
            if vnc.is_valid():
               votes = pd.DataFrame(vnc.get_user_votes(uid),columns=['user_id', 'VN_id', 'vote'])
               votes[votes['VN_id'].isin(self.ser.keys()[self.ser]]
               if votes.empty:
                   return top prediction
                   (sort by baseline indexes and get score)
            return None #if connection doesn't work, no results

    def generate_anti_test(iuid, ruid):
    """
    input: userid used by model, userid real
    output: [(userid real, game1 real id, average score),...]
    """
        return [(ruid, self.trainset.to_raw_iid(y), self.trainset.global_mean) for y in self.trainset.all_items() if (y not in [x[0] for x in self.trainset.ur[iuid]])]

    def build_test_set_from_api():
        if item in model:
            [not in list]
        if item not in model:
            filter out results
            pd.DataFrame([(3,2,1),(5,4,6)],columns=['user_id', 'VN_id', 'vote'])
            pd.concat([df,above])
            [not in list]
    def main():
        data = surprise.dataset.Dataset.load_from_df(self.high_user_votes_df[['user_id', 'VN_id', 'vote']], self.reader)
        trainset = data.build_full_trainset()
        self.ccmodel.fit(trainset)
        surprise.dump.dump('model.p',algo=model.ccmodel,verbose=True)
if __name__ == '__main__':
    print('generating model...')
    model = VNModel()
    model.main() 
    #currently, my model refits my data to the solution to that would be to manually implement the co-clustering collaborative filtering algorithm instead of using scikit-surprise, which does not have support for single value insertion (which is O(1))
    #i need to generate edge cases where if the user has no votes (send default list of recommended), or all votes (return... nothing? I suppose) as well. right now my class assumes the user has some percentage of votes.
