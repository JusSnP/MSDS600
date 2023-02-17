import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from tpot.export_utils import set_param_recursive

# NOTE: Make sure that the outcome column is labeled 'target' in the data file
print('Please enter the data filename including file extension. Only .csv files are acceptable.')
file = input()
tpot_data = pd.read_csv(file, index_col='customerID')
features = tpot_data.drop('Churn', axis=1)
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['Churn'], random_state=42)

# Average CV score on the training set was: 0.8023450478318152
exported_pipeline = make_pipeline(
    PCA(iterated_power=7, svd_solver="randomized"),
    GradientBoostingClassifier(learning_rate=0.1, max_depth=1, max_features=0.35000000000000003, min_samples_leaf=16, min_samples_split=20, n_estimators=100, subsample=0.5)
)
# Fix random state for all the steps in exported pipeline
set_param_recursive(exported_pipeline.steps, 'random_state', 42)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
print(results)