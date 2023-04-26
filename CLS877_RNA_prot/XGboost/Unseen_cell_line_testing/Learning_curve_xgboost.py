import numpy as np
import pandas as pd
import sklearn
import sys
import os
import scipy
from importlib import reload
from sklearn.metrics import r2_score
from sklearn.model_selection import ParameterGrid
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import RandomizedSearchCV
import time
import pickle
 

def run_early_stop_rand_hp_opt(param_grid=None, x=None, y=None, x_val=None, 
                               y_val=None, num_trails=1, model_func=None, 
                               es_rounds=5, eval_metric="rmse", 
                               gpu=True, verb=0):
    rng = np.random.default_rng()
    hp_inds = rng.choice(len(param_grid), size=num_trails, replace=False)

    opt_results = {'Smallest val loss': [] , 'Number of trees': [], 'HPs': []}
    losses, val_losses = [], []
    best_loss = None
    for i, ind in enumerate(hp_inds):
        if verb:
            print(f'trail {i+1} of {num_trails}')
        hps = param_grid[ind]
        if gpu:
            hps['tree_method']="gpu_hist"
            
        xgbr = model_func(**hps, objective="reg:squarederror")
        xgbr.fit(x, y, early_stopping_rounds=es_rounds, 
                 eval_set=[(x_val, y_val)], 
                 eval_metric=eval_metric,
                 verbose=verb,
                )
        
        #store results and model if its better than previos best model
        val_loss = xgbr.evals_result()['validation_0'][eval_metric]
        num_trees = xgbr.best_ntree_limit
        hps['stopped n tree'] = num_trees
        min_loss = min(val_loss)
        opt_results['Smallest val loss'].append(min_loss)
        opt_results['Number of trees'].append(num_trees)
        opt_results['HPs'].append(hps)
        if best_loss == None or min_loss < best_loss:
            best_loss = min_loss
            best_model = xgbr

        #keep if loss plots needed
        val_losses.append(val_loss)
        
        
    return pd.DataFrame(opt_results), val_losses, best_model 

def run_lc_xg_ucl(model_func=None, param_grid=None, xtrain=None, ytrain=None, 
                  xval=None, yval=None, xtest=None, ytest=None, 
                  train_sizes=None, num_trails=1, es_rounds=5, 
                  eval_metric="rmse", gpu=True, verb=0,
                  model_save_path=None):

    test_results = {'r2': [], 'mse': [], 'rho' : []}
    t1 = time.time()
    best_models, best_hps = [], []
    num_train_pairs = [] 
    for i, train_size in enumerate(train_sizes):
        
        print(f'{i+1} of {len(train_sizes)} train sizes')
        
        
        
        opt_r, _, best_model = run_early_stop_rand_hp_opt(
            param_grid=param_grid,
            x=xtrain.iloc[: train_size],
            y=ytrain.iloc[: train_size],
            x_val=xval,
            y_val=yval,
            num_trails=num_trails,
            model_func=model_func,
            es_rounds=es_rounds,
            eval_metric=eval_metric,
            gpu=gpu,
            verb=verb
            )
        
        #make predctions using the opt model
        pre = best_model.predict(xtest)
        pre = pre.reshape(len(pre))
        test_results['rho'].append(scipy.stats.pearsonr(ytest, pre))
        test_results['r2'].append(sklearn.metrics.r2_score(ytest, pre))
        test_results['mse'].append(sklearn.metrics.mean_squared_error(ytest, 
                                                                      pre))
        if model_save_path:
            best_model.save_model(f'{model_save_path}{train_size}')
            pickle.dump(best_model, 
                        open(f'{model_save_path}{train_size}', 'wb'))
            
        best_hp = opt_r.sort_values(by='Smallest val loss')['HPs'][0]
        best_hps.append(best_hp)
        
    delta_t = time.time() - t1
    test_results = pd.DataFrame(test_results)
    test_results['train size'] = train_sizes
    print('total time elapsed (s)')
    print(delta_t)
    
    return test_results, best_models, best_hps
                                   
    