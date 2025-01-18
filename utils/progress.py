from datetime import datetime

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

def calculate_water_data(user):
    """
    Функция для расчета данных о воде.
    """
    water_goal_today, water_balance_today = 0, 0
    if 'water_norm' in user:
        water_goal_today = user['water_norm'][-1][1]
    if 'water_balance' in user:
        filtered = list(filter(lambda x: x[0].date() == datetime.now().date(), user['water_balance']))
        if len(filtered) > 0:
            water_balance_today = sum(map(lambda x: x[1], filtered))
    return water_goal_today, water_balance_today

def calculate_calories_data(user):
    """
    Функция для расчета данных о калориях.
    """
    calories_current, burned_current = 0, 0
    if 'calories_balance' in user:
        calories_balanced_filtered = list(filter(lambda x: x[0].date() == datetime.now().date(), 
                                                 user['calories_balance']))
        if len(calories_balanced_filtered) > 0:
            calories_current = sum([x[2] for x in calories_balanced_filtered])
    
    if 'burned' in user:
        burned_filtered = list(filter(lambda x: x[0].date() == datetime.now().date(), 
                                      user['burned']))
        if len(burned_filtered) > 0:
            burned_current = sum([x[3] for x in burned_filtered])
    
    return calories_current, burned_current