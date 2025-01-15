def get_workout_data(text):
    """
    Возвращает данные о тренировке.
    """
    text_list = text.split(':')
    name = text_list[0]
    time = int(text_list[1])
    water = 200 * (time // 30) # 200 мл воды на каждые 30 минут тренировки
    return name, time, water
