from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import colors as colors
from core.common.names import *
import core.common.resources as cr
from helper_kit.relative_rect import RelRect
from core.common import utils


class Content:
    def __init__(self, box: RelRect = None, path: str = None):
        self.path: Optional[str] = path
        self.name = path.split("/")[-1]
        self.extension = self.name.split(".")[-1].lower()
        self.source_type: Optional[ContentSourceType] = None
        self.type_: Optional[ContentType] = None
        self.surface: Optional[Surface] = None
        self.texture: Optional[Texture] = None

        self.is_loaded: bool = False
        self.box: RelRect = box

        self.process_type()

    def process_type(self):
        all_source_types = [
            ContentSourceType.PYGAME,
            ContentSourceType.PILLOW,
            ContentSourceType.OPENCV,
        ]

        for i in all_source_types:
            if self.extension in i.value:
                self.source_type = i
                break

        if self.source_type == ContentSourceType.PYGAME:
            self.type_ = ContentType.PICTURE
        elif self.source_type == ContentSourceType.PILLOW:
            if self.extension == "gif":
                self.type_ = ContentType.GIF
            else:
                self.type_ = ContentType.PICTURE

        elif self.source_type == ContentSourceType.OPENCV:
            self.type_ = ContentType.VIDEO

        else:
            raise ValueError(
                f"Invalid content file format, {self.extension} files are not"
                "supported!"
            )

    def load(self):
        if self.source_type == ContentSourceType.PYGAME:
            self.surface = pg.image.load(self.path)
            self.texture = Texture.from_surface(cr.renderer, self.surface)

            # we destroy the surface because it is not needed anymore + it takes a lot of space
            self.surface = None
            self.is_loaded = True

        else:
            cr.log.write_log(
                f"Could not load content, we do not support {self.extension} file types yet.",
                LogLevel.ERROR,
            )

    def unload(self):
        self.texture = None
        self.is_loaded = False

    def check_events(self):
        ...

    def render_debug(self):
        ...

    def render(self, rect: FRect = None):
        if not self.is_loaded:
            cr.log.write_log("Content is not loaded, cannot render!", LogLevel.WARNING)
            return

        if self.box is None and rect is None:
            cr.log.write_log(
                "Content.box is not defined yet and a rect is not provided too"
                ", cannot render!",
                LogLevel.WARNING,
            )
            return

        if rect is not None:
            self.texture.draw(None, rect)

        else:
            if self.type_ == ContentType.PICTURE:
                size = Vector2(self.texture.get_rect().size)
                self.texture.draw(None, self.box.get_in_rect(size, True))

        if cr.event_holder.should_render_debug:
            self.render_debug()
