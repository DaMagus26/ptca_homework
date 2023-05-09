import telebot
from drawer import *
from nqueens import *

# Создаем объект бота
bot = telebot.TeleBot('5849676324:AAEgowVAqgtOaPDDhd2CN0IPQ6LH4-6maLc')


def extract_args(cmd):
    args = cmd.split()[1:]
    return args

# Отвечаем на команду /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Этот бот поможет тебе решить задачу о расстановке 8 ферзей на шахматной доске. Для получения решения напиши /solve, а если интересно узнать побольше про бота – /about.")

# Отвечаем на команду /about
@bot.message_handler(commands=['about'])
def send_info(message):
    text = """Меня зовут Степашка. Я – бот, созданный, чтобы продемонстрировать тебе, как решается задача расстановки ферзей на шахматной доске.

Я был создан в качестве домашнего задания по предмету "Прикладная теория цифровых автоматов". Я могу:
1) Объяснить тебе, как решается задача
2) Рассказать, при чем тут цифровые автоматы
3) Показать наглядную gif-визуализацию того, как я решаю эту задачу
 
Если хочешь узнать побольше о задаче, напиши /explain. Если хочешь сразу перейти к решению с визуализацией, напиши /solve.

© Михаил Овакиян ИУ6-44Б"""
    bot.reply_to(message, text)

@bot.message_handler(commands=['explain'])
def send_explanation(message):
    text = """Значит смотри, задача звучит так:
    
    Дано поле 8 на 8 клеток. Как разместить на нем 8 ферзей так, чтобы ни один из них не бил другого?
    
    Задачу можно представить как автомат, у которого состояниями является массив \"*координат*\" ферзей на доске, а входными данными – координаты нового ферзя. Тогда задача сводится к определению последовательности входных данных, при которых автомат перейдет в одно из искомых состояний (коих довольно много)
    
    Нетрудно представить себе рекурсивное решение, где ты ставишь одного ферзя, а затем в одну из тех клеток, куда он не достает, ставишь следующего
    
    Напиши /solve x, где x - количество строк и столбцов на доске, и я подробно обрисую тебе решение"""
    bot.reply_to(message, text)

# Отвечаем на команду /solve
@bot.message_handler(commands=['solve'])
def send_solution(message):
    args = extract_args(message.text)
    if len(args):
        size = int(args[0])
    else:
        bot.send_message(message.chat.id, "После /solve укажи разсер доски (вот так: /solve 8)")
        return

    bot.send_message(message.chat.id, "Дай минутку, сейчас все решу")

    task = NQueens(size)
    task.solve()
    solution = task.first_solution

    path = 'solution_imgs'
    gif = 'solution.gif'
    if os.path.exists(path):
        for file in os.listdir(path):
            os.remove(path + '/' + file)
    else:
        os.mkdir(path)

    if os.path.exists(gif):
        os.remove(gif)

    visualize_solution(solution, path)
    get_gif(path, gif)

    if task.solutions % 10 in [0, 5, 6, 7, 8, 9]:
        word = 'решений'
    elif task.solutions % 10 in [2, 3, 4]:
        word = 'решения'
    else:
        word = 'решение'

    bot.send_message(message.chat.id, f"Всего я нашел {task.solutions} {word} этой задачи. Вот визуализация поиска одного из таких решений")

    with open('solution.gif', 'rb') as gif:
        bot.send_animation(message.chat.id, gif)

    file_names = os.listdir(path)
    file_names.sort(key=lambda x: int(x.split('.')[0][3:]))
    with open(path + '/' + file_names[-1], 'rb') as photo:
        bot.send_photo(message.chat.id, photo)

    for f in os.listdir(path):
        os.remove(path + '/' + f)
    os.rmdir(path)


# Запускаем бота
bot.polling()