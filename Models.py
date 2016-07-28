import numpy as np
import pandas as pd
import time
from sklearn.decomposition import PCA
from sklearn import cross_validation
from sklearn.linear_model import LinearRegression
from sklearn.grid_search import GridSearchCV
from sklearn.svm import SVR
from Input_PreProcessor import Input_PreProcessor
from sklearn.kernel_ridge import KernelRidge
from sklearn.cross_validation import train_test_split

def First_Model_SVR(Scaled_Input_Data, Output_Data):
    n = len(Scaled_Input_Data)
    #cv_ss = cross_validation.ShuffleSplit(n, n_iter=3, train_size=0.0005, test_size=0.0001)
    Grid_Dict = {"C": [1e-1,1e0, 1e1],"gamma": np.logspace(-2, 1, 3)}
    svr_Tuned = GridSearchCV(SVR(kernel='rbf', gamma=0.1, tol = 0.05), cv=5,param_grid=Grid_Dict, scoring="mean_squared_error")
    MeanMSE_SVR = 1
    svr_Tuned.fit(Scaled_Input_Data, Output_Data)
    T0 = time.time()
    SVR_MSE = SVR(kernel='rbf', C=svr_Tuned.best_params_['C'], gamma=svr_Tuned.best_params_['gamma'], tol = 0.01)
    SVR_Time = time.time() - T0
    print('The computational time of Radial based Support Vector Regression for ', n, ' examples is: ', SVR_Time/10)
    MSEs_SVR = cross_validation.cross_val_score(SVR_MSE, Scaled_Input_Data, Output_Data, cv=10, scoring="mean_squared_error")
    MeanMSE_SVR = np.mean(list(MSEs_SVR))
    print('The average MSE of Radial based Support Vector Regression for ', n, ' examples is: ', MeanMSE_SVR)
    return(MeanMSE_SVR, svr_Tuned)

def SVR_Predictor(svr_Tuned, Input_test_Data, Address_test):
    Predicted_SVR = svr_Tuned.predict(Input_test_Data)
    Predicted_SVR_S = pd.Series(Predicted_SVR)
    Predicted_SVR_S.to_csv(Address_test, sep=',')
    return(Predicted_SVR)
    
def Second_Model_KRR(Scaled_Input_Data, Output_Data):
    n = len(Scaled_Input_Data)
    #cv_ss = cross_validation.ShuffleSplit(n, n_iter=3, train_size=0.0005, test_size=0.0001)
    Grid_Dict = {"alpha": [1e0, 1e-1, 1e-2],"gamma": np.logspace(-2, 1, 3)}
    krr_Tuned = GridSearchCV(KernelRidge(kernel='rbf', gamma=0.1), cv=5 ,param_grid=Grid_Dict, scoring="mean_squared_error")
    # krr_Tuned = KernelRidge(kernel='rbf', gamma=0.1, alpha = 0.1)
    krr_Tuned.fit(Scaled_Input_Data, Output_Data)
    T0 = time.time()
    KRR_MSE = KernelRidge(kernel='rbf', alpha=krr_Tuned.best_params_['alpha'], gamma=krr_Tuned.best_params_['gamma'])
    KRR_Time = time.time() - T0
    print('The computational time of Kernel Ridge Regression for ', n, ' examples is: ', KRR_Time/10)
    MSEs_KRR = cross_validation.cross_val_score(KRR_MSE, Scaled_Input_Data, Output_Data, cv=10, scoring="mean_squared_error")
    MeanMSE_KRR = np.mean(list(MSEs_KRR))
    print('The average MSE of Kernel Ridge Regression for ', n, ' examples is: ', MeanMSE_KRR)
    # MeanMSE_KRR = 1
    return(MeanMSE_KRR, krr_Tuned)

def KRR_Predictor(krr_Tuned, Input_test_Data, Address_test):
    Predicted_KRR = krr_Tuned.predict(Input_test_Data)
    Predicted_KRR_S = pd.Series(Predicted_KRR)
    Predicted_KRR_S.to_csv(Address_test, sep=',')
    return(Predicted_KRR)

'''
#######################################Third Model: PCA + Least Square Regression###################################################### 
# Performing Principle Component Analysis to transfer the input variables to capture the maximum variance
pca = PCA()
Input_PCA = pca.fit_transform(Scaled_Input_Data)
Cum_var_Exp=np.cumsum(np.round(pca.explained_variance_ratio_, decimals=4)*100)
plt.plot(Cum_var_Exp)
# plt.show()

# Picking the PCs one by one using 10-fold CV

n = len(Input_PCA)
kf_10 = cross_validation.KFold(n, n_folds=10, shuffle=True, random_state=2)

regr = LinearRegression()
mse = []

score = -1*cross_validation.cross_val_score(regr, np.ones((n,1)), Output_Data.ravel(), cv=kf_10, scoring='mean_squared_error').mean()    
mse.append(score)

for i in np.arange(1,n):
    score = -1*cross_validation.cross_val_score(regr, Input_PCA[:,:i], Output_Data.ravel(), cv=kf_10, scoring='mean_squared_error').mean()
    mse.append(score)


# Buidling the regression model using the first 32 PCs
pca = PCA(n_components=32)
Input_PCA = pca.fit_transform(Scaled_Input_Data)
'''
