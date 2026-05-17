from tkinter import *
from random import *




def create_mushroom():
    global x_mushroom, y_mushroom, vy_mushroom, mushroom
    try:
        canvas.delete(mushroom)
    except:
        pass
    x_mushroom = randint(0, world_width - mushroom_width)
    y_mushroom = 10
    vy_mushroom = randint(5, 15)
    mushroom = canvas.create_image(x_mushroom, y_mushroom, image=myxomor, anchor='nw')


def animate_mushroom():
    global  y_mushroom, vy_mushroom
    y_mushroom += vy_mushroom
    if y_mushroom > world_height - mushroom_height:
        create_mushroom()
    else:
        canvas.coords(mushroom, x_mushroom, y_mushroom)

    if collision_mushroom():
        create_mushroom()

    canvas.after(50, animate_mushroom)


def collision_mushroom():
    global score
    if (x_mushroom < x + actor_width and x_mushroom + mushroom_width > x) and \
            (y_mushroom < y + actor_height and y_mushroom + mushroom_height > y):
        score -= 1
        canvas.itemconfig(counter, text=f'Очки: {score}')
        return True
    return False


def create_fruit():
    global fruits
    x_fruit = randint(0, world_width - fruit_width)
    y_fruit = 0
    vy_fruit = randint(5, 15)
    current_fruit_image = choice(food)
    fruit_id = canvas.create_image(x_fruit, y_fruit, image=current_fruit_image, anchor='nw')

    fruits[fruit_id] = {
        'x': x_fruit,
        'y': y_fruit,
        'vy': vy_fruit,
        'image': current_fruit_image
    }
    animate_fruit(fruit_id)


def animate_fruit(fruit_id):
    if fruit_id in fruits:
        fruit_data = fruits[fruit_id]
        fruit_data['y'] += fruit_data['vy']

        if fruit_data['y'] > delete_fruit:
            canvas.delete(fruit_id)
            del fruits[fruit_id]
            create_fruit()
        else:
            canvas.coords(fruit_id, fruit_data['x'], fruit_data['y'])
            if collision(fruit_data):
                canvas.delete(fruit_id)
                del fruits[fruit_id]
                create_fruit()
            else:
                canvas.after(speed_fruit, animate_fruit, fruit_id)


def collision(fruit_data):
    global score, x, y, actor, actor_width, actor_height, fruit_width,vx
    if (fruit_data['x'] > x and fruit_data['x'] + fruit_width < x + actor_width):
        if (fruit_data['y'] + fruit_width > y):
            score += 1
            canvas.itemconfig(counter, text=f'Очки: {score}')
            return True


    return False


def right(event):
    global vx
    vx = 10


def left(event):
    global vx
    vx = -10


def animate():
    global x, y, vx, speed, actor_width, actor_height
    x += vx
    if x < 0:
        x = 0
    if x > world_width - actor_width:
        x = world_width - actor_width

    canvas.coords(actor, x, y)
    canvas.itemconfig(actor, image=get_current_frame())
    canvas.after(speed, animate)


def get_current_frame():
    global frame_index, vx, photos_r, photos_l
    if vx > 0:
        frame_index = (frame_index + 1) % len(photos_r)
        return photos_r[frame_index]
    else:
        frame_index = (frame_index + 1) % len(photos_l)
        return photos_l[frame_index]

score = 0
mushroom_width = 60
mushroom_height = 70
vy_mushroom = randint(5, 15)
fruit_width = 50
delete_fruit = 500
world_width = 500
world_height = 400
x = 0
y = 250
vx = 10
speed = 50
speed_fruit = 70
actor_width = 60
actor_height = 70

frame_index = 0
fruits = {}
num_fruits = 3

window = Tk()
window.title("Меню")


# Стартовое меню
menu_frame = Frame(window)
menu_frame.pack(padx=150, pady=150)

start_button = Button(menu_frame, text="Играть", font=('Arial', 14))
start_button.pack(pady=10)

exit_button = Button(menu_frame, text="Выход", font=('Arial', 14), command= window.destroy)
exit_button.pack(pady=10)


def start_game():
    # Убираем меню
    menu_frame.pack_forget()


    global canvas, window, mushrooms, actor, counter, x, y, vx, score, fruits # Используем уже существующее окно
    canvas = Canvas(window, width=world_width, height=world_height, bg='white')
    canvas.pack()

    global fon, myxomor, photos_r, photos_l, food
    fon = PhotoImage(file='фон1.png')
    fon_1 = canvas.create_image(0, 0, image=fon, anchor=NW, state='normal')

    myxomor = PhotoImage(file='мухомор.png')
    food = [PhotoImage(file=f'food{i}.png') for i in range(1, 5)]
    photos_r = [PhotoImage(file=f"Ractor{i}.png") for i in range(1, 7)]
    photos_l = [PhotoImage(file=f"Lactor{i}.png") for i in range(1, 7)]

    # Создаем объекты
    global mushroom, actor, counter
    x = 0
    y = 250
    vx = 10
    score = 0
    global frame_index, fruits
    frame_index = 0
    fruits = {}
    mushroom = canvas.create_image(0, 0, image=myxomor, anchor='nw')
    actor = canvas.create_image(x, y, image=photos_r[0], anchor='nw')
    counter = canvas.create_text(350, 50, anchor=SW, font=('Arial', '18'), text=f'Очки: {score}', fill="Black")

    # Создаем гриба и фрукты
    create_mushroom()
    for _ in range(num_fruits):
        create_fruit()

    # Запускаем анимации
    animate()
    animate_mushroom()
    window.bind("d", right)
    window.bind("a", left)


# Связываем кнопку "Играть" с запуском игры
start_button.config(command=start_game)

# Запуск главного цикла
window.mainloop()