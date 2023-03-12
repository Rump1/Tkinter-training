import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb
Arial_11 = ("Arial", 11)

def error_message(error):
    mb.showerror("Ошибка", error)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('250x140')     # Установка размера окна
        self.title("Авторизация")     # Название окна
        self.resizable(width=False, height=False)   # Запрещаем менять размер окна

        user_label = tk.Label(self, text="user", font=Arial_11, width=25)    # Текст "user"
        user_label.grid(row=0, column=0, sticky="S", padx=10)
        user_entry = tk.Entry(self, width=25)     # Поле для ввода user
        user_entry.grid(row=1, column=0, sticky="N", padx=10)

        pwd_label = tk.Label(self, text="password", font=Arial_11, width=25)     # Текст "password"
        pwd_label.grid(row=2, column=0, sticky="S", padx=10)
        pwd_entry = tk.Entry(self, width=25)     # Поле для ввода password
        pwd_entry.grid(row=3, column=0, sticky="N", padx=10)

        '''
        В параметр command для кнопки можно запихать лямбда функцию, чтобы использовать эту функцию с параметрами.
        Таким образом происходит передача заполненных пользователем данных
        '''
        connect_button = tk.Button(self, text="Войти", font=Arial_11, width=10,
                                   command=lambda: self.enter_button(user_entry.get(), pwd_entry.get()))
        connect_button.grid(row=4, column=0, pady=10, padx=10)

    def enter_button(self, user, password): # Что происходит при нажатии на кнопку
        Config_window(self)     # Открываем новое окно

class Config_window(tk.Toplevel):
    def __init__(self, parent_window):
        parent_window.withdraw()
        tk.Toplevel.__init__(self, parent_window)      # Инициализация окна
        self.title("Config")  # Название окна
        self.protocol("WM_DELETE_WINDOW",
                               lambda: parent_window.destroy())  # Уничтожение main окна при выключении окна настроек

        container = tk.Frame(self)
        container.pack(fill="both", expand="yes")

        self.frames = {}
        for Frame in (Dictionary_page, Tumbler_page):
            frame = Frame(container, self)
            self.frames[Frame] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Dictionary_page)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class Dictionary_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        mode_panel = tk.Frame(self)    # Фрейм с кнопками переключения режима
        mode_panel.grid(row=0, column=0, sticky="ew", columnspan=3)  # Фрейм для кнопок переключения страниц

        to_dictionary = tk.Button(mode_panel, text="К словарю", font=('Arial', 10), width=11, state="disabled", relief="sunken")
        to_dictionary.grid(row=0, column=0)     # Кнопка "К словарю" неактивна

        to_config = tk.Button(mode_panel, text="К настройкам", font=('Arial', 10),   # Кнопка "к настройкам" переключает страницу
                              command=lambda: controller.show_frame(Tumbler_page))
        to_config.grid(row=0, column=2)

        words_listbox = tk.Listbox(self)  # Размещение листбокса для слов в гриде
        words_listbox.grid(row=1, column=0, columnspan=3, sticky="news")

        scrollbar = tk.Scrollbar(self)  # Размещение скроллбара в гриде
        scrollbar.grid(row=1, column=3, sticky="nws")

        words_listbox.config(yscrollcommand=scrollbar.set)  # Прикрепление скроллбара к листбоксу
        scrollbar.config(command=words_listbox.yview)

        word_entry = tk.Entry(self, width=25)
        word_entry.grid(row=2, column=0, sticky="w")

        entry_button = tk.Button(self, text="Добавить", font=('Arial', 10),
                                 command=lambda: self.add_to_dictionary(words_listbox, word_entry.get()))
        entry_button.grid(row=2, column=1, sticky="e")

        entry_button = tk.Button(self, text="Удалить", font=('Arial', 10),
                                 command=lambda: self.delete_from_dictionary(words_listbox))
        entry_button.grid(row=2, column=2, sticky="e")

    def add_to_dictionary(self, words_listbox, word):
        if (word):
            words_listbox.insert("end", word)
        else:
            error_message("Введите слово для добавления")

    def delete_from_dictionary(self, words_listbox):
        if (words_listbox.curselection()):
            words_listbox.delete(words_listbox.curselection())
        else:
            error_message("Выберите элемент из списка")


class Tumbler_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


        to_dictionary = tk.Button(self, text="К словарю", font=('Arial', 10), width=11,  # Кнопка "к словарю" переключает страницу
                                  command=lambda: controller.show_frame(Dictionary_page))
        to_dictionary.grid(row=0, column=0)

        to_config = tk.Button(self, text="К настройкам", font=('Arial', 10), state="disabled", relief="sunken")
        to_config.grid(row=0, column=1)     # Кнопка "К настройкам" неактивна

        disclaimer_button = tk.Checkbutton(self, text="Отображение дисклеймера")
        disclaimer_button.grid(row=1, column=0, columnspan=2, sticky="w", pady=10)

        blur_button = tk.Checkbutton(self, text="Замыливание текста")
        blur_button.grid(row=2, column=0, columnspan=2, sticky="w", pady=10)

        sound_button = tk.Checkbutton(self, text="Звук")
        sound_button.grid(row=3, column=0, columnspan=2, sticky="w", pady=10)


def main():
    autorization_window = App()
    autorization_window.mainloop()

if __name__ == "__main__":
    main()