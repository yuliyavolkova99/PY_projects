import tkinter
from tkinter import messagebox as mb
import tkinter.scrolledtext as scroll
from tkinter import Canvas
import random

rules = '''Добро пожаловать в игру «Змейка»!\n
Суть игры:\n
Вы управляете змейкой, которая двигается по игровому полю (поле ограничено стенками),
собирая яблоки, избегая столкновения с собственным хвостом и краями игрового поля.
Когда змея съедает яблоко, она становится длиннее, что постепенно усложняет игру.\n
Правила игры:\n
1.В начале игры змейка находится в верхнем правом углу игрового поля и состоит из трех элементов(то есть ее размер равен трем).\n
2.Вы управляете змейкой при помощи клавиш (↑ ↓ ← →).\n
3.В правом верхнем углу идет подсчет размера змейки и количества очков.\n
4.Если Вы добрались до яблока, то Вы получаете одно очко и длина змейки увеличивается на один элемент.\n
После взятия игроком текущего яблока, следующее яблоко появляется в случайном месте игрового поля.\n
5.Змейке запрещено сталкиваться с границами игрового поля и с самой собой.
В случае, если змейка врезается в границу игрового поля или в свой хвост – игра заканчивается\n'''

#основное окно 
window = tkinter.Tk()
window.geometry('450x500')
window.title('Snake')
window.resizable(False, False)

#игровое поле
field = Canvas(window, width = 400, height=400, bg = '#94AE03')
field.place(x = 25, y = 10)
field.focus_set()
field.score = 0

#поступающий текст
field.create_text(30, 10, text = f'Счет: {field.score}', tag = 'score', fill = 'black', font = ('Courier New',9))
end = field.create_text(200, 200, text=f"ИГРА ОКОНЧЕНА!", fill = 'black', font = ('Courier New', 20),state='hidden')
new = field.create_text(200, 250, text="НОВАЯ ИГРА", fill = 'white', font = ('Courier New', 15) , state='hidden')

#вспомогательные переменные
field_width = 400
field_height = 400
snake_oval = 10

#элемент
class Element(object):
    def __init__(self, x, y):
        self.example = field.create_oval(x, y, x + snake_oval, y + snake_oval, fill = '#FAD829')
#появление яблок
def eating(): 
    global apple
    posx = snake_oval * random.randint(1, 39)
    posy = snake_oval * random.randint(1, 39)
    apple = field.create_oval(posx, posy, posx + snake_oval, posy + snake_oval, fill="red")
#управление
class Snake(object):
    def __init__(self, parts):
        self.parts = parts
        self.mapping = {'Right': (1, 0), 'Down': (0, 1), 'Left': (-1, 0), 'Up': (0, -1)} #как может двигаться
        self.vector = self.mapping['Right'] #начальное направление
    def move(self):
        for i in range(len(self.parts)-1):
            part = self.parts[i].example
            left_border, up_border, right_border, down_border = field.coords(self.parts[i+1].example)
            field.coords(part, left_border, up_border, right_border, down_border)
        left_border, up_border, right_border, down_border = field.coords(self.parts[-2].example)
        field.coords(self.parts[-1].example, left_border + self.vector[0]*snake_oval, up_border + self.vector[1]*snake_oval,
        right_border + self.vector[0]*snake_oval, down_border + self.vector[1]*snake_oval)
    def add(self): #добавление элемента
        last_oval = field.coords(self.parts[0].example)
        x = last_oval[2] - snake_oval
        y = last_oval[3] - snake_oval
        self.parts.insert(0, Element(x, y))
    def move_dir(self, event): #изменение направления
        if event.keysym in self.mapping:
            self.vector = self.mapping[event.keysym]
    def new(self):#возврат к начальному размеру 
        for part in self.parts:
            field.delete(part.example)
#идентификация
def snake_is():
    parts = [Element(snake_oval, snake_oval),Element(snake_oval*2, snake_oval),Element(snake_oval*3, snake_oval)]
    return Snake(parts)

def start_game():
    global snake
    eating()
    snake = snake_is()
    field.bind("<KeyPress>", snake.move_dir)
    main()
def clicked(event):
    global game
    snake.new()
    game = True
    field.delete(apple)
    field.itemconfigure(end, state='hidden')
    field.itemconfigure(new, state='hidden')
    field.score = 0
    score = field.find_withtag('score')
    field.itemconfigure(score, text = f'Счет: {field.score}', tag = 'score')
    start_game()

#функция статуса игры
game = True
def main(): 
    global game
    if game:
        snake.move()
        head = field.coords(snake.parts[-1].example)
        left_border, up_border, right_border, down_border = head
        if left_border < 0 or up_border < 0 or right_border > 400 or down_border > 400: #условие прекращения игры
            game = False
        elif head == field.coords(apple): #поедание яблок
            snake.add()
            field.delete(apple)
            field.score+=1
            score = field.find_withtag('score')
            field.itemconfigure(score, text = f'Счет: {field.score}', tag = 'score')
            eating()
        else: #если кусает себя
            for i in range(len(snake.parts)-1):
                if head == field.coords(snake.parts[i].example):
                    game = False
        window.after(110, main)
    else:
        visual(end,'normal')
        visual(new,'normal')

def visual(item, state):
    field.itemconfigure(item, state=state)
    
start_game()

#правила игры
def helpp():
    root = tkinter.Toplevel()
    root.geometry('400x450')
    root.title('Snake')
    root.resizable(False, False)
    ress = scroll.ScrolledText(root, width = 45, height = 25)
    ress.place(x = 10, y = 10)
    for x in rules:
        ress.delete('1.0', 'end')
        ress.insert('insert', rules)
    root.mainloop()
#выход из игры
def quit():
    que = mb.askyesno(title = 'Внимание!', message = 'Вы точно хотите выйти из программы?')
    if que == True:
        window.destroy()
    else:
        pass    
#кнопки
field.tag_bind(new, "<Button-1>", clicked)
help_button = tkinter.Button(window, text = 'Правила', width = 25, bg = '#bcb100', command = helpp).place(x = 35,y = 430)
game_out = tkinter.Button(window, text = 'Выход из игры', width = 25, bg = '#ccccb3', command = quit).place(x = 235,y = 430)

window.mainloop()
