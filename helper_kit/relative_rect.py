
from core.common.enums import *
from core.common.names import  *
from core.common import utils

class RelRect:
    def __init__(self,source_function,*args):
        if len(args) in [4,2]:
            self.rect = FRect(*args)
        else:
            raise ValueError("Bad input.")

        self.init_rect = self.rect.copy()

        self.scale_source_function = source_function
        self.__get_result = FRect(0,0,0,0)


    def get(self,pos_rel=None) -> FRect:
        """
        Multiplies the dimensions of the rectangle with the values acquired from
        the source function and assigns the result to an existing rectangle. Please
        note that this rectangle should not be modified. Use with caution.

        :return: FRect pointer
        """
        if pos_rel is None:
            pos_rel = Vector2(0,0)

        w,h = self.scale_source_function()
        self.__get_result.x = (self.rect.x+pos_rel.x) * w - 1
        self.__get_result.w = self.rect.w * w + 2
        self.__get_result.y = (self.rect.y+pos_rel.y) * h - 1
        self.__get_result.h = self.rect.h * h + 2

        return self.__get_result



    def get_in_rect(self,rect_size:Vector2):
        container_ar = utils.get_aspect_ratio(Vector2(self.rect.size))
        container_ar_group = utils.get_aspect_ratio_group(container_ar)
        in_rect_ar = utils.get_aspect_ratio(rect_size)
        in_rect_ar_converted = in_rect_ar.copy()
        in_rect_ar_group = utils.get_aspect_ratio_group(in_rect_ar_converted)

        res = FRect((0,0),in_rect_ar_converted)
        in_rect_ar_converted.x *= self.rect.w
        in_rect_ar_converted.y *= self.rect.h

        res.size = in_rect_ar_converted
        res.x = self.rect.x
        res.y = self.rect.y

        if in_rect_ar_group == AspectRatioGroup.RECTANGULAR:
            size = min(self.rect.size)
            if container_ar_group == AspectRatioGroup.PORTRAIT:
                res.size = size, size * container_ar.x
            else:
                res.size = size, size * container_ar.x

            res.center = self.rect.center

        elif container_ar_group == AspectRatioGroup.PORTRAIT:
            if in_rect_ar_group == AspectRatioGroup.PORTRAIT :
                # portrait, portrait
                if in_rect_ar.y < container_ar.y:
                    # when the picture is shorter than the container in scale
                    width = min(self.rect.size)
                    res.size = width , width * in_rect_ar.y
                    res.center = self.rect.center
                else:
                    # when the picture is taller than the container in scale
                    height = max(self.rect.size)
                    res.size = height / in_rect_ar.y, height
                    res.center = self.rect.center

            else:
                # portrait, landscape
                width = self.rect.w
                res.size = width , width * in_rect_ar.y
                res.center = self.rect.center

        elif container_ar_group == AspectRatioGroup.LANDSCAPE:
            if in_rect_ar_group == AspectRatioGroup.PORTRAIT :
                # landscape, portrait
                height = self.rect.h
                res.size = height / in_rect_ar.y  ,height
                res.center = self.rect.center
            else:
                # landscape, landscape
                if in_rect_ar.y > container_ar.y :
                    # when the picture is narrower than the container in scale
                    height = self.rect.h
                    res.size = height / in_rect_ar.y, height
                    res.center = self.rect.center
                else :
                    # when the picture is wider than the container in scale
                    width = self.rect.w
                    res.size = width , width * in_rect_ar.y
                    res.center = self.rect.center

        else:
            if in_rect_ar_group == AspectRatioGroup.PORTRAIT :
                # rectangular, portrait
                width = min(self.rect.size)
                res.size = width / in_rect_ar.y , width
                res.center = self.rect.center

            else:
                # rectangular, landscape
                width = self.rect.w
                res.size = width, width * in_rect_ar.y
                res.center = self.rect.center

        w, h = self.scale_source_function()
        res.x = res.x * w - 1
        res.w = res.w * w + 2
        res.y = res.y * h - 1
        res.h = res.h * h + 2

        return res


if __name__ == "__main__":
    # this block tests to see if this helper class is functioning correctly
    def f():
        return 800,600

    rel_rect = RelRect(f,(0.3,0.2),(0.5,0.5))

    print(rel_rect.rect,rel_rect.get())

    rel_rect = RelRect(f, 0.3,0.2,0.5,0.8)

    print(rel_rect.rect, rel_rect.get())

