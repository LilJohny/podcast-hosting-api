from sqladmin import ModelAdmin

from shows.models import Show


class ShowAdmin(ModelAdmin, model=Show):
    column_list = [Show.language,
                   Show.category,
                   Show.is_removed,
                   Show.id,
                   Show.title,
                   Show.description,
                   Show.show_copyright,
                   Show.show_link,
                   Show.media_link,
                   Show.generator,
                   Show.featured,
                   Show.image,
                   Show.is_locked,
                   Show.owner,
                   Show.last_build_date,
                   Show.feed_file_link]
