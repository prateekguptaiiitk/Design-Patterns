class ExpenseSplit {
  validateSplitRequest(splitList, totalAmount) {
    throw new Error("Abstract method must be implemented");
  }
}

class EqualExpenseSplit extends ExpenseSplit {
  validateSplitRequest(splitList, totalAmount) {
    const amountShouldBePresent = Math.floor(totalAmount / splitList.length);

    for (let split of splitList) {
      if (split.getAmountOwe() !== amountShouldBePresent) {
        throw new Error("Invalid split amount");
      }
    }
  }
}

class UnequalExpenseSplit extends ExpenseSplit {
  validateSplitRequest(splitList, totalAmount) {
    return;
  }
}

class PercentageExpenseSplit extends ExpenseSplit {
  validateSplitRequest(splitList, totalAmount) {
    return;
  }
}

class Split {
  constructor(user, amount) {
    this.user = user;
    this.amountOwe = amount;
  }

  getUser() {
    return this.user;
  }

  setUser(user) {
    this.user = user;
  }

  getAmountOwe() {
    return this.amountOwe;
  }

  setAmountOwe(amount) {
    this.amountOwe = amount;
  }
}

class Expense {
  constructor(expenseId, description, expenseAmount, paidByUser, splitType, splitDetails) {
    this.expenseId = expenseId;
    this.description = description;
    this.expenseAmount = expenseAmount;
    this.paidByUser = paidByUser;
    this.splitType = splitType;
    this.splitDetails = splitDetails;
  }
}

class ExpenseController {
  constructor() {
    this.balanceSheetController = new BalanceSheetController();
  }

  createExpense(expenseId, description, expenseAmount, paidByUser, splitType, splitDetails) {
    const expenseSplit = new SplitFactory().getSplitObject(splitType);
    expenseSplit.validateSplitRequest(splitDetails, expenseAmount);

    const expense = new Expense(expenseId, description, expenseAmount, paidByUser, splitType, splitDetails);

    this.balanceSheetController.updateUserExpenseBalanceSheet(paidByUser, splitDetails, expenseAmount);

    return expense;
  }
}

const ExpenseSplitType = Object.freeze({
  EQUAL: "EQUAL",
  UNEQUAL: "UNEQUAL",
  PERCENTAGE: "PERCENTAGE",
});

class SplitFactory {
  getSplitObject(splitType) {
    if (splitType === ExpenseSplitType.EQUAL) {
      return new EqualExpenseSplit();
    } else if (splitType === ExpenseSplitType.UNEQUAL) {
      return new UnequalExpenseSplit();
    } else if (splitType === ExpenseSplitType.PERCENTAGE) {
      return new PercentageExpenseSplit();
    } else {
      return null;
    }
  }
}

class Group {
  constructor() {
    this.groupId = null;
    this.groupName = null;
    this.groupMembers = [];
    this.expenseList = [];
    this.expenseController = new ExpenseController();
  }

  addMember(member) {
    this.groupMembers.push(member);
  }

  getGroupId() {
    return this.groupId;
  }

  setGroupId(groupId) {
    this.groupId = groupId;
  }

  setGroupName(groupName) {
    this.groupName = groupName;
  }

  createExpense(expenseId, description, expenseAmount, paidByUser, splitType, splitDetails) {
    const expense = this.expenseController.createExpense(expenseId, description, expenseAmount, paidByUser, splitType, splitDetails);
    this.expenseList.push(expense);
    return expense;
  }
}

class GroupController {
  constructor() {
    this.groupList = [];
  }

  createNewGroup(groupId, groupName, createdByUser) {
    const group = new Group();
    group.setGroupId(groupId);
    group.setGroupName(groupName);
    group.addMember(createdByUser);
    this.groupList.push(group);
  }

  getGroup(groupId) {
    return this.groupList.find((group) => group.getGroupId() === groupId) || null;
  }
}

class User {
  constructor(userId, userName) {
    this.userId = userId;
    this.userName = userName;
    this.userExpenseBalanceSheet = new UserExpenseBalanceSheet();
  }

  getUserId() {
    return this.userId;
  }

  getUserExpenseBalanceSheet() {
    return this.userExpenseBalanceSheet;
  }
}

class UserController {
  constructor() {
    this.userList = [];
  }

  addUser(user) {
    this.userList.push(user);
  }

  getUser(userId) {
    return this.userList.find((user) => user.getUserId() === userId) || null;
  }

  getAllUsers() {
    return this.userList;
  }
}

class Balance {
  constructor() {
    this.amountOwe = 0.0;
    this.amountGetBack = 0.0;
  }

  getAmountOwe() {
    return this.amountOwe;
  }

  setAmountOwe(amountOwe) {
    this.amountOwe = amountOwe;
  }

  getAmountGetBack() {
    return this.amountGetBack;
  }

  setAmountGetBack(amountGetBack) {
    this.amountGetBack = amountGetBack;
  }
}

