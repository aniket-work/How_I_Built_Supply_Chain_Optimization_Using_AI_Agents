import numpy as np


class InventoryOptimizer:
    def optimize(self, historical_demand, current_inventory):
        avg_demand = np.mean(historical_demand)
        std_demand = np.std(historical_demand)

        # Simple reorder point calculation
        reorder_point = avg_demand * 7 + 2 * std_demand  # 7 days of average demand + safety stock

        # Simple EOQ calculation (assuming ordering cost = 100 and holding cost = 0.2)
        eoq = np.sqrt((2 * 100 * avg_demand * 365) / 0.2)

        return reorder_point, eoq