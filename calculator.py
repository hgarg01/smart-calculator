# write your code
from collections import deque
import re
# class to define error and custom exceptions
class Error(Exception):
    pass


class InvalidCommand(Error):
    pass


class InvalidIdError(Error):
    pass


class UnknownVarError(Error):
    pass

class InvalidAsgnmnt(Error):
    pass

# function to find the operation from multiple continous operations like +++ , --+ etc
def find_operation(item):
    plus = item.count('+')
    minus = item.count('-')
    times = item.count('*')
    divide = item.count('/')
    if plus:
        if minus:
            if minus % 2 == 1:
                return '-'
            else:
                return '+'
        else:
            return '+'
    elif minus:
        if minus % 2 == 1:
            return '-'
        else:
            return '+'
    elif times == 1:
        return '*'
    elif divide == 1:
        return '/'
    elif item == '^':
        return '^'
    elif item == '(':
        return '('
    elif item == ')':
        return ')'
    elif times > 1 or divide > 1:
        raise NameError
    else:
        return False


def calculate(lst, var_dict):
    operands = []
    operators = []
    list_nums = []
    #if '=' in lst:

    #    return
    # from the input, put every number in operands list and every operation in operators list
    for item in lst:
        if item.lstrip('-').isdigit() or item in var_dict:
            operands.append(item)
        else:
            op = find_operation(item)
            operators.append(op)

    operands = [int(var_dict[x]) if x in var_dict.keys() else int(x) for x in operands]

    # At a time, remove 1 operand and 1 operator from respective lists and put in another list called list_nums
    while len(operators) >= 1:
        op = operators.pop()
        num1 = operands.pop()
        if op == '-':
            if num1 < 0:
                list_nums.append(abs(int(num1)))
            else:
                list_nums.append(int(num1) * -1)
        else:
            list_nums.append(num1)
    last_item = operands.pop()
    if last_item in var_dict:
        list_nums.append(int(var_dict[last_item]))
    else:
        list_nums.append(int(last_item))

    # list_nums = [int(var_dict[x]) if x in vair_dict.keys() else int(x) for x in list_nums]
    # sum of the list is the final answer
    #print(list_nums)
    return(sum(list_nums))


def is_var(var):
    return (all(c.isalpha() for c in var))

def is_operator(var):
    if var in ['+', '-', '=', '*', '/', '^', '(', ')']:
        return True
    else:
        return False

def check_lhs(var):
  if not is_var(var):
    raise InvalidIdError
  else:
      return True

def check_rhs(var, var_dict):
  if var.count('=') >= 1:
    raise InvalidAsgnmnt
  for x in var:
    if not x.isdigit() and not is_operator(x):
        if not is_var(x) :
            raise InvalidAsgnmnt
        elif not x in var_dict:
            raise UnknownVarError


def to_postfix(ip, var_dict):
  #print(ip)
  precedence = {'^' : 3, '*' : 2, '/' : 2, '+' : 1, '-' : 1, '(' : 0, ')' : 0}
  my_stack = deque()
  result = []
  ip.append(')')
  my_stack.append('(')
  for item in ip:
    if item.isdigit() or item in var_dict:
      result.append(item)
    elif item == '(':
      my_stack.append(item)

    elif item == ')':
      x = my_stack.pop()
      while x != '(':
        result.append(x)
        x = my_stack.pop()
    else:
      while my_stack and precedence[my_stack[-1]] >= precedence[item]:
        result.append(my_stack.pop())
      my_stack.append(find_operation(item))

  while my_stack:
    result.append(my_stack.pop())

  return result


def calculate_postfix(postfix, var_dict):
    calculate_stack = deque()
    for item in postfix:
        if item.isdigit():
            calculate_stack.append(item)
        elif item in var_dict:
            calculate_stack.append(var_dict[item])
        else:
            num1 = int(calculate_stack.pop())
            num2 = int(calculate_stack.pop())
            if item == '+':
                calculate_stack.append(num1 + num2)
            elif item == '-':
                calculate_stack.append(num2 - num1)
            elif item == '*':
                calculate_stack.append(num1 * num2)
            elif item == '/':
                calculate_stack.append(num2 // num1)
    return calculate_stack.pop()



var_dict = {}
while True:
    equal = False
    try:
        ip = input()
        equal = False
        if not ip:  # deals with empty line
            continue
        elif "/exit" in ip:
            break
        elif "/help" in ip:
            print("The program converts an expression into postfix notation and calculates the answer. Variables can also be used")
            continue
        elif ip.startswith('/') and ip not in ["/exit", "help"]:
            raise InvalidCommand
        elif '=' in ip:
            equal = True
            lhs = ip[:ip.find('=')].strip(' ')
            rhs = ip[ip.find('=')+1:].split()
            check_lhs(lhs)
            check_rhs(rhs, var_dict)
        else:
            if ip.count('(') != ip.count(')'):
                raise NameError
            split_ip = ip.split()
            for x in split_ip: # checks if every element in input is number or operator
                if not x.lstrip('+-(').rstrip(')').isdigit() :
                    op = find_operation(x)
                    if not is_operator(op):
                        if not is_var(x):
                            raise InvalidIdError
                        elif x not in var_dict:
                            raise UnknownVarError
    except (ValueError, NameError):
        print("Invalid expression")
    except InvalidCommand:
        print("Unknown command")
    except InvalidIdError:
        print("Invalid identifier")
    except UnknownVarError:
        print("Unknown variable")
    except InvalidAsgnmnt:
        print("Invalid Assignment")
    else:  # if no exception occurs
        if equal:
            lhs = ip[:ip.find('=')].strip(' ')
            rhs = ip[ip.find('=')+1:].split()
            var_dict[lhs] = calculate(rhs, var_dict)
        else:
            new_ip = ip.replace('++', '+').replace('+-', '-').replace('-+', '-').replace('--', '+')
            #print(new_ip)
            new_ip = new_ip.replace('+', ' + ').replace('-', ' - ').replace('*', ' * ').replace('/', ' / ').replace('(', ' ( ').replace(')', ' ) ')
            postfix = to_postfix(new_ip.split(), var_dict)
            #print(postfix)
            print(calculate_postfix(postfix, var_dict))

print("Bye!")










