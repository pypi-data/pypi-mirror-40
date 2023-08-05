import pync
import rumps

from .image_handler import main as set_new_wallpaper


def change_wallpaper(sender):
    set_new_wallpaper()
    pync.notify('Set new wallpaper!', title='WallpaperApp')


class WallpaperStatusBarApp(rumps.App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.wallpaper_timer = rumps.Timer(change_wallpaper, 60 * 60)

    @rumps.clicked('Set new random wallpaper')
    def new_wallpaper(self, sender):
        change_wallpaper(sender)

    @rumps.clicked('Auto change (every hour)')
    def auto_change(self, sender):
        sender.state = not sender.state

        if sender.state:
            self.wallpaper_timer.start()
        else:
            self.wallpaper_timer.stop()


def launch_app():
    WallpaperStatusBarApp('🖼').run()


if __name__ == '__main__':
    launch_app()
