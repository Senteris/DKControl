import json

from django.http import QueryDict
from django import forms
from django.urls import reverse

from main.models import Student


def form_check(func):
    def wrapper(self):
        r = func(self) if len(self.form.errors) == 0 else {}
        r['form'] = self.get_form()
        return r
    return wrapper


class DynamicForm(forms.Form):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', 0)

        super(DynamicForm, self).__init__(*args, **kwargs)

        for name, item in fields.items():
            self.fields[name] = item['field']
            self.fields[name].label = item['name']
            if 'list' in item:
                self.fields[name].choices = ((x, x) for x, _ in item['list'].items())


class Report:
    id = None
    name = ''
    description = ''
    form: forms.Form

    parameters = {}

    @form_check
    def generate(self):
        """
        Должна вернуть данные для графиков из self.parameters
        Например: {"data": [{"\u0423\u0447\u0435\u043d\u0438\u043a\u0438": 1}, {"\u0423\u0447\u0435\u043d\u0438\u0446\u044b": 0}]}
        :return: dict
        """
        pass

    def get_form(self):
        return """
        <form action='""" + reverse('report_generate', kwargs={'report_type': self.id}) + """' method="get">
            """ + self.form.as_p() + """
            <input type="button" name="ajax-submit" value="Сгенерировать отсчёт">
        </form>
        """

    def __str__(self):
        return json.dumps(self.generate())

    def __init__(self, data: QueryDict = None):
        self.form = DynamicForm(data, fields=self.parameters)

        if data is not None:
            if self.form.is_valid():
                data = {k: v[0] if len(v) == 1 and 'list' not in self.parameters[k] else v for k, v in data.lists()}
                for name, value in data.items():
                    self.parameters[name]['value'] = value
            else:
                self.errors = self.form.errors


class CountReport(Report):
    id = 'count'
    name = 'Количество'

    parameters = {
        'objects': {
            'name': 'Объекты',
            'list': {'Ученики': Student.objects.filter(gender='Мужской'),
                     'Ученицы': Student.objects.filter(gender='Женский')},
            'field': forms.MultipleChoiceField()
        },
        'just_number': {
            'name': 'Просто число',
            'field': forms.IntegerField()
        }
    }

    @form_check
    def generate(self):
        queries = list()

        for v in (o := self.parameters['objects'])['value']:
            queries.append({v: len([str(s) for s in o['list'][v]])})

        return {'data': queries}
