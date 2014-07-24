import os
import sys
from tkinter import *
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import threading
from comparator import compare


class CodeDiffGui(Frame):

    def __init__(self, root):
        Frame.__init__(self, root)
        self.quiet = IntVar()
        self.mode = IntVar()
        self.mcl = 0.8
        self.mode_list = ["last", "all"]
        self.compare_thread = None

        self.contest_path_text = Entry(self, width=50, bd=3)
        self.contest_path_text.grid(row=1, column=3, columnspan=5, sticky=NW)
        self.load_contest_directory = Button(self, text="Загрузить поссылки", command=self.load_runs)
        self.load_contest_directory.grid(row=1, column=1, columnspan=2, sticky=NW)

        self.diff_program_path_text = Entry(self, width=50, bd=3)
        self.diff_program_path_text.insert(0, os.path.join(os.curdir, "kdiff3"))
        self.diff_program_path_text.grid(row=2, column=3, columnspan=5, sticky=NW)
        self.choice_diff_program = Button(self, text="Программа сравнения", command=self.load_logfile)
        self.choice_diff_program.grid(row=2, column=1, columnspan=2, sticky=NW)

        self.logfile_path_text = Entry(self, width=50, bd=3)
        self.logfile_path_text.insert(0, os.path.join(os.curdir, "code_diff.log"))
        self.logfile_path_text.grid(row=3, column=3, columnspan=5, sticky=NW)
        self.choice_logfile = Button(self, text="Выбрать .log файл", command=self.load_logfile)
        self.choice_logfile.grid(row=3, column=1, columnspan=2, sticky=NW)

        self.without_problems_label = Label(self, text="Пропустить задачи:", font="Times 17", bd=3)
        self.without_problems_label.grid(row=4, column=1, columnspan=2, sticky=W)
        self.without_problems = Entry(self, width=50, bd=3)
        self.without_problems.grid(row=4, column=3, columnspan=5, sticky=NW)

        self.options_frame = Frame(self)
        self.options_frame.grid(row=5, column=1, sticky=NW)

        self.quiet_checkbox = Checkbutton(self.options_frame, text="только log", font="Times 17", variable=self.quiet)
        self.quiet_checkbox.grid(row=1, columnspan=2, sticky=NW)

        self.mcl_label = Label(self.options_frame, text="Макс. совпадение:", font="Times 17", bd=3)
        self.mcl_label.grid(row=2, column=1, sticky=W)
        self.mcl_text = Entry(self.options_frame, width=4, bd=3)
        self.mcl_text.insert(0, "0.8")
        self.mcl_text.grid(row=2, column=2, sticky=NW)

        self.mode_check1 = Radiobutton(self.options_frame, text='только поcледний', variable=self.mode, value=0)
        self.mode_check2 = Radiobutton(self.options_frame, text='все', variable=self.mode, value=1)
        self.mode_check1.grid(row=3, column=1, sticky=NW)
        self.mode_check2.grid(row=4, column=1, sticky=NW)

        self.log_window_text = Text(self, width=57, height=15, bd=3,  relief=RIDGE)
        self.log_window_text.grid(row=5, column=3, columnspan=5, sticky=NW)

        self.start_stop_frame = Frame(self)
        self.start_stop_frame.grid(row=6, column=7, sticky="NE")
        self.start = Button(self.start_stop_frame, text="Начать", command=self.start_compare)
        self.start.grid(row=1, column=1, columnspan=1, sticky=NE)
        self.start = Button(self.start_stop_frame, text="Стоп", command=self.stop_compare)
        self.start.grid(row=1, column=2, columnspan=1, sticky=NE)

    def load_runs(self):
        open_path = filedialog.askdirectory()
        if open_path == "":
            return
        if not os.path.isdir(open_path):
            return
        self.contest_path_text.delete(0, len(self.contest_path_text.get()))
        self.contest_path_text.insert(0, open_path)

    def load_logfile(self):
        open_file = filedialog.askopenfile()
        if open_file is None:
            return
        self.logfile_path_text.delete(0, len(self.logfile_path_text.get()))
        self.logfile_path_text.insert(0, open_file.name)

    def start_compare(self):
        if self.compare_thread is not None:
            messagebox.showerror("Ошибка при начале сравнения", "Тестирование еще идет")
            return
        if not os.path.isdir(self.contest_path_text.get()):
            messagebox.showerror("Ошибка при начале сравнения", "Неверный путь к контесту.")
            return
        tmp = self.mcl
        try:
            tmp = float(self.mcl_text.get())
        except 'Exception':
            messagebox.showerror("Ошибка при начале сравнения", "Неверное значения макс. совпадения")
            self.mcl = tmp
            return
        self.mcl = tmp
        if self.logfile_path_text.get() != "stdout" and not os.path.exists(os.path.dirname(self.logfile_path_text.get())):
            messagebox.showerror("Ошибка при начале сравнения", "Неверный путь к log файлу")
            return
        if not os.path.isfile(self.diff_program_path_text.get()):
            messagebox.showerror("Ошибка при начале сравнения", "Неверный путь к программе сравнения")
            return

        log_file = None
        if self.logfile_path_text.get().strip() == "stdout":
            log_file = LogWriter(sys.stdout, self.log_window_text)
        else:
            log_file = LogWriter(open(self.logfile_path_text.get(), "w"), self.log_window_text)

        compare(self.contest_path_text.get(), self.diff_program_path_text.get(), log_file,
                self.without_problems.get().split(), self.mcl, self.quiet.get(), self.mode_list[self.mode.get()])

    def stop_compare(self):
        pass


class LogWriter:
    def __init__(self, log_file, log_window_text):
        self.log_file = log_file
        self.log_window = log_window_text
        self.log_window.delete('0.0')

    def write(self, text):
        self.log_file.write(text)
        self.log_window.insert(END, text)

    def close(self):
        self.log_file.close()


if __name__ == "__main__":
    main_window = Tk()
    main_window.title("Code diff")
    main_window.geometry("610x390+40+80")
    main_window.resizable(False, False)
    code_diff = CodeDiffGui(main_window)
    code_diff.pack()
    main_window.mainloop()