class BalanceSheetController {
  updateUserExpenseBalanceSheet(expensePaidBy, splits, totalExpenseAmount) {
    const paidByUserExpenseSheet = expensePaidBy.getUserExpenseBalanceSheet();
    paidByUserExpenseSheet.setTotalPayment(paidByUserExpenseSheet.getTotalPayment() + totalExpenseAmount);

    for (let split of splits) {
      const userOwe = split.getUser();
      const oweUserExpenseSheet = userOwe.getUserExpenseBalanceSheet();
      const oweAmount = split.getAmountOwe();

      if (expensePaidBy.getUserId() === userOwe.getUserId()) {
        paidByUserExpenseSheet.setTotalYourExpense(paidByUserExpenseSheet.getTotalYourExpense() + oweAmount);
      } else {
        paidByUserExpenseSheet.setTotalYouGetBack(paidByUserExpenseSheet.getTotalYouGetBack() + oweAmount);

        let userOweBalance = paidByUserExpenseSheet.getUserVsBalance()[userOwe.getUserId()];
        if (!userOweBalance) {
          userOweBalance = new Balance();
          paidByUserExpenseSheet.getUserVsBalance()[userOwe.getUserId()] = userOweBalance;
        }
        userOweBalance.setAmountGetBack(userOweBalance.getAmountGetBack() + oweAmount);

        oweUserExpenseSheet.setTotalYouOwe(oweUserExpenseSheet.getTotalYouOwe() + oweAmount);
        oweUserExpenseSheet.setTotalYourExpense(oweUserExpenseSheet.getTotalYourExpense() + oweAmount);

        let userPaidBalance = oweUserExpenseSheet.getUserVsBalance()[expensePaidBy.getUserId()];
        if (!userPaidBalance) {
          userPaidBalance = new Balance();
          oweUserExpenseSheet.getUserVsBalance()[expensePaidBy.getUserId()] = userPaidBalance;
        }
        userPaidBalance.setAmountOwe(userPaidBalance.getAmountOwe() + oweAmount);
      }
    }
  }

  showBalanceSheetOfUser(user) {
    console.log("---------------------------------------");
    console.log("Balance sheet of user:", user.getUserId());

    const userExpenseBalanceSheet = user.getUserExpenseBalanceSheet();
    console.log("TotalYourExpense:", userExpenseBalanceSheet.getTotalYourExpense());
    console.log("TotalGetBack:", userExpenseBalanceSheet.getTotalYouGetBack());
    console.log("TotalYourOwe:", userExpenseBalanceSheet.getTotalYouOwe());
    console.log("TotalPaymentMade:", userExpenseBalanceSheet.getTotalPayment());

    for (let [userId, balance] of Object.entries(userExpenseBalanceSheet.getUserVsBalance())) {
      console.log("userID:", userId, "YouGetBack:", balance.getAmountGetBack(), "YouOwe:", balance.getAmountOwe());
    }
    console.log("---------------------------------------");
  }
}

class Splitwise {
  constructor() {
    this.userController = new UserController();
    this.groupController = new GroupController();
    this.balanceSheetController = new BalanceSheetController();
  }

  demo() {
    this.setupUserAndGroup();

    const group = this.groupController.getGroup("G1001");
    group.addMember(this.userController.getUser("U2001"));
    group.addMember(this.userController.getUser("U3001"));

    const splits = [
      new Split(this.userController.getUser("U1001"), 300),
      new Split(this.userController.getUser("U2001"), 300),
      new Split(this.userController.getUser("U3001"), 300),
    ];
    group.createExpense("Exp1001", "Breakfast", 900, this.userController.getUser("U1001"), ExpenseSplitType.EQUAL, splits);

    const splits2 = [
      new Split(this.userController.getUser("U1001"), 400),
      new Split(this.userController.getUser("U2001"), 100),
    ];
    group.createExpense("Exp1002", "Lunch", 500, this.userController.getUser("U2001"), ExpenseSplitType.UNEQUAL, splits2);

    for (let user of this.userController.getAllUsers()) {
      this.balanceSheetController.showBalanceSheetOfUser(user);
    }
  }

  setupUserAndGroup() {
    this.addUsersToSplitwiseApp();
    const user1 = this.userController.getUser("U1001");
    this.groupController.createNewGroup("G1001", "Outing with Friends", user1);
  }

  addUsersToSplitwiseApp() {
    this.userController.addUser(new User("U1001", "User1"));
    this.userController.addUser(new User("U2001", "User2"));
    this.userController.addUser(new User("U3001", "User3"));
  }
}

class UserExpenseBalanceSheet {
  constructor() {
    this.userVsBalance = {};
    this.totalYourExpense = 0;
    this.totalPayment = 0;
    this.totalYouOwe = 0;
    this.totalYouGetBack = 0;
  }

  getUserVsBalance() {
    return this.userVsBalance;
  }

  getTotalYourExpense() {
    return this.totalYourExpense;
  }

  setTotalYourExpense(val) {
    this.totalYourExpense = val;
  }

  getTotalYouOwe() {
    return this.totalYouOwe;
  }

  setTotalYouOwe(val) {
    this.totalYouOwe = val;
  }

  getTotalYouGetBack() {
    return this.totalYouGetBack;
  }

  setTotalYouGetBack(val) {
    this.totalYouGetBack = val;
  }

  getTotalPayment() {
    return this.totalPayment;
  }

  setTotalPayment(val) {
    this.totalPayment = val;
  }
}

// Run demo
const splitwise = new Splitwise();
splitwise.demo();
