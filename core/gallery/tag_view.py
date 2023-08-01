from core.common.utils import *
from core.common.enums import *
import core.common.constants as constants
from core.common.constants import colors as colors
from core.common.names import *
import core.common.resources as cr
from core.gallery.content import Content
from gui.button import Button
from gui.name_tag import NameTag
from gui.text_view import TextView
from gui.zoom_view import ZoomView
from helper_kit.relative_pos import RelPos
from helper_kit.relative_rect import RelRect
from core.common import utils, assets
from core.sql_agent import SqlAgent


def make_fun(size, con_box):
    ar = utils.get_aspect_ratio(Vector2(size))

    def fun(rect):
        res = rect.copy()
        pa = con_box.get()

        res.x = pa.x
        res.y = pa.y
        res.h = pa.h
        res.w = pa.h / ar.y

    return fun


def make_box_fun(
    text: Texture, box: RelRect, alignment: Alignment = None, con_box=None
):
    fun = make_fun(text.get_rect().size, con_box)

    def new_fun(rect):
        pa = box.get()
        res = fun(rect)
        if alignment == Alignment.CENTER:
            res.center = pa.center
        elif alignment == Alignment.LEFT:
            res.left = pa.left
        elif alignment == Alignment.RIGHT:
            res.right = pa.right

        if res.right > pa.right:
            res.right = pa.right

        return res

    return new_fun


