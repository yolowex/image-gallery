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
        self.pure_name = self.name.split(".")[0]
        self.extension = self.name.split(".")[-1].lower()
        self.source_type: Optional[ContentSourceType] = None
        self.type: Optional[ContentType] = None
        self.ctime = time.strftime(
            "%B/%d/%Y", time.localtime(os.path.getctime(self.path))
        )
        self.size = utils.get_file_size(self.path)

        self.__gif_surface_list: Optional[list[tuple[Surface, float]]] = None
        self.__gif_index: Optional[int] = None
        self.__gif_timer: float = 0

        self.opencv_video: Optional[cv2.VideoCapture] = None
        self.__moviepy_video: Optional[moviepy.video.io.VideoFileClip] = None
        self.__moviepy_audio: Optional[
            moviepy.video.io.VideoFileClip.AudioFileClip
        ] = None
        self.video_fps: Optional[float] = None
        self.__video_total_frames: Optional[float] = None
        self.video_total_time: Optional[float] = None
        self.__video_current_time: Optional[float] = None
        self.__video_frame_duration: Optional[float] = None
        self.__video_timer: float = 0
        self.video_is_started = False
        self.video_is_paused = False
        self.__temp_audio_path: Optional[str] = None
        self.__video_audio_sync_timer = -1
        self.__video_audio_sync_duration = 0.01
        self.video_music_start_time = 0
        self.audio_extraction_result: Optional[bool] = None

        self.is_loading_audio = False
        self.video_audio_loaded = False

        self.surface: Optional[Surface] = None
        self.texture: Optional[Texture] = None

        self.is_loaded: bool = False
        self.box: RelRect = box
        self.failed_to_load = False
        self.process_type()

    def load_audio(self):
        self.__temp_audio_path = constants.TEMPDIR + "/tmp.mp3"
        command = (
            f'{constants.FFMPEG_PATH} -y -i "{self.path}" -vn '
            f'-acodec libmp3lame -qscale:a 2 "{self.__temp_audio_path}"'
        )

        cr.log.write_log(
            f"Extracting the audio of {self.name[-10 :]} ...", LogLevel.ANNOUNCE
        )

        try:
            subprocess.check_call(command, shell=True)
            cr.log.write_log(
                f"Audio extraction for {self.name[-10:]} was successful.",
                LogLevel.ANNOUNCE,
            )
            self.audio_extraction_result = True

        except subprocess.CalledProcessError as e:
            cr.log.write_log(
                f"Audio extraction for {self.name} failed due to this error: {e}",
                LogLevel.WARNING,
            )

            cr.log.write_log(
                f"Audio extraction for {self.name[-10:]} failed. ", LogLevel.ANNOUNCE
            )

            self.audio_extraction_result = False

        self.video_audio_loaded = True
        self.is_loading_audio = False
        self.__moviepy_video = None
        self.__moviepy_audio = None

        # self.cancel_audio_extraction = False

    def destroy_audio(self):
        pg.mixer.music.unload()
        self.video_is_started = False
        self.video_is_paused = False
        self.audio_extraction_result = None
        self.video_audio_loaded = False

    def start(self):
        self.video_is_started = True
        # cr.event_holder.determined_fps = self.__video_fps
        # print(cr.event_holder.determined_fps)

    def pause(self):
        music = pg.mixer.music
        self.video_is_paused = True

        if self.audio_extraction_result:
            music.pause()

    def unpause(self):
        music = pg.mixer.music

        self.video_is_paused = False
        if self.audio_extraction_result:
            music.unpause()

    def go_forward(self):
        if self.video_is_paused:
            return

        music = pg.mixer.music

        step = self.video_total_time / 100
        if step < 5:
            step = 5

        if self.audio_extraction_result:
            pos = self.video_music_start_time + music.get_pos() / 1000
            pos += step

            if pos >= self.video_total_time:
                return

            self.video_music_start_time = pos

            music.stop()
            music.play(start=self.video_music_start_time)

        else:
            pos = self.opencv_video.get(cv2.CAP_PROP_POS_FRAMES) / self.video_fps
            pos += step

            if pos >= self.video_total_time:
                return

            self.opencv_video.set(cv2.CAP_PROP_POS_FRAMES, pos * self.video_fps)

        self.update_frame()

    def go_back(self):
        if self.video_is_paused:
            return

        music = pg.mixer.music
        step = self.video_total_time / 100
        if step < 5:
            step = 5

        if self.audio_extraction_result:
            pos = self.video_music_start_time + music.get_pos() / 1000
            pos -= step
            self.video_music_start_time = pos
            if self.video_music_start_time < 0:
                self.video_music_start_time = 0

            music.stop()
            music.play(start=self.video_music_start_time)
        else:
            pos = self.opencv_video.get(cv2.CAP_PROP_POS_FRAMES) / self.video_fps
            pos -= step

            if pos < 0:
                pos = 0

            self.opencv_video.set(cv2.CAP_PROP_POS_FRAMES, pos * self.video_fps)

        self.update_frame()

    @property
    def __video_is_playing(self):
        return self.video_is_started and not self.video_is_paused

    @property
    def resolution(self):
        if not self.is_loaded or self.texture is None:
            return "NaN"

        w, h = self.texture.get_rect().size

        return f"{w}x{h}"

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
                self.type = ContentType.GIF
            else:
                self.type = ContentType.PICTURE

        elif self.source_type == ContentSourceType.OPENCV:
            self.type = ContentType.VIDEO

        else:
            raise ValueError(
                f"Invalid content file format, {self.extension} files are not "
                f"supported!: {self.path}"
            )

    def __get_next_video_frame(self):
        ret, frame = self.opencv_video.read()

        if not ret:
            self.video_is_started = False
            self.opencv_video.set(cv2.CAP_PROP_POS_MSEC, 0)
            ret, frame = self.opencv_video.read()

            ui_layer = cr.gallery.detailed_view.image_ui_layer

            if cr.gallery.get_current_view() == ViewType.FULLSCREEN:
                ui_layer = cr.gallery.fullscreen_view.image_ui_layer

            ui_layer.reverse_trigger_button()

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

            self.surface = None
            self.is_loaded = True

        elif self.source_type == ContentSourceType.OPENCV:
            try:
                self.opencv_video = cv2.VideoCapture(self.path)

                self.texture = Texture.from_surface(
                    cr.renderer, self.__get_next_video_frame()
                )
                self.video_fps = self.opencv_video.get(cv2.CAP_PROP_FPS)
                self.__video_total_frames = self.opencv_video.get(
                    cv2.CAP_PROP_FRAME_COUNT
                )
                self.video_total_time = self.__video_total_frames / self.video_fps
                self.__video_frame_duration = 1 / self.video_fps
                self.__video_timer = utils.now()

                self.is_loaded = True

                # print(self.__video_fps,self.__video_total_frames,
                #     utils.print_time(self.__video_total_time))

                # self.__moviepy_video = VideoFileClip(self.path)
                # self.__moviepy_audio = self.__moviepy_video.audio
            except Exception as e:
                cr.log.write_log(
                    f"Could not load {self.path} due to this error: {e}", LogLevel.ERROR
                )
                self.failed_to_load = True
                return

        else:
            cr.log.write_log(
                f"Could not load content, we do not support {self.extension} file types yet.",
                LogLevel.ERROR,
            )

    def sync_video_with_audio(self):
        music = pg.mixer.music

        audio_cursor = music.get_pos() + self.video_music_start_time * 1000
        # print(audio_cursor)
        self.opencv_video.set(cv2.CAP_PROP_POS_MSEC, audio_cursor)

    def update_frame(self):
        self.texture.update(self.__get_next_video_frame())

    def unload(self):
        if self.__gif_surface_list is not None:
            self.__gif_surface_list.clear()

        if self.source_type == ContentSourceType.OPENCV:
            self.opencv_video = None
            self.__moviepy_video = None
            self.__moviepy_audio = None

        self.surface = None
        self.texture = None
        self.is_loaded = False

    def check_events(self):
        if self.type == ContentType.GIF:
            current_duration = self.__gif_surface_list[self.__gif_index][1]

            if utils.now() > self.__gif_timer + current_duration:
                self.__gif_index += 1
                if self.__gif_index >= len(self.__gif_surface_list):
                    self.__gif_index = 0

                self.surface = self.__gif_surface_list[self.__gif_index][0]
                self.texture = Texture.from_surface(cr.renderer, self.surface)
                self.__gif_timer = utils.now()

        elif self.type == ContentType.VIDEO:
            if self.__video_is_playing and self.audio_extraction_result is not None:
                # print(cr.event_holder.final_fps)

                if self.audio_extraction_result:
                    music = pg.mixer.music

                    if music.get_busy():
                        self.sync_video_with_audio()

                        # print(audio_cursor,video_cursor,video_cursor2)
                        # if utils.now() > self.__video_audio_sync_timer +\
                        #         self.__video_audio_sync_duration:
                        #     self.__video_audio_sync_timer = utils.now()
                        # print(video_cursor, audio_cursor)
                        # print("Syncing the audio")

                        # music.rewind()
                        # music.set_pos(video_cursor)
                    else:
                        music.load(self.__temp_audio_path)
                        music.play()

                if utils.now() > self.__video_timer + self.__video_frame_duration:
                    try:
                        self.update_frame()
                    except cv2.error as e:
                        cr.log.write_log(
                            f"Could not fetch the video frame due to this error: {e}",
                            LogLevel.ERROR,
                        )

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
            if self.type in [ContentType.PICTURE, ContentType.GIF]:
                self.texture.draw(src_rect, dst_rect)
            else:
                self.texture.draw(src_rect, dst_rect, flip_x=True)

        else:
            if self.type in [ContentType.PICTURE, ContentType.GIF]:
                size = Vector2(self.texture.get_rect().size)
                self.texture.draw(src_rect, self.box.get_in_rect(size, True))
            else:
                self.texture.draw(src_rect, dst_rect, flip_x=True)

        if cr.event_holder.should_render_debug:
            self.render_debug()

    @property
    def short_name(self):
        name = self.pure_name
        ext = self.extension

        max_ = 10
        if len(name) >= max_:
            if ext is None:
                return name[:max_] + "..."
            else:
                return name[:max_] + "-." + ext

        return self.name
