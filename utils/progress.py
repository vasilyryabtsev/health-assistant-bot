def get_water_progress(goal, score):
    """
    Функция для получения прогресса по воде.
    """
    res = f'''
    Water:
    - Goal: {score} ml out of {goal}\n
    '''
    if score >= goal:
        res += 'You have reached your goal! Congratulations!🥳\n'
    else:
        res += f'You have {goal - score} ml left to reach your goal!\n'
    return res
        
def get_calories_progress(goal, score):
    """
    Функция для получения прогресса по калориям.
    """
    res = f'''
    Calories:
    - Goal: {score} out of {goal}\n
    '''
    if score >= goal:
        res += 'You have reach your daily calorie goal.🍎\n'
    else:
        res += f'We are {goal - score} kcal away from reaching our calorie goal.\n'
    return res