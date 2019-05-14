import cv2
import tempfile
from os import path, makedirs, listdir, remove
import imageio


class VideoService():

    def __init__(self, pt: str, begin: float = 0, end: float = 20):
        self._path = pt
        self._begin = begin
        self._end = end
        self._to_dir = path.join(
            tempfile.gettempdir(), 'jojogif', path.basename(pt))

    def _to_images(self):
        timeF = 3
        c = 1
        folder = path.exists(self._to_dir)
        if not folder:
            makedirs(self._to_dir)
            print("--- create temp folder... ---")
        try:
            vc = cv2.VideoCapture(self._path)
            if vc.isOpened():
                width = vc.get(cv2.CAP_PROP_FRAME_WIDTH)
                height = vc.get(cv2.CAP_PROP_FRAME_HEIGHT)
                fps = vc.get(cv2.CAP_PROP_FPS)
            else:
                raise RuntimeError("cannot open video")
            while True:
                rval, frame = vc.read()
                if frame is None:
                    break

                if c % timeF == 0:
                    frame = cv2.resize(
                        frame, (int(width * 0.5), int(height * 0.5)))
                    cv2.imwrite(f'{self._to_dir}/{c}.jpg', frame)
                c += 1
                cv2.waitKey(1)
        finally:
            vc.release()

    def to_gif(self):
        self._to_images()
        ls = listdir(self._to_dir)
        ls.sort(key=lambda x: int(x.split('.')[0]))
        print(ls)
        outfilename = 'test.gif'

        frames = [imageio.imread(path.join(self._to_dir, image_name))
                  for image_name in ls]

        imageio.mimsave(outfilename, frames, 'GIF')