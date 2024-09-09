class RecommendationGenerator:
    def generate(self, optimization_result):
        recommendations = []

        if optimization_result.supplier_risk > 0.3:
            recommendations.append("Consider diversifying suppliers to reduce risk.")

        if optimization_result.current_inventory < optimization_result.reorder_point:
            recommendations.append(
                f"Place an order for {optimization_result.economic_order_quantity:.0f} units immediately.")

        if max(optimization_result.forecast) > 1.5 * min(optimization_result.forecast):
            recommendations.append("Prepare for significant demand fluctuations in the coming month.")

        return recommendations
