# -*- coding: utf-8 -*-
import os.path as path
import os
import subprocess


class Comparator():
    """
    Предоставляет функции сравнения двух исходных текстов.
    """
    BAD_FOR_DUPLICATE = "\n"  # пордряд идущие символы из этой сторки удаляются из кода перед началом обработки

    def __init__(self, source1, source2):
        """
        Принимает два параметра source1, source2. Две  строки с исходными кодами.
        """
        self.source1 = self.prepare_source_for_compare(self, source1)
        self.source2 = self.prepare_source_for_compare(self, source2)

    @staticmethod
    def prepare_source_for_compare(self, source):
        """
        Переводит все в нижний регистр и удаляет дупликаты символов из BAD_FOR_DUPLICATES
        """
        letter_list = list(source)
        new_letter_list = list()
        last_letter = None

        for curr_letter in letter_list:
            if not (last_letter == curr_letter and curr_letter in Comparator.BAD_FOR_DUPLICATE):
                new_letter_list.append(curr_letter)

        source = source.lower()
        source = source.replace("\t", "    ")
        return source

    def get_lcs_size(self):
        """
        Возвращает размер наибольшей общей подстроки в исходных кодах.
        """
        lcs_din = [[0 for i in range(len(self.source2) + 1)] for j in range(len(self.source1) + 1)]

        for i in range(1, len(lcs_din)):
            for j in range(1, len(lcs_din[i])):
                lcs_din[i][j] = max(lcs_din[i][j - 1], lcs_din[i - 1][j])
                if self.source1[i - 1] == self.source2[j - 1]:
                    lcs_din[i][j] = max(lcs_din[i][j], lcs_din[i - 1][j - 1] + 1)

        return lcs_din[len(self.source1)][len(self.source2)]

    def probably_equal(self):
        return self.get_lcs_size() / min(len(self.source1), len(self.source2)) > 0.8


class Source():
    def __init__(self, file_path):
        self.path = file_path
        file_path = path.split(file_path)[-1]
        name, self.lang_id = file_path.split(".")
        self.run_id, self.user_id, self.prob_id = name.split("-")
        self.source = open(self.path, "r").read()


def compare_all(contest_path, diff_program, path_log_file):
    contest_path = path.abspath(contest_path)
    diff_program = path.abspath(diff_program)
    log_file = open(path.abspath(path_log_file), "w")
    if not path.isdir(contest_path):
        raise Exception("неверный путь к папке с контестом")
    if not path.isfile(diff_program):
        raise Exception("неверный путь к программе сравнения")
    files = os.listdir()
    for file1id in range(len(files)):
        for file2id in range(len(files)):
            file1name = files[file1id]
            file2name = files[file2id]
            try:
                source1 = Source(path.join(contest_path, file1name))
                source2 = Source(path.join(contest_path, file2name))
            except:
                raise Exception("не могу обработать файлы {0} и {1}".format(file1name, file2name))
            if source1.user_id != source2.user_id and source1.prob_id == source2.prob_id:
                if Comparator(source1.source, source2.source).probably_equal():
                    subprocess.call([diff_program, source1.path, source2.path], stderr=open(os.devnull, "w"),
                                    stdout=open(os.devnull, "w"))
                    s = input("добавить в log файл(y, n)>>").strip().lower()
                    if s == 'y':
                        print("{0} == {1}".format(source1.path, source2.path), file=log_file)
    log_file.close()


