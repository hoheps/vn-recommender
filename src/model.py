import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import surprise
from api import VNConnection
class Model():
    def __init__():
        self.df = pd.read_csv('../data/votes2', sep=' ', names=['VN_id', 'user_id', 'vote', 'date'])
        self.user_ser = (df.groupby('user_id').count()[['VN_id']]['VN_id']>15)
        self.ser = (df.groupby('VN_id').count()[['user_id']]['user_id']>20)
        high_user_votes_df = df[df['VN_id'].isin(ser.keys()[ser])][df[df['VN_id'].isin(ser.keys()[ser])]['user_id'].isin(user_ser.keys()[user_ser])]
        #the problem with this is that it ends up taking around 50MB of memory, which isn't too much but it's not sustainable for multiple instances.
        self.ccmodel = surprise.prediction_algorithms.co_clustering.CoClustering(n_cltr_u=3,n_cltr_i=5,verbose=True)
        #coclustering was chosen because of the tradeoffs of speed and useful predictions it could bring.
        #the clusters above were determined through cross-validation
        self.reader = surprise.Reader(rating_scale=(10,100))
        # insert code to call api, concat data

    def create_model():
        self.model = surprise.dump.load('./model.p')
    def new_predictions(uid):
        if uid in self.user_ser: 
        
        else:
            vnc = VNConnection()
            if vnc.is_valid():
                
            pass

    def build_prediction_set():
        if in model:
            [not in list]
        if not in model:
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
    model = Model()
    model.main() 
    #currently, my model refits my data to the solution to that would be to manually implement the co-clustering collaborative filtering algorithm instead of using scikit-surprise, which does not have support for single value insertion (which is O(1))

