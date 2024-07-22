from decorators import check_zero_division, print_arguments


@check_zero_division
def divide(a, b):
    return a / b


@print_arguments
def print_stuff(x, y, *, z):
    print(x, y, z)


division_result = divide(5, 0)

print_stuff(1, 2, z=3)
