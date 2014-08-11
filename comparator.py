# -*- coding: utf-8 -*-
import os.path as path
import os
import subprocess


class Comparator:
    """
    Предоставляет функции сравнения двух исходных текстов.
    """
    
    def __init__(self, source1, source2, mcl=0.8):
        """
        Принимает два параметра source1, source2. Две  строки с исходными кодами.
        И необязательный пораметр prob=максимальное отношение длинны подпоследовательности
        к длинне минимального из файлов с которого мы считаем пару подозрительной
        """
        self.source1 = Comparator.prepare_source(source1)
        self.source2 = Comparator.prepare_source(source2)
        self.max_common_len = mcl

    @staticmethod
    def prepare_source(source):
        interest_symbols = [':', '(', ')', '{', '}', '[', ']', '<', '>', ';', '+', '-', '*', '**', '/', '=', ',', '+=',
                            '-=', '*=', '/=']
        for i in interest_symbols:
            source = source.replace(i, ' %s ' % i)
        return source

    @staticmethod
    def get_lcs_size(sequence1, sequence2):
        """
        Возвращает размер наибольшей общей подстроки в двух последовательностях.
        """
        lcs_din = [[0 for i in range(len(sequence2) + 1)] for j in range(len(sequence1) + 1)]

        for i in range(1, len(lcs_din)):
            for j in range(1, len(lcs_din[i])):
                lcs_din[i][j] = max(lcs_din[i][j - 1], lcs_din[i - 1][j])
                if sequence1[i - 1] == sequence2[j - 1]:
                    lcs_din[i][j] = max(lcs_din[i][j], lcs_din[i - 1][j - 1] + 1)

        return lcs_din[len(sequence1)][len(sequence2)]

    def probably_equal(self):
        return self.get_lcs_size(self.source1.split(), self.source2.split()) / min(len(self.source1.split()), len(self.source2.split())) > self.max_common_len


class Source:
    """
    хранит информацию об исходном файле
    """
    __slots__ = ['path', 'lang_id', 'run_id', 'user_id', 'prob_id', 'source']

    def __init__(self, file_path):
        self.path = file_path
        file_path = path.split(file_path)[-1]
        name, self.lang_id = file_path.split(".")
        self.run_id, self.user_id, self.prob_id = name.split("-")
        self.source = None

    def __hash__(self):
        return hash(self.get_path(self))

    def get_source(self):
        """
        возвращает код в исходном файле
        """
        if self.source is not None:
            return self.source
        self.source = open(self.path, "r", encoding="utf-8").read()
        return self.source

    def get_lang_id(self):
        return self.lang_id

    def get_user_id(self):
        return self.user_id

    def get_path(self):
        return self.path

    def get_run_id(self):
        return self.run_id

    def get_prob_id(self):
        return self.prob_id


def compare_all(contest_path, diff_program, path_log_file, without_problems, mcl, is_quiet):
    """
    проверяет все файлы в директории contest_path на похожесть
    """
    compare_list(os.listdir(contest_path), contest_path, diff_program, path_log_file, without_problems, mcl, is_quiet)


def compare_list(name_list, contest_path, diff_program, log_file, without_problems, mcl, is_quiet):
    """
    сравнивает на похожесть все файлы из листа name_list
    """
    without_problems = set(without_problems)
    try:
        source_list = [Source(path.join(contest_path, name)) for name in name_list]
    except:
        raise Exception("не могу обработать файлы в директории")
    prob_dict = dict()
    for source in source_list:
        if source.get_prob_id() not in prob_dict:
            prob_dict[source.get_prob_id()] = [source]
        else:
            prob_dict[source.get_prob_id()].append(source)

    for prob in prob_dict:
        if prob not in without_problems:
            print("проверяю задачу %s:" % prob, file=log_file)
            for file1id in range(len(prob_dict[prob])):
                for file2id in range(file1id + 1, len(prob_dict[prob])):
                    source1 = prob_dict[prob][file1id]
                    source2 = prob_dict[prob][file2id]

                    if source1.get_user_id() != source2.get_user_id() and \
                            Comparator(source1.get_source(), source2.get_source(), mcl).probably_equal():
                        if not is_quiet:
                            subprocess.call([diff_program, source1.get_path(), source2.get_path()],
                                            stderr=open(os.devnull, "w"), stdout=open(os.devnull, "w"))

                        print("{0} == {1}".format(source1.get_path(), source2.get_path()), file=log_file)
    print("конец", file=log_file)
    log_file.close()


def choice_last(list_dir):
    """
    возвращяет лист отсортированных последних поссылок(по каждой задаче) каждого пользователя из листа list_dir
    """
    last_dict = dict()
    list_dir.sort()
    try:
        list_dir = [Source(file) for file in list_dir if file[0] != '.']
    except:
        raise Exception("не могу обработь папку")
    for source in list_dir:
        last_dict[source.get_user_id() + " " + source.get_prob_id()] = source.get_path()
    return list(sorted(last_dict.values()))


def compare(contest_path, diff_program=None, log_file=None, without_problems=None, mcl=0.8,
            is_quiet=False, mode='last'):
    """
    сравнивает файлы в папке contest_path с учетом параметров
    """
    if log_file is None:
        log_file = open(os.path.join(os.curdir, "code_diff.log"))

    if diff_program is None:
        diff_program = os.path.join(os.curdir, "code_diff.log")

    if without_problems is None:
        without_problems = list()

    if mode == "last":
        compare_list(choice_last(os.listdir(contest_path)), contest_path, diff_program,
                     log_file, without_problems, mcl, is_quiet)
    else:
        compare_all(contest_path, diff_program, log_file, without_problems, mcl, is_quiet)



