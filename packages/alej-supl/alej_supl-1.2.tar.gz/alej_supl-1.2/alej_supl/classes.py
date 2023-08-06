import re
import requests
from bs4 import BeautifulSoup


class Change:
    def __init__(self, type_, **kwargs):
        if str(type_) == 'odpadá':
            self.new_dismiss(**kwargs)
        elif str(type_) == 'změna':
            self.new_change(**kwargs)
        elif str(type_) == 'přesun >>':
            self.new_move_from(**kwargs)
        elif str(type_) == 'přesun <<':
            self.new_move_to(**kwargs)
        elif str(type_) == 'supluje':
            self.new_substitution(**kwargs)
        elif str(type_) == 'spojí':
            self.new_unification(**kwargs)
        elif str(type_) == 'navíc':
            self.new_extra(**kwargs)
        elif str(type_) == 'absence':
            self.new_event(**kwargs)

    def new_dismiss(self, **kwargs):
        self.type_ = 'dismiss'
        self.lesson = re.compile(r'([0-9]+)\.hod').search(str(kwargs.get('lesson_field'))).group(1)
        self.subject = kwargs.get('subject_field')
        self.class_part = kwargs.get('class_part_field')
        self.extra = kwargs.get('extra_field')

    def new_change(self, **kwargs):
        self.type_ = 'change'
        self.lesson = re.compile(r'([0-9]+)\.hod').search(str(kwargs.get('lesson_field'))).group(1)
        self.subject = kwargs.get('subject_field')
        self.class_part = kwargs.get('class_part_field')
        self.classroom = re.compile(r'[0-9]+').search(str(kwargs.get('classroom_field'))).group()
        self.teacher = kwargs.get('teacher_field')

    def new_move_from(self, **kwargs):
        self.type_ = 'move_from'
        self.lesson = re.compile(r'([0-9]+)\.hod').search(str(kwargs.get('lesson_field'))).group(1)
        self.subject = kwargs.get('subject_field')
        self.class_part = kwargs.get('class_part_field')
        self.extra = kwargs.get('extra_field')

    def new_move_to(self, **kwargs):
        self.type_ = 'move_to'
        self.lesson = re.compile(r'([0-9]+)\.hod').search(str(kwargs.get('lesson_field'))).group(1)
        self.subject = kwargs.get('subject_field')
        self.class_part = kwargs.get('class_part_field')
        self.classroom = re.compile(
            r'\(([Tv0-9]+)\)').search(str(kwargs.get('classroom_field'))).group(1)
        self.teacher = kwargs.get('teacher_field')
        self.extra = kwargs.get('extra_field')

    def new_substitution(self, **kwargs):
        self.type_ = 'substitution'
        self.lesson = re.compile(r'([0-9]+)\.hod').search(str(kwargs.get('lesson_field'))).group(1)
        self.subject = kwargs.get('subject_field')
        self.class_part = kwargs.get('class_part_field')
        self.classroom = re.compile(
            r'\(([Tv0-9]+)\)').search(str(kwargs.get('classroom_field'))).group(1)
        self.teacher = kwargs.get('teacher_field')
        self.extra = kwargs.get('extra_field')

    def new_unification(self, **kwargs):
        self.type_ = 'unification'
        self.lesson = re.compile(r'([0-9]+)\.hod').search(str(kwargs.get('lesson_field'))).group(1)
        self.subject = kwargs.get('subject_field')
        self.class_part = kwargs.get('class_part_field')
        self.classroom = re.compile(
            r'\(([Tv0-9]+)\)').search(str(kwargs.get('classroom_field'))).group(1)
        self.teacher = kwargs.get('teacher_field')
        self.extra = kwargs.get('extra_field')

    def new_extra(self, **kwargs):
        self.type_ = 'extra'
        self.lesson = re.compile(r'([0-9]+)\.hod').search(str(kwargs.get('lesson_field'))).group(1)
        self.subject = kwargs.get('subject_field')
        self.class_part = kwargs.get('class_part_field')
        self.classroom = re.compile(
            r'\(([Tv0-9]+)\)').search(str(kwargs.get('classroom_field'))).group(1)
        self.teacher = kwargs.get('teacher_field')

    def new_event(self, **kwargs):
        self.type_ = 'event'
        self.lesson = int(kwargs.get('lesson'))

    def format_dismiss(self):
        if self.class_part == '\xa0':
            string = 'Odpadá ' + self.lesson + '. hodina' + '(' + self.subject + ')' + '.'
        else:
            string = 'Skupině ' + self.class_part + ' odpadá ' + \
                self.lesson + '. hodina' + '(' + self.subject + ')' + '.'
        return string

    def format_change(self):
        if self.class_part == '\xa0':
            string = self.lesson + '. hodina je ' + self.subject + ' ve třídě ' + \
                self.classroom + ' s učitelemm ' + self.teacher + '.'
        else:
            string = 'Skupina ' + self.class_part + ' má o ' + self.lesson + \
                '. hodině ' + self.subject + ' ve třídě ' + \
                self.classroom + ' s učitelem-' + self.teacher + '.'
        return string

    def format_move_from(self):
        if self.class_part == '\xa0':
            string = self.lesson + '. hodina' + \
                '(' + self.subject + ')' + ' se přesouvá ' + self.extra + '.'
        else:
            string = 'Skupině ' + self.class_part + ' se ' + self.lesson + \
                '. hodina' + '(' + self.subject + ')' + ' přesouvá ' + self.extra + '.'
        return string

    def format_move_to(self):
        if self.class_part == '\xa0':
            string = 'Na ' + self.lesson + '. hodinu se přesouvá ' + \
                self.subject + ' do třídy ' + self.classroom + ' ' + self.extra + '.'
        else:
            string = 'Skupině ' + self.class_part + ' se na ' + self.lesson + '. hodinu přesouvá ' + \
                self.subject + ' do třídy ' + self.classroom + ' ' + self.extra + '.'
        return string

    def format_substitution(self):
        if self.class_part == '\xa0':
            string = self.lesson + '. hodinu supluje ' + self.teacher + \
                ' ve třídě ' + self.classroom + ' a bude se učit ' + self.subject + '.'
        else:
            string = 'Skupině ' + self.class_part + ' supluje ' + self.lesson + '. hodinu ' + \
                self.teacher + ' ve třídě ' + self.classroom + ' a bude se učit ' + self.subject + '.'
        return string

    def format_unification(self):
        if self.class_part == '\xa0':
            string = self.lesson + '. hodinu spojí ' + self.teacher + ' ve třídě ' + \
                self.classroom + ' a bude se učit ' + self.subject + '.'
        else:
            string = 'Skupine ' + self.class_part + ' spojí ' + self.lesson + '. hodinu ' + \
                self.teacher + ' ve třídě ' + self.classroom + ' a bude se učit ' + self.subject + '.'
        return string

    def format_extra(self):
        if self.class_part == '\xa0':
            string = self.lesson + '. hodina je ' + self.subject + ' ve třídě ' + \
                self.classroom + ' s učitelem ' + self.teacher + '.'
        else:
            string = 'Skupina ' + self.class_part + ' má o ' + self.lesson + \
                '. hodině ' + self.subject + ' s učitelem-' + self.teacher + '.'
        return string

    def format_event(self):
        return str(self.lesson) + '.hodinu ' + 'bude školní akce!!!'

    def format(self):
        if self.type_ == 'dismiss':
            return self.format_dismiss()
        elif self.type_ == 'change':
            return self.format_change()
        elif self.type_ == 'move_to':
            return self.format_move_to()
        elif self.type_ == 'move_from':
            return self.format_move_from()
        elif self.type_ == 'substitution':
            return self.format_substitution()
        elif self.type_ == 'unification':
            return self.format_unification()
        elif self.type_ == 'event':
            return self.format_event()
        elif self.type_ == 'extra':
            return self.format_extra()
        else:
            return str(vars(self))


