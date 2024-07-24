class PayrollSystem:
    @staticmethod
    def calculate_payroll(employees):
        print('Calculating Payroll...')

        for employee in employees:
            print(f'Payroll for: {employee.id_} - {employee.name}')
            print(f'Check amount: {employee.calculate_payroll()}', end='\n\n')
