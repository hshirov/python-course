from employees import SalaryEmployee, HourlyEmployee, CommissionEmployee
from payrollSystem import PayrollSystem

salary_employee = SalaryEmployee(1, 'Joe', 1200)
hourly_employee = HourlyEmployee(2, 'Adam', 40, 20)
commission_employee = CommissionEmployee(3, 'Nick', 1000, 310)

PayrollSystem.calculate_payroll([salary_employee, hourly_employee, commission_employee])
