import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import surprise
from api import VndbConnection
class VNModel():
    def __init__():
        df = pd.read_csv('../data/votes2', sep=' ', names=['VN_id', 'user_id', 'vote', 'date'])
        self.user_ser = (df.groupby('user_id').count()[['VN_id']]['VN_id']>15)
        self.ser = (df.groupby('VN_id').count()[['user_id']]['user_id']>20)
        #grab users with >15 votes and games with >20 votes
        self.high_user_votes_df = df[df['VN_id'].isin(self.ser.keys()[self.ser])][df[df['VN_id'].isin(self.ser.keys()[self.ser])]['user_id'].isin(self.user_ser.keys()[self.user_ser])]
        #the problem with this is that it ends up taking around 50MB of memory, which isn't too much but it's not sustainable for multiple instances.
        self.ccmodel = surprise.prediction_algorithms.co_clustering.CoClustering(n_cltr_u=3,n_cltr_i=5,verbose=True)
        #coclustering was chosen because of the tradeoffs of speed and useful predictions it could bring.
        #the clusters above were determined through cross-validation
        self.reader = surprise.Reader(rating_scale=(10,100))
        data = surprise.dataset.Dataset.load_from_df(self.high_user_votes_df[['user_id', 'VN_id', 'vote']], self.reader)
        self.trainset = data.build_full_trainset()
    def load_model():
        self.model = surprise.dump.load('./model.p')
    def top_predictions(ruid): #raw user id
        """
        input: real userid
        output: [game1, ..., game10]
        """
        if ruid in self.user_ser:
            self.load_model()
            iuid = self.trainset.to_inner_uid(ruid) #inner user id, used by model
            anti_test = self.generate_anti_test(iuid, ruid)
            top_pred = sorted(self.model.test(anti_test), key=lambda x: -x.est)[:10]
            return [x.iid for x in top_pred]
        else:
            vnc = VndbConnection()
            if vnc.is_valid():
               votes = pd.DataFrame(vnc.get_user_votes(ruid),columns=['user_id', 'VN_id', 'vote'])
               votes = votes[votes['VN_id'].isin(self.ser.keys()[self.ser])][votes[votes['VN_id'].isin(self.ser.keys()[self.ser])]['user_id'].isin(self.user_ser.keys()[self.user_ser])]
               # filters for just votes that are in the model as well
               df = pd.concat([self.high_user_votes_df, votes])
               data = surprise.dataset.Dataset.load_from_df(df[['user_id', 'VN_id', 'vote']], self.reader)
               trainset = data.build_full_trainset()
               self.ccmodel.fit(trainset)
               iuid = self.trainset.to_inner_uid(ruid) 
               anti_test = self.generate_anti_test(iuid, uid, trainset)
               top_pred = sorted(self.model.test(anti_test), key=lambda x: -x.est)[:10]
               return [x.iid for x in top_pred]
               if votes.empty:
                   return [1913, 92, 562, 2016, 12402, 20802, 7771, 2002, 3144, 24]#[trainset.to_raw_iid(x) for x in np.argsort(bmodel.bi)[-10:][::-1]] top predictions using a baseline model. in the future I plan to adjust this so it can take tags and add a filter function
            return None #if connection doesn't work, no results

    def generate_anti_test(iuid, ruid, trainset = self.trainset):
        """
        input: userid used by model, userid real
        output: [(userid real, game1 real id, average score),...]
        """
        return [(ruid, trainset.to_raw_iid(y), trainset.global_mean) for y in trainset.all_items() if (y not in [x[0] for x in trainset.ur[iuid]])]

    def main():
        data = surprise.dataset.Dataset.load_from_df(self.high_user_votes_df[['user_id', 'VN_id', 'vote']], self.reader)
        trainset = data.build_full_trainset()
        self.ccmodel.fit(trainset)
        surprise.dump.dump('model.p',algo=model.ccmodel,verbose=True)
"""
if __name__ == '__main__':
    print('generating model...')
    model = VNModel()
    model.main()
"""
    #currently, my model refits my data to the solution to that would be to manually implement the co-clustering collaborative filtering algorithm instead of using scikit-surprise, which does not have support for single value insertion (which is O(1))
    #i need to generate edge cases where if the user has no votes (send default list of recommended), or all votes (return... nothing? I suppose) as well. right now my class assumes the user has some percentage of votes.
    #other way to restructure would be to add multiprocessing to call functions as processes when needed and that'll free up the memory in the long run.
