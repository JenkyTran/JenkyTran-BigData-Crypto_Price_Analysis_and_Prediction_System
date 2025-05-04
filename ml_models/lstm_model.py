import numpy as np
import pandas as pd
import logging
from typing import Tuple, List
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler

logger = logging.getLogger(__name__)

class LSTMModel:
    def __init__(self, sequence_length: int = 60, prediction_length: int = 7):
        self.sequence_length = sequence_length
        self.prediction_length = prediction_length
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.model = None
        
    def prepare_data(self, data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare data for LSTM model
        
        Args:
            data (pd.DataFrame): Price data
            
        Returns:
            Tuple: X (features) and y (target) arrays
        """
        try:
            # Scale the data
            scaled_data = self.scaler.fit_transform(data[['price']].values)
            
            X, y = [], []
            for i in range(len(scaled_data) - self.sequence_length - self.prediction_length + 1):
                X.append(scaled_data[i:(i + self.sequence_length)])
                y.append(scaled_data[i + self.sequence_length:i + self.sequence_length + self.prediction_length])
                
            return np.array(X), np.array(y)
            
        except Exception as e:
            logger.error(f"Error preparing data: {str(e)}")
            raise
            
    def build_model(self, input_shape: Tuple[int, int]) -> None:
        """
        Build LSTM model
        
        Args:
            input_shape (Tuple): Shape of input data
        """
        try:
            self.model = Sequential([
                LSTM(50, return_sequences=True, input_shape=input_shape),
                Dropout(0.2),
                LSTM(50, return_sequences=True),
                Dropout(0.2),
                LSTM(50),
                Dropout(0.2),
                Dense(self.prediction_length)
            ])
            
            self.model.compile(
                optimizer=Adam(learning_rate=0.001),
                loss='mean_squared_error',
                metrics=['mae']
            )
            
            logger.info("Successfully built LSTM model")
            
        except Exception as e:
            logger.error(f"Error building model: {str(e)}")
            raise
            
    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 100, batch_size: int = 32) -> None:
        """
        Train the LSTM model
        
        Args:
            X (np.ndarray): Training features
            y (np.ndarray): Training targets
            epochs (int): Number of training epochs
            batch_size (int): Batch size for training
        """
        try:
            if self.model is None:
                self.build_model(input_shape=(X.shape[1], X.shape[2]))
                
            history = self.model.fit(
                X, y,
                epochs=epochs,
                batch_size=batch_size,
                validation_split=0.2,
                verbose=1
            )
            
            logger.info("Successfully trained LSTM model")
            return history
            
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            raise
            
    def predict(self, data: np.ndarray) -> np.ndarray:
        """
        Make predictions using the trained model
        
        Args:
            data (np.ndarray): Input data for prediction
            
        Returns:
            np.ndarray: Predicted values
        """
        try:
            if self.model is None:
                raise ValueError("Model has not been trained yet")
                
            # Scale the input data
            scaled_data = self.scaler.transform(data)
            
            # Reshape for LSTM input
            X = scaled_data.reshape(1, self.sequence_length, 1)
            
            # Make prediction
            predictions = self.model.predict(X)
            
            # Inverse transform predictions
            predictions = self.scaler.inverse_transform(predictions)
            
            return predictions[0]
            
        except Exception as e:
            logger.error(f"Error making predictions: {str(e)}")
            raise
            
    def evaluate(self, X: np.ndarray, y: np.ndarray) -> dict:
        """
        Evaluate model performance
        
        Args:
            X (np.ndarray): Test features
            y (np.ndarray): Test targets
            
        Returns:
            dict: Evaluation metrics
        """
        try:
            if self.model is None:
                raise ValueError("Model has not been trained yet")
                
            # Make predictions
            predictions = self.model.predict(X)
            
            # Calculate metrics
            mse = np.mean((predictions - y) ** 2)
            rmse = np.sqrt(mse)
            mae = np.mean(np.abs(predictions - y))
            
            return {
                'mse': mse,
                'rmse': rmse,
                'mae': mae
            }
            
        except Exception as e:
            logger.error(f"Error evaluating model: {str(e)}")
            raise 