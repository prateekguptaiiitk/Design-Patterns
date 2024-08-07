# 1. EAGER INITIALIZATION METHOD
class DBConnection:
    # Eagerly initialize the single instance of the connection
    _con_object = None

    def __new__(cls):
        if cls._con_object is None:
            cls._con_object = super(DBConnection, cls).__new__(cls)
        return cls._con_object

    def __init__(self):
        # Prevent reinitialization
        if not hasattr(self, '_initialized'):
            # Place any initialization logic here
            self._initialized = True

    @staticmethod
    def get_instance():
        return DBConnection._con_object

# Usage
if __name__ == "__main__":
    con_object = DBConnection.get_instance()
