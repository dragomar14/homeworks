result = None
operand = None
operator = None
wait_for_number = True

while True:
    user_input = input('>>> ')
    if user_input == '=':
        print(result)
        break

    if wait_for_number is True:
        try:
            operand = float(user_input)
        except ValueError:
            print(f"{user_input} isn't a number")
            continue
        wait_for_number = False

        if result is None:
            result = operand

        if operator == '+':
            result += operand
        elif operator == '-':
            result -= operand
        elif operator == '*':
            result *= operand
        elif operator == '/':
            try:
                result /= operand
            except ZeroDivisionError:
                print(f"{operand} is 0")
                continue

    else:
        if user_input in ['+', '-', '*', '/']:
            operator = user_input
            wait_for_number = True
        else:
            print(f'{user_input} not a math operator')
            operator = None
            continue