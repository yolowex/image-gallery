from pygame import FRect

class RelRect:
    def __init__(self,source_function,*args):
        if len(args) in [4,2]:
            self.rect = FRect(*args)
        else:
            raise ValueError("Bad input.")

        self.source_function = source_function
        self.__get_result = FRect(0,0,0,0)


    def get(self) -> FRect:
        """
        Multiplies the dimensions of the rectangle with the values acquired from
        the source function and assigns the result to an existing rectangle. Please
        note that this rectangle should not be modified. Use with caution.

        :return: FRect pointer
        """
        w,h = self.source_function()
        self.__get_result.x = self.rect.x * w
        self.__get_result.w = self.rect.w * w
        self.__get_result.y = self.rect.y * h
        self.__get_result.h = self.rect.h * h

        return self.__get_result


if __name__ == "__main__":
    # this block tests to see if this helper class is functioning correctly

    def f():
        return 800,600

    rel_rect = RelRect(f,(0.3,0.2),(0.5,0.5))

    print(rel_rect.rect,rel_rect.get())

    rel_rect = RelRect(f, 0.3,0.2,0.5,0.8)

    print(rel_rect.rect, rel_rect.get())

