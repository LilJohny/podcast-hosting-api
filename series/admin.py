from sqladmin import ModelAdmin

from series.models import Series


class SeriesAdmin(ModelAdmin, model=Series):
    column_list = [Series.show_id, Series.name]
