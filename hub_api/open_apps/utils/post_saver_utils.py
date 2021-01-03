from datetime import date
from random import random

from django.db import IntegrityError
from fuzzywuzzy import process
from open_apps.models.post_saver import Post, SavedPost, Title


def generate_saved_posts(self, logger):
    posts = Post.objects.filter(date=date.today())
    posts_titles = [post.title for post in posts]

    titles = Title.objects.filter(user=self.request.user)

    for item in titles:
        similars = process.extract(item.title, posts_titles, limit=5)
        for title_name, accuracy in similars:
            if accuracy > 89:
                index = posts_titles.index(title_name)
                try:
                    SavedPost.objects.get_or_create(
                        title=posts[index].title, url=posts[index].url, user=self.request.user)
                except IntegrityError:
                    try:
                        new_title = f"{posts[index].title}{str(random())[0:5]}"
                        SavedPost.objects.get_or_create(
                            title=new_title, url=posts[index].url, user=self.request.user)
                    except:
                        continue
                except:
                    logger.exception('This is an unhandled exception.')
                    continue
