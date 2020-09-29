import json

from django.http import QueryDict

from main.models import Student


class Report:
    id = None
    name = ''
    description = ''

    parameters = {}

    def generate(self):
        """
        Должна вернуть данные для графиков из self.parameters
        Например: {

        }
        :return: dict
        """
        pass

    def __str__(self):
        return json.dumps(self.generate())

    def __init__(self, data: QueryDict):
        data = {k: v[0] if len(v) == 1 and 'list' not in self.parameters[k] else v for k, v in data.lists()}
        for name, value in data.items():
            self.parameters[name]['value'] = value


class CountReport(Report):
    id = 'count'
    name = 'Колличество'

    parameters = {
        'objects': {
            'name': 'Объекты',
            'list': {'Ученики': Student.objects.filter(gender='Мужской'),
                     'Ученицы': Student.objects.filter(gender='Женский')}
        }
    }

    def generate(self):
        queries = list()

        for v in (o := self.parameters['objects'])['value']:
            queries.append({v: [str(s) for s in o['list'][v]]})

        print(queries)
        return {'data': queries}

