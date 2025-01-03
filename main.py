import ptbot
import os
from dotenv import load_dotenv
from pytimeparse import parse


TG_TOKEN = os.getenv('TELEGRAM_TOKEN')


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def wait(chat_id, text):
    delay = parse(text)
    if delay is None:
        bot.send_message(
            chat_id, "Не могу понять время. Введите в формате: '10s', '2m' или '1h'.")
        return

    message_id = bot.send_message(chat_id, f"Осталось {delay} секунд!")

    bot.create_countdown(delay, notify_progress,
                         chat_id=chat_id, message_id=message_id, total=delay)
    bot.create_timer(delay, notify_timeout,
                     chat_id=chat_id)


def notify_progress(secs_left, chat_id, message_id, total):
    iteration = total - secs_left
    progress_bar = render_progressbar(total=total, iteration=iteration)
    bot.update_message(chat_id, message_id,
                       f"Осталось {secs_left} секунд!\n{progress_bar}")


def notify_timeout(chat_id):
    bot.send_message(chat_id, "⏰ Время вышло!")


def main():
    load_dotenv('.env')
    global bot
    bot = ptbot.Bot(TG_TOKEN)
    bot.reply_on_message(wait)
    bot.run_bot()


if __name__ == '__main__':
    main()
