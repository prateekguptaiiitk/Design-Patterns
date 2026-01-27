from abc import ABC, abstractmethod

class EmployeeDAO(ABC):
    @abstractmethod
    def create(self, client, employeeObj):
        pass

    @abstractmethod
    def delete(self, client, employeeId):
        pass

    @abstractmethod
    def get(self, client, employeeId):
        pass

class EmployeeDAOImpl(EmployeeDAO):
    def create(self, client, employeeObj):
        # creates a new row
        print('created a new row in employee table')

    def delete(self, client, employeeId):
        # delete a row
        print('deleted a row with employee id: ', employeeId)

    def get(self, client, employeeId):
        # fetch row
        print('fetching data from the DB')
        return EmployeeDO("Dummy", employeeId)

class EmployeeDAOProxy(EmployeeDAO):
    def __init__(self):
        self.employeeDAOObj = EmployeeDAOImpl()

    def create(self, client, employeeObj):
        if client == 'ADMIN':
            self.employeeDAOObj.create(client, employeeObj)
            return 
        
        raise Exception('Access Denied!')

    def delete(self, client, employeeId):
        if client == 'ADMIN':
            self.employeeDAOObj.delete(client, employeeId)
            return 
        
        raise Exception('Access Denied!')

    def get(self, client, employeeId):
        if client == 'ADMIN' or client == 'USER':
            return self.employeeDAOObj.get(client, employeeId)
        
        raise Exception('Access Denied!')

class EmployeeDO():
    def __init__(self, name, id):
        self.name = name
        self.id = id
    
class ProxyDesignPattern:
    employeeTableObj = EmployeeDAOProxy()
    employeeTableObj.create('USER', EmployeeDO('John', '23'))
    # employeeTableObj.delete('ADMIN', EmployeeDO('Doe', '54').id)
    print('operation executed successfully')



