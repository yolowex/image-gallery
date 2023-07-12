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
        self.failed_to_load = False
        self.process_type()

    def process_type(self):
        all_source_types = [
            ContentSourceType.PILLOW,
            ContentSourceType.OPENCV,
        ]

        for i in all_source_types:
            if self.extension in i.value:
                self.source_type = i
                break

        if self.source_type == ContentSourceType.PILLOW:
            if self.extension == "gif":
                self.type_ = ContentType.GIF
            else:
                self.type_ = ContentType.PICTURE

        elif self.source_type == ContentSourceType.OPENCV:
            self.type_ = ContentType.VIDEO

        else:
            raise ValueError(
                f"Invalid content file format, {self.extension} files are not "
                f"supported!: {self.path}"
            )

    def load(self):
        if self.source_type == ContentSourceType.PILLOW:
            try:
                self.surface = utils.open_image_to_pygame_surface(self.path)
                self.texture = Texture.from_surface(cr.renderer, self.surface)
            except Exception as e:
                cr.log.write_log(
                    f"Could not load {self.path} due to this error: {e}", LogLevel.ERROR
                )
                self.failed_to_load = True
                return

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

    def render(self, dst_rect: FRect = None, src_rect: FRect = None):
        if not self.is_loaded:
            cr.log.write_log("Content is not loaded, cannot render!", LogLevel.WARNING)
            return

        if self.box is None and dst_rect is None:
            cr.log.write_log(
                "Content.box is not defined yet and a rect is not provided too"
                ", cannot render!",
                LogLevel.WARNING,
            )
            return

        if dst_rect is not None:
            self.texture.draw(src_rect, dst_rect)

        else:
            if self.type_ == ContentType.PICTURE:
                size = Vector2(self.texture.get_rect().size)
                self.texture.draw(src_rect, self.box.get_in_rect(size, True))

        if cr.event_holder.should_render_debug:
            self.render_debug()
