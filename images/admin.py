from sqladmin import ModelAdmin

from images.models import Image


class ImageAdmin(ModelAdmin, model=Image):
    column_list = [Image.id, Image.title, Image.file_url, Image.is_removed]
