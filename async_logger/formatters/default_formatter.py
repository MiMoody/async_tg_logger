from logging import Formatter


class DefaultFormatter(Formatter):

    def __init__(self):
        fmt: str = (
            "<b>App logger</b>: %(name)s\n<b>Log level</b>: %(levelname)s\n<b>Path:</b> %(pathname)s\n<b>Line:</b> %(lineno)d\n<b>Message:</b> %(message)s"
        )
        super().__init__(fmt)
