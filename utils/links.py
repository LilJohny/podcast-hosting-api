from settings import BASE_URL


def get_feed_link(show_id: str):
    return f"{BASE_URL}/rss/{show_id}/feed.xml"


def get_episode_link(show_id: str, episode_id: str):
    return f"{BASE_URL}/podcasts/{show_id}/{episode_id}"


def get_show_link(show_id: str):
    return f"{BASE_URL}/podcasts/{show_id}"
