import tw_likes_fetch
import fxer
import telegram_poster


def main():
    tw_likes_fetch.get_likes()
    fxer.fxer()
    telegram_poster.post_msg()
    print('ALL DONE!')


if __name__ == '__main__':
    main()
