import math

def calculate_expression(current_text):
    """Разбирает и вычисляет базовые операции (+, -, *, /)"""
    expression = current_text
    for op in ['+', '-', '*', '/']:
        expression = expression.replace(op, f" {op} ")
        
    parts = expression.split()
    
    if len(parts) != 3:
        return None, "Ой... Выражение неполное. 🥺"
        
    try:
        num1 = float(parts[0])
        operation = parts[1]
        num2 = float(parts[2])
    except ValueError:
        return None, "Я не смогла разобрать числа..."
        
    if operation == '+':
        result = num1 + num2
    elif operation == '-':
        result = num1 - num2
    elif operation == '*':
        result = num1 * num2
    elif operation == '/':
        if num2 == 0:
            return "zero_division", "На ноль делить нельзя... ❌"
        result = num1 / num2
    else:
        return None, "Неизвестная операция"

    if isinstance(result, float) and result.is_integer():
        result = int(result)
        
    return result, "Вот... Всё правильно посчитано? 💙"

def calculate_sqrt(current_text):
    """Вычисляет квадратный корень"""
    try:
        val = float(current_text)
        if val < 0:
            return None, "Из отрицательного числа нельзя... ❌"
        result = math.sqrt(val)
        if result.is_integer():
            result = int(result)
        return result, "Вот... Корень извлечен. 💙"
    except ValueError:
        return None, "Я не могу взять корень из этого..."

def calculate_percent(current_text):
    """Делит текущее число на 100 для получения процентов"""
    try:
        val = float(current_text)
        result = val / 100.0
        if result.is_integer():
            result = int(result)
        return result, "Вот... Перевела в проценты. 💙"
    except ValueError:
        return None, "Сначала введи простое число для процентов... 🥺"
