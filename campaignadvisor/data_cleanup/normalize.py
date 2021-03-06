import pandas as pd
import numpy as np
import os
import cPickle as pickle
from context import campaignadvisor
from sklearn import preprocessing

class Normalizer():
    MIN_VAL = 0
    MAX_VAL = 1

    """
    input: Series
    output: Series
    """

    def __init__(self, df, alg="minmax"):
        self.df = df
        self.alg = alg

    # algorithm types =
    # 'minmax' is rescaling,
    # 	'std' is standardization,
    #	'unit' is scaling to unit length

    def __repr__(self):
        return self.df

    def normalize_minmax(self, feature):
        self.MAX_VAL = self.df[feature].max()
        self.MIN_VAL = self.df[feature].min()
        feature_minmax = feature + '_' + str(self.alg)
        self.df[feature_minmax] = (self.df[feature] - self.MIN_VAL) / (self.MAX_VAL - self.MIN_VAL)

    # return self.df[feature_minmax]

    def normalize_std(self, feature):
        feature_zscore = feature + '_' + str(self.alg)
        self.df[feature_zscore] = (self.df[feature] - self.df[feature].mean()) / self.df[feature].std(ddof=0)

    # return self.df[feature_zscore]

    def normalize(self, feature):
        # check if column min and max equals the global min and max
        if self.MAX_VAL == self.df[feature].max() and self.MIN_VAL == self.df[feature].min():
            return True
        if self.alg == 'minmax':
            self.normalize_minmax(feature)
        elif self.alg == 'std':
            self.normalize_std(feature)

def _save_pickle(data, path):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    with open(path, 'wb') as file_out:
        pickle.dump(data, file_out)

def _load_pickle(path):
    with open(path, 'rb') as file_in:
        return pickle.load(file_in)

def test_normalize(df, features, alg):
    if alg == 'minmax':
        scale = preprocessing.MinMaxScaler().fit(df[features])
    elif alg == 'std':
        scale = preprocessing.StandardScaler().fit(df[features])
    df_scaled = scale.transform(df[features])
    return df_scaled

def main():
    #jobs_name = campaignadvisor.dataframe_holder.JOBS
    #votes_name = campaignadvisor.dataframe_holder.VOTES
    #jobs = campaignadvisor.dataframe_holder.get_dataframe(jobs_name)
    #votes = campaignadvisor.dataframe_holder.get_dataframe(votes_name)
    #votes['clean_fips'] = votes['fips_code']
    
    # country statistics dataframes
    # df = pd.merge(votes, jobs, on='clean_fips', sort=False, how="inner")
    df_name = campaignadvisor.dataframe_holder.COUNTY_STATISTICS
    df = campaignadvisor.dataframe_holder.get_dataframe(df_name)

    # get feature list from county statistics
    features_to_drop = ['clean_fps', 'fips_code', 'FIPS', 'State', 'County', 'winner_name', 'winner_party']
    # keywords_to_drop = ['Pct', 'Rate']
    features_to_scale = list()
    for feature in df.columns:
        feature_element = df[feature][0]
        if type(feature_element) != type(str()) and feature not in features_to_drop:
            if 'Pct' not in feature and 'Rate' not in feature:
                features_to_scale.append(feature)

    # set algorithm 
    n_alg = 'minmax'

    # instantiate Normalizer object with given algorithm
    df_scaled = Normalizer(df, alg=n_alg)

    # normalize only features to be scaled
    for feature in features_to_scale:
        df_scaled.normalize(feature)
        # print df_scaled.df[feature]

    df_cs = df_scaled.df

    # testing
    print "-------ALG CHECK TEST-------"
    #print test_normalize(df, features_to_scale, alg=n_alg)

    print "--------MIN MAX TEST--------"
    features_to_test = list()
    for feature in df_cs.columns:
        if 'minmax' in feature:
            #print df[feature]
            features_to_test.append(feature)
            local_max = max(df_cs[feature])
            #print local_max
    #print features_to_test
    #df_cs['Test_Max'] = df_cs[features_to_test].max(axis=1)

    # pickling
    path = 'county_statistics.pik'
    df['clean_fips'] = df_cs.index
    with open(path, 'wb') as file_out:
        pickle.dump(df_cs, file_out)

if __name__ == "__main__":
    main()