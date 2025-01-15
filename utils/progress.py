def get_water_progress(goal, logged):
    """
    Функция для получения прогресса по воде.
    """
    res = f'''
    Water:
    - Goal: {logged} ml out of {goal}\n
    '''
    if logged >= goal:
        res += 'You have reached your goal! Congratulations!🥳\n'
    else:
        res += f'You have {goal - logged} ml left to reach your goal!💧\n'
    return res
        
def get_calories_progress(goal, logged, burned):
    """
    Функция для получения прогресса по калориям.
    """
    balance = logged - burned
    res = f'''
    Calories:
    - Goal: {logged} kcal out of {goal}
    - Burned: {burned} kcal
    - Balance: {balance} kcal\n
    '''
    if balance < goal:
        res += f'Your daily calorie intake is normal.🍎\n'
    else:
        res += f'Your daily calorie intake is exceeded. Time to go for a run!🏃\n'
    return res