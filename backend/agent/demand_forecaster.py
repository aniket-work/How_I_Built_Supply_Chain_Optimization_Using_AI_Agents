import numpy as np
from sklearn.ensemble import RandomForestRegressor


class DemandForecaster:
    def forecast(self, historical_demand):
        # Simple forecasting using RandomForestRegressor
        X = np.array(range(len(historical_demand))).reshape(-1, 1)
        y = np.array(historical_demand)
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)

        future_X = np.array(range(len(historical_demand), len(historical_demand) + 30)).reshape(-1, 1)
        forecast = model.predict(future_X)
        return forecast.tolist()