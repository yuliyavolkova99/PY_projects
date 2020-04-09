import tkinter
import json
from tkinter import messagebox as mb

tasks=[]
def my_json(data):
    with open('listOfTask.json', 'w', encoding = 'utf-8') as file:
        json.dump(data, file)
def click():
    try:        
        d = {'Задача': task.get(), 'Категория': category.get(), 'Время': float(time.get())}
        my_json(d)
        tasks.append(d)
        task.delete(0, 'end')
        category.delete(0, 'end')
        time.delete(0, 'end')
        return tasks
    except ValueError:
        mistake = tkinter.Tk()
        mistake.geometry('300x50')
        mistake.title('Ошибка')
        mistake = tkinter.Label(mistake, text= 'Неверный формат задачи времени!')
        mistake.pack()
        mistake.mainloop()
def list_of_task():
        print(tasks)
def quit():
    question = mb.askyesno(title = 'Внимание!', message = 'Вы точно хотите выйти из программы?')
    if question == True:
        window.destroy()
    else:
        pass

window = tkinter.Tk()
window.geometry('300x180')
window.title('Менеджер задач')

a = tkinter.Label(text = 'Задача:').grid(row = 1, column = 0)
b = tkinter.Label(text = 'Категория:').grid(row = 2, column = 0)
c = tkinter.Label(text = 'Время:').grid(row = 3, column = 0)

task = tkinter.Entry(width = 30)
task.grid(row = 1, column = 1)
category = tkinter.Entry(width = 30)
category.grid(row = 2, column = 1)
time = tkinter.Entry(width = 30)
time.grid(row = 3, column = 1)

e = tkinter.Button(window, text = 'Добавить задачу', width = 15, bg = '#bde200', command = click).grid(row = 4, column = 1)
g = tkinter.Button(window, text = 'Список задач', width = 15, bg = '#bcb100', command = list_of_task).grid(row = 5, column = 1)
f = tkinter.Button(window, text = 'Выход', width = 15, bg = '#ccccb3', command = quit).grid(row = 6, column = 1)

window.mainloop()