class TagView:
    def __init__(self, box: RelRect):
        self.box = box
        self.font: Font = assets.fonts["mid"]
        self.name_tags: list[NameTag] = []
        self.people_text_view_list: list[TextView] = []
        self.people_location_list: list[Vector2] = []
        # self.people_button_list: list[Button] = []

        self.vertical_margin = 0.01
        self.save_timer = 0
        self.save_duration = 0.5
        self.check_save_timer = False

        def fun(rect):
            # win_size = cr.ws()
            res = rect.copy()
            pa = self.box.get()
            res.x *= pa.w
            res.y *= pa.h
            res.w *= pa.w
            res.h *= pa.h
            res.x += pa.x
            res.y += pa.y
            return res

        def button_fun(rect):
            res = rect.copy()
            pa = self.box.get()
            res.x *= pa.w
            res.y *= pa.h
            res.w *= pa.w
            res.h *= pa.h
            res.x += pa.x
            res.y += pa.y

            lc = res.center
            res.w = res.h
            res.center = lc
            return res

        self.fun = fun
        self.button_fun = button_fun

        self.people_box = RelRect(fun, 0.01, 0.01, 0.8, 0.05, use_param=True)
        self.people_text = TextView(self.people_box, is_entry=False, text="Add People")

        self.add_people_box = RelRect(button_fun, 0.8, 0.01, 0.2, 0.05, use_param=True)

        self.add_people_button = Button(
            "Add People",
            self.add_people_box,
            assets.ui_buttons["tag_add"],
            self.add_person,
            None,
        )

        self.location_box = RelRect(
            self.fun,
            0.01,
            0.01 + (self.people_box.rect.h + self.vertical_margin) * 2,
            0.97,
            self.people_box.rect.h,
            use_param=True,
        )
        self.location_text = TextView(
            self.location_box, is_entry=False, text="Location : ", y_scale=0.75
        )

        self.location_entry_box = RelRect(
            self.fun,
            0.01,
            0.01 + (self.people_box.rect.h + self.vertical_margin) * 3,
            0.97,
            self.people_box.rect.h,
            use_param=True,
        )
        self.location_entry_text = TextView(
            self.location_entry_box, is_entry=True, text="", y_scale=0.75
        )

        self.caption_box = RelRect(
            self.fun,
            0.01,
            0.01 + (self.people_box.rect.h + self.vertical_margin) * 5,
            0.97,
            self.people_box.rect.h,
            use_param=True,
        )
        self.caption_text = TextView(
            self.caption_box, is_entry=False, text="Caption : ", y_scale=0.75
        )

        self.caption_entry_box = RelRect(
            self.fun,
            0.01,
            0.01 + (self.people_box.rect.h + self.vertical_margin) * 6,
            0.97,
            self.people_box.rect.h * 4,
            use_param=True,
        )
        self.caption_entry_text = TextView(
            self.caption_entry_box,
            is_entry=True,
            text="",
            y_scale=0.18,
            line_max_char=20,
        )

    @property
    def any_name_tag_selected(self):
        return any([i.is_selected == True for i in self.name_tags])

    @property
    def text_entries_list(self) -> list[TextView]:
        res = self.people_text_view_list.copy()
        res.extend([self.location_entry_text,self.caption_entry_text])

        return res

    @property
    def zoom_view(self) -> ZoomView:
        return cr.gallery.detailed_view.zoom_view

    def update_name_tags(self):
        def fun(pos: Vector2):
            rect = self.zoom_view.get_picture_rect()

            return Vector2(
                utils.lerp(rect.left, rect.right, pos.x),
                utils.lerp(rect.top, rect.bottom, pos.y),
            )

        for text_view, pos in zip(
            self.people_text_view_list, self.people_location_list
        ):
            text = text_view.text
            rel_pos = RelPos(pos, fun)
            name_tag = NameTag(self)
            name_tag.update_text(text, rel_top_left=rel_pos)
            self.name_tags.append(name_tag)

    def clear(self):
        self.people_text_view_list.clear()
        # self.people_button_list.clear()

        self.location_box = RelRect(
            self.fun,
            0.01,
            0.01 + (self.people_box.rect.h + self.vertical_margin) * 2,
            0.97,
            self.people_box.rect.h,
            use_param=True,
        )
        self.location_text = TextView(
            self.location_box, is_entry=False, text="Location : ", y_scale=0.75
        )

        self.location_entry_box = RelRect(
            self.fun,
            0.01,
            0.01 + (self.people_box.rect.h + self.vertical_margin) * 3,
            0.97,
            self.people_box.rect.h,
            use_param=True,
        )
        self.location_entry_text = TextView(
            self.location_entry_box, is_entry=True, text="", y_scale=0.75
        )

        self.caption_box = RelRect(
            self.fun,
            0.01,
            0.01 + (self.people_box.rect.h + self.vertical_margin) * 4,
            0.97,
            self.people_box.rect.h,
            use_param=True,
        )
        self.caption_text = TextView(
            self.caption_box, is_entry=False, text="Caption : ", y_scale=0.75
        )

        self.caption_entry_box = RelRect(
            self.fun,
            0.01,
            0.01 + (self.people_box.rect.h + self.vertical_margin) * 5,
            0.97,
            self.people_box.rect.h * 4,
            use_param=True,
        )
        self.caption_entry_text = TextView(
            self.caption_entry_box,
            is_entry=True,
            text=" ",
            y_scale=self.caption_entry_text.y_scale,
            line_max_char=self.caption_entry_text.line_max_char,
        )

    def load(self):
        self.name_tags.clear()
        self.people_location_list.clear()

        content: Content = cr.gallery.content_manager.current_content

        if content in assets.reserved_contents:
            return

        self.clear()

        item = cr.sql_agent.pull_item(content.path)

        if not len(item[1]):
            return

        location = None
        caption = None
        for i in item[1]:
            if i[1] == "Location":
                location = i
            if i[1] == "Caption":
                caption = i

        self.location_entry_text.text = location[2]
        self.caption_entry_text.text = caption[2]

        for name in item[0]:
            self.add_person(
                text=name[1], location=Vector2(name[2], name[3]), has_focus=False
            )

        self.location_entry_text.update()
        self.caption_entry_text.update()
        self.update_name_tags()

    def save(self):
        """
        using a thread makes the app run smoothely while calling the save function.
        """

        def operation():
            try:
                content: Content = cr.gallery.content_manager.current_content

                name_tags = []
                for text_view, location in zip(
                    self.people_text_view_list, self.people_location_list
                ):
                    name_tag = [content.path, text_view.text, location.x, location.y]
                    name_tags.append(name_tag)

                perma_tags = []

                if self.location_entry_text.text != "":
                    location_text = self.location_entry_text.text
                else:
                    location_text = " "


                if self.caption_entry_text.text != "":
                    caption_text = self.caption_entry_text.text
                else:
                    caption_text = " "

                if self.caption_entry_text.text == "" and self.location_entry_text.text and not len(self.name_tags):
                    return

                perma_tags.append([content.path, "Location", location_text])
                perma_tags.append([content.path, "Caption", caption_text])

                agent = SqlAgent()
                agent.init()
                agent.push_item(content.path, name_tags, perma_tags)
                self.name_tags.clear()
                self.update_name_tags()
            except Exception as e:
                cr.log.write_log(
                    f"An error occurred while saving changes to database!: {e}",
                    LogLevel.ERROR,
                )

            # self.load(agent)

        th = threading.Thread(target=operation)
        th.start()

    def add_person(self, text="", location=None, has_focus=True):
        for text_entry in self.text_entries_list:
            if text_entry.has_focus:
                return

        if location is None:
            location = Vector2(0.5, 0.5)

        height = 0.05

        y = 0.01 + (1 + len(self.people_text_view_list)) * (
            height + self.vertical_margin
        )

        person_box = RelRect(self.fun, 0.01, y, 0.97, height, use_param=True)
        person_text = TextView(person_box, is_entry=True, text=text)
        person_text.has_focus = has_focus
        # move_person_box = RelRect(self.button_fun, 0.8, y, 0.2, height, use_param=True)
        #
        # move_person_button = Button(
        #     "Move Box",
        #     move_person_box,
        #     assets.ui_buttons["tag_move"],
        #     cr.mouse.enable_virtual,
        #     None,
        # )

        self.people_text_view_list.append(person_text)
        self.people_location_list.append(location)
        # self.people_button_list.append(move_person_button)

        self.sync_perma_tags()

    def sync_people(self):
        height = 0.05

        for index, text_view in enumerate(self.people_text_view_list):
            y = 0.01 + (1 + index) * (height + self.vertical_margin)
            text_view.box.rect.y = y

        # for index, button in enumerate(self.people_button_list):
        #     y = 0.01 + (1 + index) * (height + self.vertical_margin)
        #     button.rel_rect.rect.y = y

    def sync_perma_tags(self):
        height = 0.05

        y = 0.01 + (2 + len(self.people_text_view_list)) * (
            height + self.vertical_margin
        )

        self.location_box = RelRect(
            self.fun,
            self.location_box.rect.x,
            y,
            self.location_box.rect.w,
            self.location_box.rect.h,
            use_param=True,
        )
        self.location_text = TextView(
            self.location_box,
            is_entry=False,
            text="Location : ",
            y_scale=self.location_text.y_scale,
        )

        y = 0.01 + (3 + len(self.people_text_view_list)) * (
            height + self.vertical_margin
        )

        self.location_entry_box = RelRect(
            self.fun,
            self.location_entry_box.rect.x,
            y,
            self.location_entry_box.rect.w,
            self.people_box.rect.h,
            use_param=True,
        )
        self.location_entry_text = TextView(
            self.location_entry_box,
            is_entry=self.location_entry_text.is_entry,
            text=self.location_entry_text.text,
            y_scale=self.location_text.y_scale,
        )

        y = 0.01 + (4 + len(self.people_text_view_list)) * (
            height + self.vertical_margin
        )

        self.caption_box = RelRect(
            self.fun,
            0.01,
            y,
            0.97,
            self.people_box.rect.h,
            use_param=True,
        )
        self.caption_text = TextView(
            self.caption_box, is_entry=False, text="Caption : ", y_scale=0.75
        )

        y = 0.01 + (5 + len(self.people_text_view_list)) * (
            height + self.vertical_margin
        )

        self.caption_entry_box = RelRect(
            self.fun,
            0.01,
            y,
            0.97,
            self.people_box.rect.h * 4,
            use_param=True,
        )
        self.caption_entry_text = TextView(
            self.caption_entry_box,
            is_entry=True,
            text=self.caption_entry_text.text,
            y_scale=self.caption_entry_text.y_scale,
            line_max_char=self.caption_entry_text.line_max_char,
        )

    def trigger_save_timer(self):
        self.save_timer = utils.now()
        self.check_save_timer = True

    def check_save(self):
        for text_entry in self.text_entries_list:
            if text_entry.just_lost_focus:
                self.save()
                break

        if self.check_save_timer and utils.now() > self.save_timer + self.save_duration:
            self.save()
            self.check_save_timer = False

    def check_name_tags(self):
        for name_tag in self.name_tags[::-1]:
            name_tag.check_events()
            if name_tag.just_selected:
                break

    def check_events(self):
        if cr.mouse.just_lost_virtual:
            self.save()

        self.check_name_tags()
        content: Content = cr.gallery.content_manager.current_content
        if content in assets.reserved_contents:
            return

        self.location_text.check_events()
        self.location_entry_text.check_events()
        self.caption_text.check_events()
        self.caption_entry_text.check_events()
        self.people_text.check_events()
        for text_view in self.people_text_view_list:
            text_view.check_events()

        for index, text_view in list(enumerate(self.people_text_view_list))[::-1]:
            if text_view.just_lost_focus and text_view.text == "":
                self.people_text_view_list.pop(index)
                self.people_location_list.pop(index)
                # self.people_button_list.pop(index)
                self.sync_people()
                self.sync_perma_tags()
                self.trigger_save_timer()

        self.add_people_button.check_events()

        # for button in self.people_button_list:
        #     button.check_events()

        self.check_save()

    def render_name_tags(self):
        zv = self.zoom_view
        container = zv.container_box.get()

        for name_tag in self.name_tags:
            if container.colliderect(name_tag.rect):
                name_tag.render()

    def render(self):
        self.render_name_tags()

        content: Content = cr.gallery.content_manager.current_content
        if content in assets.reserved_contents:
            return

        self.people_text.render()
        self.add_people_button.render()

        for text_view in self.people_text_view_list:
            text_view.render()

        # for button in self.people_button_list:
        #     button.render()

        self.location_text.render()
        self.location_entry_text.render()
        self.caption_text.render()
        self.caption_entry_text.render()
