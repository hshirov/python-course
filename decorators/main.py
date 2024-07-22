from decorators import check_zero_division


@check_zero_division
def divide(a, b):
    return a / b


result = divide(5, 0)

print(result)
