import re
import datetime
import requests
from bs4 import BeautifulSoup
from classes import Change, PageNotFoundError, NoChangesFoundError


def tr_to_Change(tr):
    tds = tr.find_all('td')
    change = Change(tds[5].text, lesson_field=tds[1].text,
                    subject_field=tds[2].text, class_part_field=tds[3].text,
                    classroom_field=tds[4].text, teacher_field=tds[6].text,
                    extra_field=tds[7].text)
    return change


def find_supl(table, class_re):
    changes = []
    belongs_to_class = False
    for td in table.find_all('td', {'width': '11%'}):
        if re.compile('[0-9]\.[A-Z]').search(td.text) is not None:
            if class_re.search(td.text) is not None:
                changes.append(tr_to_Change(td.parent))
                belongs_to_class = True
            else:
                belongs_to_class = False
        elif belongs_to_class:
            changes.append(tr_to_Change(td.parent))
    if not changes:
        raise NoChangesFoundError

    return changes


def find_abs(table, class_re):
    absences = []
    belongs_to_class = False
    for td in table.find_all('td', {'width': '40%'}):
        if re.compile('[0-9]\.[A-Z]').search(td.text) is not None:
            if class_re.search(td.text) is not None:
                absences.append(tr_to_Change(td.parent))
                belongs_to_class = True
            else:
                belongs_to_class = False
        elif belongs_to_class:
            absences.append(tr_to_Change(td.parent))
    if not absences:
        pass

    return absences


# date is a datetime.date object and wanted_class is a string(example:'O6.B')
def get_changes(date, class_code):
    result = []
    date_formated = str(date.strftime('%y%m%d'))
    class_re = re.compile('(^|\s)' + class_code)
    html = requests.get('http://rozvrh-suplovani.alej.cz/suplovani/su' + date_formated + '.htm')
    soup = BeautifulSoup(html.text, 'html.parser')

    if soup.title.find(text=re.compile('Not found')):
        raise PageNotFoundError

    if soup.find('table', {'class': 'tb_supltrid_3'}):
        table = soup.find('table', {'class': 'tb_supltrid_3'})
        result.append(find_supl(table, class_re))

    if soup.find('table', {'class': 'tb_abtrid_3'}):
        table = soup.find('table', {'class': 'tb_abtrid_3'})
        result.append(find_abs(table, class_re))

    return result


def get_multiple_changes(first_day, last_day, class_code):
    result = []
    delta_days = (last_day - first_day).days
    for delta_day in range(0, delta_days + 1):
        day = first_day + datetime.timedelta(days=delta_day)
        result.append(get_changes_text(day, class_code))
    return result


def get_changes_text(day, class_code):
    result = []
    try:
        for change in get_changes(day, class_code)[0]:
            result.append(change.format())
        return result
    except requests.exceptions.ConnectionError:
        return 'The specified URL is not available it might be outdated '
    except PageNotFoundError:
        return 'PageNotFoundError'
    except NoChangesFoundError:
        return 'there are no changes'


def get_changes_and_print_out(day, class_code):
    try:
        for change in get_changes(day, class_code):
            print(change.format())
    except requests.exceptions.ConnectionError:
        print('The specified URL is not available it might be outdated ')
    except PageNotFoundError:
        print('PageNotFoundError')
    except NoChangesFoundError:
        print('there are no changes')


def print_changes_per_day(day, changes):
    print(day.strftime('%d, %b %Y'))
    for change in changes:
        print('  ' + change.format())
