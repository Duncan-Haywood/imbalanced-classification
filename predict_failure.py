#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import seaborn as sns
import pycaret.classification as pcclass
from sklearn.preprocessing import LabelEncoder
from IPython import display

class imbalanced_classification:
    def __init__(self):
        self.df = pd.read_csv('./predict_failure.csv')
    def data_exploration(self):
        display(self.df)
        encoded_df = self.encode_categorical_columns()
        display(encoded_df)
        self.display_distribution_plots(encoded_df)
        display("number of failures:", self.df.failure.sum())
        display(sns.pairplot(encoded_df, x_vars=['failure']))
    def display_distribution_plots(self, encoded_df):
        for col in encoded_df.columns: 
            display(sns.displot(encoded_df, x=col))
    def encode_categorical_columns(self):
        encoded_df = self.df.copy()
        # encode date
        date_le = LabelEncoder()
        date_le.fit(self.df.date.values)
        date_encoded = list(date_le.transform(self.df.date.values))
        encoded_df.date = date_encoded
        # encode device
        device_le = LabelEncoder()
        device_le.fit(self.df.device.values)
        device_encoded = list(device_le.transform(self.df.device.values))
        encoded_df.device = device_encoded
        return encoded_df
    def train(self):
        pcclass.setup(self.df, target='failure', silent=True, use_gpu=True, fix_imbalance=True, log_experiment="mlflow", experiment_name="baseline", log_plots=True) 
        best_model = pcclass.compare_models(sort="f1", n_select=1)
        boosted_model = pcclass.ensemble_model(best_model, method="Boosting", optimize="f1")
        tuned_model = pcclass.tune_model(boosted_model, optimize="f1")
        self.final_model = pcclass.calibrate_model(tuned_model)
        pcclass.save_model(self.final_model, model_name='imbalanced_classification_model.pkl')
    def evaluate(self):
        display(pcclass.evaluate_model(self.final_model))
    def predict(self, df):
        self.final_model = pcclass.load_model('imbalanced_classification_model.pkl')
        predictions = pcclass.predict_model(self.final_model, df)
        return predictions    
    def retrain(self, updated_df):
        self.final_model = pcclass.load_model('imbalanced_classification_model.pkl')
        pcclass.setup(updated_df, target='failure', silent=True, use_gpu=True, fix_imbalance=True, log_experiment="mlflow", experiment_name="retrain", log_plots=True) 
        updated_model = pcclass.finalize_model(self.final_model)
        pcclass.save_model(updated_model, 'imbalanced_classification_model.pkl')


def __main__():
    imb = imbalanced_classification()
    imb.train()
    imb.evaluate()