import uuid


class Receipt:
    _instance = None
    _store = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Receipt, cls).__new__(cls)
        return cls._instance

    def save_receipt(self, points):
        receipt_id = str(uuid.uuid4())
        self._store[receipt_id] = points
        return receipt_id

    def get_points(self, receipt_id):
        return self._store.get(receipt_id)
