from sqladmin import ModelAdmin

from episodes.models import Episode


class EpisodeAdmin(ModelAdmin, model=Episode):
    column_list = [Episode.episode_type,
                   Episode.is_removed,
                   Episode.id,
                   Episode.title,
                   Episode.description,
                   Episode.episode_num,
                   Episode.season_num,
                   Episode.explicit,
                   Episode.show_id,
                   Episode.series,
                   Episode.file_link,
                   Episode.episode_link,
                   Episode.episode_guid,
                   Episode.pub_date,
                   Episode.duration,
                   Episode.cover_image]
