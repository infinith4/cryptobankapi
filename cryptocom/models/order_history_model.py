class OrderHistoryModel:
    def __init__(self, orderId: str, side: str, price: float, quantity: float):
        self.orderId = orderId
        self.side = side
        self.price = price
        self.quantity = quantity