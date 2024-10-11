class Background:
    def __init__(self, image_path: str, image_path_full_hd: str = None) -> None:
        self.image_path = image_path
        self.image_path_full_hd = image_path_full_hd
        self.__resolutions_path_dict: dict[int, str] =  {0: image_path}
        if image_path_full_hd:
            self.__resolutions_path_dict.setdefault(1080, image_path_full_hd)


    def get_path(self, resolution: tuple[int, int] = (1280, 720)) -> str:
        ret_path_index = 0
        for k in self.__resolutions_path_dict:
            if resolution[1] >= k:
                ret_path_index = k
        return self.__resolutions_path_dict[ret_path_index]



