# 1. EAGER INITIALIZATION METHOD
class DBConnection_1:
    _con_object = object()

    @staticmethod
    def get_instance():
        return DBConnection_1._con_object
    
# 2. LAZY INITIALIZATION METHOD
class DBConnection_2:
    _con_object = None

    def __init__(self):
        pass
    
    @staticmethod
    def get_instance():
        if DBConnection_2._con_object is None:
            DBConnection_2._con_object = DBConnection_2()
        return DBConnection_2._con_object

# 3. LAZY INITIALIZATION WITH THREAD SAFETY (DOUBLE LOCKING)
import threading

# OPTION-I
class DBConnection_3:
    _con_object = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._con_object is None:
            with cls._lock:
                if cls._con_object is None:
                    cls._con_object = super(DBConnection_3, cls).__new__(cls)
        return cls._con_object

    def __init__(self):
        pass

    @staticmethod
    def get_instance():
        return DBConnection_3._con_object

# OPTION-II
class DBConnection_4:
    _con_object = None
    _lock = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_instance():
        if DBConnection_4._con_object is None:
            with DBConnection_4._lock:
                if DBConnection_4._con_object is None:
                    DBConnection_4._con_object = DBConnection_4()
        return DBConnection_4._con_object

if __name__ == "__main__":
    con_object_1 = DBConnection_1.get_instance()
    con_object_2 = DBConnection_1.get_instance()
    print(f"Instance ID: {id(con_object_1)}")
    print(f"Instance ID: {id(con_object_2)}")

    con_object_1 = DBConnection_2.get_instance()
    con_object_2 = DBConnection_2.get_instance()
    
    print(f"Instance ID: {id(con_object_1)}")
    print(f"Instance ID: {id(con_object_2)}")

    def test_singleton_3():
        singleton = DBConnection_3.get_instance()
        print(f"Instance ID: {id(singleton)}")
    
    def test_singleton_4():
        singleton = DBConnection_4.get_instance()
        print(f"Instance ID: {id(singleton)}")

     # Create multiple threads to test thread safety
    threads = []
    for i in range(5):
        thread = threading.Thread(target=test_singleton_3)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    
    threads = []
    for i in range(5):
        thread = threading.Thread(target=test_singleton_4)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
        