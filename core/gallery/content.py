import moviepy.video.io.VideoFileClip

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
        self.__gif_surface_list: Optional[list[tuple[Surface, float]]] = None
        self.__gif_index: Optional[int] = None
        self.__gif_timer: float = 0

        self.__opencv_video: Optional[cv2.VideoCapture] = None
        self.__moviepy_video: Optional[moviepy.video.io.VideoFileClip] = None
        self.__moviepy_audio: Optional[moviepy.video.io.VideoFileClip.AudioFileClip] =None
        self.__video_fps: Optional[float] = None
        self.__video_total_frames: Optional[float] = None
        self.__video_total_time: Optional[float] = None
        self.__video_current_time: Optional[float] = None
        self.__video_frame_duration: Optional[float] = None
        self.__video_timer: float = 0
        self.__video_is_started = False
        self.__video_is_paused = False


        self.surface: Optional[Surface] = None
        self.texture: Optional[Texture] = None

        self.is_loaded: bool = False
        self.box: RelRect = box
        self.failed_to_load = False
        self.process_type()


    def load_audio(self):
        ...

    def start(self):


        self.__video_is_started = True

    def pause(self):
        ...

    def unpause(self):
        ...

    def stop(self):
        ...

    @property
    def __video_is_playing(self):
        return self.__video_is_started and not self.__video_is_paused

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

    def __get_next_video_frame(self):
        frame = self.__opencv_video.read()[1]
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = numpy.rot90(frame)
        surface = pg.surfarray.make_surface(frame)
        return surface

    def load(self):
        if self.source_type == ContentSourceType.PILLOW:
            try:
                if self.extension == "gif":
                    self.__gif_surface_list = utils.extract_frames_from_gif(self.path)
                    self.__gif_index = 0
                    self.surface = self.__gif_surface_list[0][0]
                    self.__gif_timer = utils.now()

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
        elif self.source_type == ContentSourceType.OPENCV:

            try:
                self.__opencv_video = cv2.VideoCapture(self.path)

                self.texture = Texture.from_surface(cr.renderer,self.__get_next_video_frame())
                self.__video_fps = self.__opencv_video.get(cv2.CAP_PROP_FPS)
                self.__video_total_frames = self.__opencv_video.get(cv2.CAP_PROP_FRAME_COUNT)
                self.__video_total_time = self.__video_total_frames / self.__video_fps
                self.__video_frame_duration = 1 / self.__video_fps
                self.__video_timer = utils.now()

                self.is_loaded = True

                # print(self.__video_fps,self.__video_total_frames,
                #     utils.print_time(self.__video_total_time))

                # self.__moviepy_video = VideoFileClip(self.path)
                # self.__moviepy_audio = self.__moviepy_video.audio
            except Exception as e:
                cr.log.write_log(f"Could not load {self.path} due to this error: {e}",
                    LogLevel.ERROR)
                self.failed_to_load = True
                return


        else:
            cr.log.write_log(
                f"Could not load content, we do not support {self.extension} file types yet.",
                LogLevel.ERROR,
            )

    def unload(self):
        if self.__gif_surface_list is not None:
            self.__gif_surface_list.clear()

        if self.source_type == ContentSourceType.OPENCV:
            self.__opencv_video = None
            self.__moviepy_video = None
            self.__moviepy_audio = None

        self.surface = None
        self.texture = None
        self.is_loaded = False

    def check_events(self):
        if self.type_ == ContentType.GIF:
            current_duration = self.__gif_surface_list[self.__gif_index][1]

            if utils.now() > self.__gif_timer + current_duration:
                self.__gif_index += 1
                if self.__gif_index >= len(self.__gif_surface_list):
                    self.__gif_index = 0

                self.surface = self.__gif_surface_list[self.__gif_index][0]
                self.texture = Texture.from_surface(cr.renderer, self.surface)
                self.__gif_timer = utils.now()

        elif self.type_ == ContentType.VIDEO:
            if self.__video_is_playing:
                if utils.now() > self.__video_timer + self.__video_frame_duration:
                    self.texture.update(self.__get_next_video_frame())
                    self.__video_timer = utils.now()


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
            if self.type_ in [ContentType.PICTURE,ContentType.GIF]:
                self.texture.draw(src_rect, dst_rect)
            else:
                self.texture.draw(src_rect, dst_rect,flip_x=True)


        else:
            if self.type_ in [ContentType.PICTURE,ContentType.GIF]:
                size = Vector2(self.texture.get_rect().size)
                self.texture.draw(src_rect, self.box.get_in_rect(size, True))
            else :
                self.texture.draw(src_rect, dst_rect,flip_x=True)


        if cr.event_holder.should_render_debug:
            self.render_debug()
