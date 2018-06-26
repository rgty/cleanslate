# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 17:58:36 2018

@author: raghug
"""

import numpy as np
import math
from operator import itemgetter
from pprint import pprint
import time
import pandas as pd

def get_similarity(doc_id, N=10):
    
    s_time = time.time()
    
    df = pd.read_csv('social_info.csv')
    sp_df = pd.read_csv('speciality_info.csv')

    doc_df = df[df.doc_id == doc_id]
    other_df = df[df.doc_id != doc_id]
    other_set = set(other_df.doc_id)
    sim_list = list()
    
    speciality = sp_df[sp_df.doc_id == doc_id].speciality.to_string().split()
    speciality = ' '.join([_name for _name in speciality[1:]])
    sim_list.append([doc_id, speciality, 1.0])
    
    at, counter, percent = math.floor(len(other_set)/100), 0, 0    
    
    for other_id in other_set:
        
        counter += 1
                
        if(counter == at):
            percent += 1
            counter = 0
            if percent == 100:
                print("\rPROCESSED..{}%".format(percent), end="")
            else:
                print("\rPROCESSING..{}%".format(percent), end="")
        
        doc_dict, fd1, fd2 = dict(), dict(), dict()
        
        temp_df = other_df[other_df.doc_id == other_id]
        
        com_feeds = np.intersect1d(doc_df.feed_id, temp_df.feed_id).tolist()
        
        if len(com_feeds) == 0 : continue

        for _id in com_feeds:
            fd1[_id] = int(doc_df[doc_df.feed_id == _id].rate)
            fd2[_id] = int(temp_df[temp_df.feed_id == _id].rate)
        
        doc_dict[doc_id] = fd1
        doc_dict[other_id] = fd2
        
        score = pearson_correlation(doc_dict, com_feeds, (doc_id, other_id))
        
        if score:
            speciality = sp_df[sp_df.doc_id == other_id].speciality.to_string().split()
            speciality = ' '.join([_name for _name in speciality[1:]])
            sim_list.append([other_id, speciality, score])
            
    
    sim_list = sorted(sim_list, key=itemgetter(2), reverse=True)[:N]
    
    print("\nTIME TAKEN -  %d seconds" %(time.time() - s_time))
    
    return sim_list

def pearson_correlation(doc_dict, feeds, doc_id):
    
    N = len(feeds)
    
    sum1 = sum([doc_dict[doc_id[0]][it] for it in feeds])
    sum2 = sum([doc_dict[doc_id[1]][it] for it in feeds])
    
    sum1Sq=sum([pow(doc_dict[doc_id[0]][it], 2) for it in feeds])
    sum2Sq=sum([pow(doc_dict[doc_id[1]][it], 2) for it in feeds])
    
    pSum = sum([doc_dict[doc_id[0]][it]*doc_dict[doc_id[1]][it] for it in feeds])
    
    num = (pSum - sum1*sum2/N)
    den = math.sqrt((sum1Sq - pow(sum1, 2)/N)*(sum2Sq - pow(sum2, 2)/N))
    
    if den == 0: return 0
    
    return num/den
    
def euclidean_distance(doc_dict, feeds, doc_id):
    distance = sum([math.pow(doc_dict[doc_id[0]][it] - doc_dict[doc_id[1]][it], 2) 
        for it in feeds])
    if distance : return float('%.2f' % (1/(1+math.sqrt(distance))))

if __name__ == '__main__':
    N = 10
    pprint(get_similarity(16166, N))
    
    
    


