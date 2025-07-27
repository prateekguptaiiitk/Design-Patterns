class EmployeeDAO {
    create(client, employeeObj) {
        throw new Error('Abstract method "create()" must be implemented');
    }

    delete(client, employeeId) {
        throw new Error('Abstract method "delete()" must be implemented');
    }

    get(client, employeeId) {
        throw new Error('Abstract method "get()" must be implemented')
    }
}

class EmployeeDAOImpl extends EmployeeDAO {
    create(client, employeeObj) {
        // creates a new row
        console.log('created a new row in employee table')
    }

    delete(client, employeeId) {
        // delete a row
        console.log('deleted a row with employee id:', employeeId)
    }

    get(client, employeeId) {
        // fetch row 
        console.log('fetching data from the DB')
        return new EmployeeDO()
    }
}

class EmployeeDAOProxy extends EmployeeDAO {
    constructor() {
        super()
        this.employeeDAOObj = new EmployeeDAOImpl()
    }

    create(client, employeeObj) {
        if (client == 'ADMIN') {
            this.employeeDAOObj.create(client, employeeObj)
            return 
        } else {
            console.log('Access Denied!')
        }
    }

    delete(client, employeeId) {
        if (client == 'ADMIN') {
            this.employeeDAOObj.delete(client, employeeId)
            return 
        } else {
            console.log('Access Denied!')
        }
    }

    get(client, employeeId) {
        if (client == 'ADMIN') {
            this.employeeDAOObj.get(client, employeeId)
            return 
        } else {
            console.log('Access Denied!')
        }
    }
}

class EmployeeDO {
    constructor(name, id) {
        this.name = name
        this.id = id
    }
}

const employeeTableObj = new EmployeeDAOProxy()
employeeTableObj.create('USER', new EmployeeDO('John', '23'))
employeeTableObj.delete('ADMIN', new EmployeeDO('Doe', '54').id)



