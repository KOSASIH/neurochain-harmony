import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

class DecisionSupportModel:
    def __init__(self, data: pd.DataFrame, target: str, features: List[str]):
        self.data = data
        self.target = target
        self.features = features
        self.X = data[features]
        self.y = data[target]

    def train_random_forest(self) -> None:
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
        self.rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.rf_model.fit(X_train, y_train)
        y_pred = self.rf_model.predict(X_test)
        print("Random Forest Accuracy:", accuracy_score(y_test, y_pred))
        print("Random Forest Classification Report:")
        print(classification_report(y_test, y_pred))
        print("Random Forest Confusion Matrix:")
        print(confusion_matrix(y_test, y_pred))

    def train_xgboost(self) -> None:
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
        self.xgb_model = XGBClassifier(objective='binary:logistic', max_depth=6, learning_rate=0.1, n_estimators=1000, n_jobs=-1)
        self.xgb_model.fit(X_train, y_train)
        y_pred = self.xgb_model.predict(X_test)
        print("XGBoost Accuracy:", accuracy_score(y_test, y_pred))
        print("XGBoost Classification Report:")
        print(classification_report(y_test, y_pred))
        print("XGBoost Confusion Matrix:")
        print(confusion_matrix(y_test, y_pred))

    def train_catboost(self) -> None:
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
        self.cat_model = CatBoostClassifier(iterations=1000, learning_rate=0.1, depth=6, task_type='GPU')
        self.cat_model.fit(X_train, y_train)
        y_pred = self.cat_model.predict(X_test)
        print("CatBoost Accuracy:", accuracy_score(y_test, y_pred))
        print("CatBoost Classification Report:")
        print(classification_report(y_test, y_pred))
        print("CatBoost Confusion Matrix:")
        print(confusion_matrix(y_test, y_pred))

    def train_lightgbm(self) -> None:
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
        self.lgbm_model = LGBMClassifier(objective='binary', max_depth=6, learning_rate=0.1, n_estimators=1000, n_jobs=-1)
        self.lgbm_model.fit(X_train, y_train)
        y_pred = self.lgbm_model.predict(X_test)
        print("LightGBM Accuracy:", accuracy_score(y_test, y_pred))
        print("LightGBM Classification Report:")
        print(classification_report(y_test, y_pred))
        print("LightGBM Confusion Matrix:")
        print(confusion_matrix(y_test, y_pred))

    def train_neural_network(self) -> None:
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
        self.nn_model = Sequential()
        self.nn_model.add(Dense(64, activation='relu', input_shape=(self.X.shape[1],)))
        self.nn_model.add(Dense(32, activation='relu'))
        self.nn_model.add(Dense(1, activation='sigmoid'))
        self.nn_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        self.nn_model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))
        y_pred = self.nn_model.predict(X_test) > 0.5
        print("Neural Network Accuracy:", accuracy_score(y_test, y_pred))
        print("Neural Network Classification Report:")
        print(classification_report(y_test, y_pred))
        print("Neural Network Confusion Matrix:")
        print(confusion_matrix(y_test, y_pred))

    def predict(self, model: str, data: pd.DataFrame) -> np.ndarray:
        if model == "random_forest":
            return self.rf_model.predict(data)
        elif model == "xgboost":
            return self.xgb_model.predict(data)
        elif model == "catboost":
            return self.cat_model.predict(data)
        elif model == "lightgbm":
            return self.lgbm_model.predict(data)
        elif model == "neural_network":
            return self.nn_model.predict(data) > 0.5
        else:
            raise ValueError("Invalid model specified")

    def evaluate(self, model: str, data: pd.DataFrame, target: pd.Series) -> None:
        y_pred = self.predict(model, data)
        print("Model Evaluation:")
        print("Accuracy:", accuracy_score(target, y_pred))
        print("Classification Report:")
        print(classification_report(target, y_pred))
        print("Confusion Matrix:")
        print(confusion_matrix(target, y_pred))
