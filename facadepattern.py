class EmployeeClient:
    def get_employee_details(self):
        employee_facade = EmployeeFacade()
        employee_details = employee_facade.get_employee_details(121222)

class EmployeeFacade:
    employee_DAO = None

    def __init__(self):
        self.employee_DAO = EmployeeDAO()

    def insert(self):
        self.employee_DAO.insert()
    
    def get_employee_details(self, empID):
        return self.employee_DAO.get_employee_details(empID)

class EmployeeDAO:
    def insert(self):
        # insert into employee table
        pass
    
    def update_employee_name(self):
        # updating employee name
        pass

    def get_employee_details(self, emailID):
        # get employee details based on Emp ID
        return Employee()