class Connection:
    def __init__(self, date):
        self.date = date
        date_formatted = str(date.strftime('%y%m%d'))
        self.html = requests.get(
            'http://rozvrh-suplovani.alej.cz/suplovani/su' + date_formatted + '.htm')
        self.html.encoding = 'windows-1250'
        self.soup = BeautifulSoup(self.html.text, 'html.parser')

        if self.soup.title.find(text=re.compile('Not found')):
            raise PageNotFoundError

    def supplementation_to_change(self, tr):
        tds = tr.find_all('td')
        change = Change(tds[5].text, lesson_field=tds[1].text, subject_field=tds[2].text,
                        class_part_field=tds[3].text, classroom_field=tds[4].text, teacher_field=tds[6].text,
                        extra_field=tds[7].text)
        return change

    def absence_to_change(self, tr):
        result = []
        tds = tr.find_all('td')
        i = 0
        for td in tds[1:]:
            if re.compile(r'[A-Z0-9]+').match(td.text):
                result.append(Change('absence', lesson=i))
            i += 1
        return result

    def get_supplementation(self, class_code):
        class_re = re.compile('(^|\s)' + class_code)
        result = []
        if self.soup.find('table', {'class': 'tb_supltrid_3'}):
            table = self.soup.find('table', {'class': 'tb_supltrid_3'})
            belongs_to_class = False
            for td in table.find_all('td', {'width': '11%'}):
                if re.compile('[0-9]\.[A-Z]').search(td.text) is not None:
                    if class_re.search(td.text) is not None:
                        result.append(self.supplementation_to_change(td.parent))
                        belongs_to_class = True
                    else:
                        belongs_to_class = False
                elif belongs_to_class:
                    result.append(self.supplementation_to_change(td.parent))
        return result

    def get_absence(self, class_code):
        class_re = re.compile('(^|\s)' + class_code)
        if self.soup.find('table', {'class': 'tb_abtrid_3'}):
            table = self.soup.find('table', {'class': 'tb_abtrid_3'})
            for td in table.find_all('td', {'width': '40%'}):
                if class_re.search(td.text) is not None:
                    return self.absence_to_change(td.parent)

    def get_changes(self, class_code):
        return self.get_supplementation(class_code) + (
            self.get_absence(class_code) if self.get_absence(class_code) is not None else [])


class Error(Exception):
    pass


class PageNotFoundError(Error):
    pass


class NoChangesFoundError(Error):
    pass


class WrongDataError(Error):
    pass


class Lesson():
    def __init__(self, lesson, subject, teacher, classroom, part):
        self.lesson = lesson
        self.subject = subject
        self.teacher = teacher
        self.classroom = classroom
        self.part = part


class Timetable:
    def __init__(self, data):
        if len(data[0]) == 5:
            self.monday = data[1]
            self.tuesday = data[2]
            self.wednesday = data[3]
            self.thursday = data[4]
            self.friday = data[5]
        else:
            raise WrongDataError
