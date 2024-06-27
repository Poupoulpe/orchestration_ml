import sys
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Define the time step (e.g., 24 hours for a daily prediction)
time_step = 24


# Create a function to prepare the data for time series forecasting
def create_dataset(features, target, time_step=1):
    X, y = [], []
    for i in range(len(features) - time_step):
        X.append(features[i : (i + time_step), :])
        y.append(target[i + time_step])
    return np.array(X), np.array(y)


if __name__ == "__main__":
    if len(sys.argv) < 1:
        raise ValueError("No arguments were passed.")
    file_path = sys.argv[1]

    # Load the data
    data = pd.read_csv(file_path)  # data_06_23_to_06_24.csv

    # Convert date column to datetime
    data["date"] = pd.to_datetime(data["date"])

    # Set date as index
    data.set_index("date", inplace=True)

    # Fill NaN values with the mean of the respective column
    data.fillna(data.mean(), inplace=True)

    # Select relevant features (excluding the target variable)
    features = data.drop(columns=["temperature_2m"])

    # Target variable
    target = data["temperature_2m"]

    # Scale the features and target
    scaler_features = MinMaxScaler()
    scaler_target = MinMaxScaler()

    features_scaled = scaler_features.fit_transform(features)
    target_scaled = scaler_target.fit_transform(target.values.reshape(-1, 1))

    # Create the dataset
    X, y = create_dataset(features_scaled, target_scaled, time_step)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Define the LSTM model
    model = tf.keras.Sequential(
        [
            tf.keras.layers.LSTM(
                50, return_sequences=True, input_shape=(time_step, X_train.shape[2])
            ),
            tf.keras.layers.LSTM(50, return_sequences=False),
            tf.keras.layers.Dense(25),
            tf.keras.layers.Dense(1),
        ]
    )

    # Compile the model
    model.compile(optimizer="adam", loss="mean_squared_error")

    # Train the model

    history = model.fit(
        X_train,
        y_train,
        validation_data=(X_test, y_test),
        epochs=20,
        batch_size=32,
    )

    # Predict on the test set
    y_pred_scaled = model.predict(X_test)

    # Inverse transform the predictions and the actual values
    y_pred = scaler_target.inverse_transform(y_pred_scaled)
    y_test_actual = scaler_target.inverse_transform(y_test)

    # Calculate evaluation metrics
    mse = mean_squared_error(y_test_actual, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test_actual, y_pred)

    print(f"Mean Squared Error: {mse}")
    print(f"Root Mean Squared Error: {rmse}")
    print(f"R-squared Score: {r2}")

    # Save Model
    model.save(f"/app/lstm.keras")
