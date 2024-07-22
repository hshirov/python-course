class Employee:
    def __init__(self, id_, name):
        self.id_ = id_
        self.name = name


class SalaryEmployee(Employee):
    def __init__(self, id_, name, weekly_salary):
        super().__init__(id_, name)
        self.weekly_salary = weekly_salary

    def calculate_payroll(self):
        return self.weekly_salary


class HourlyEmployee(Employee):
    def __init__(self, id_, name, hours_worked, hourly_rate):
        super().__init__(id_, name)
        self.hours_worked = hours_worked
        self.hourly_rate = hourly_rate

    def calculate_payroll(self):
        return self.hourly_rate * self.hours_worked


class CommissionEmployee(SalaryEmployee):
    def __init__(self, id_, name, weekly_salary, commission):
        super().__init__(id_, name, weekly_salary)
        self.commission = commission

    def calculate_payroll(self):
        fixed = super().calculate_payroll()
        return fixed + self.commission
