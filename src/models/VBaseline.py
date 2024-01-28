from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.dummy import DummyRegressor
import numpy as np

class GroupMeanRegressor(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.group_regressors = {}

    def fit(self, X, y):
        # Assuming X is a DataFrame with 'start_station_name' and y is 'hourly_volume'
        for name, group in X.groupby('start_station_name'):
            reg = DummyRegressor(strategy="mean")
            self.group_regressors[name] = reg.fit(group, y.loc[group.index])
        return self

    def predict(self, X):
        # Predict the mean for each group
        # Reset index of X to ensure proper alignment of predictions
        X_reset = X.reset_index(drop=True)
        predictions = np.zeros(X_reset.shape[0])
        for name, group in X_reset.groupby('start_station_name'):
            if name in self.group_regressors:
                # Use the index of the reset DataFrame for proper alignment
                predictions[group.index] = self.group_regressors[name].predict(group)
        return predictions

# Assuming 'df_hire' is the DataFrame containing the bicycle hire data
# and 'hourly_volume' is the target variable we want to predict.

