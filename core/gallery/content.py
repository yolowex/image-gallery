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
        self.gif_surface_list: Optional[list[tuple[Surface, float]]] = None
        self.gif_index: Optional[int] = None
        self.gif_timer: float = 0

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
                if self.extension == "gif":
                    self.gif_surface_list = utils.extract_frames_from_gif(self.path)

                    self.gif_index = 0
                    self.surface = self.gif_surface_list[0][0]
                    self.gif_timer = utils.now()

                    self.texture = Texture.from_surface(cr.renderer, self.surface)

                else:
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
        self.gif_surface_list.clear()
        self.surface = None
        self.texture = None
        self.is_loaded = False

    def check_events(self):
        if self.extension == "gif":
            current_duration = self.gif_surface_list[self.gif_index][1]

            if utils.now() > self.gif_timer + current_duration:
                self.gif_index += 1
                if self.gif_index >= len(self.gif_surface_list):
                    self.gif_index = 0

                self.surface = self.gif_surface_list[self.gif_index][0]
                self.texture = Texture.from_surface(cr.renderer, self.surface)
                self.gif_timer = utils.now()

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
