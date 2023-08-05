import json
from celery import shared_task
from telegram import Update, Bot

from bots.models import TelegramBot
from telebaka_channel_helper.bot import post_update
from telebaka_channel_helper.models import PlannedPost


@shared_task
def send_planned_posts():
    bots = PlannedPost.objects.values('bot').distinct()
    for bot in bots:
        bot_instance = TelegramBot.objects.get(pk=bot['bot'])
        bot = Bot(bot_instance.token)
        post = PlannedPost.objects.filter(bot=bot_instance).first()  # type: PlannedPost
        if post:
            post_update(bot_instance, Update.de_json(json.loads(post.update), bot))
            post.delete()
