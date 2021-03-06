#!/usr/bin/env python

import sys
import argparse
import collections
import time

import pygame
import numpy
import cv2

import filters
import inspect

class FutCam:
    def __init__(self, resolution=None, scale_to=None):
        self.resolution = resolution
        self.scale_to = scale_to

    def run(self):
        # Open a camera device for capturing.
        self.cam = cv2.VideoCapture(0)

        if not self.cam.isOpened():
            print >> sys.stderr, 'error: could not open camera.'
            return 1

        if self.resolution is not None:
            w, h = self.resolution
            self.cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, w)
            self.cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, h)

        if self.scale_to is not None:
            self.width, self.height = self.scale_to
        else:
            self.width = int(self.cam.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
            self.height = int(self.cam.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))

        # Load the library.
        self.futhark = filters.filters(interactive=True)

        # Setup pygame.
        pygame.init()
        pygame.display.set_caption('futcam')
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()

        # Determine the filters using inspection.
        self.filters = {}
        for name,f in inspect.getmembers(filters.filters, predicate=inspect.ismethod):
            if name != '__init__' and not name.startswith('futhark_'):
                def makeApply(name, f):
                    def applyFilter(frame, dims, user_value):
                        return f(self.futhark, frame, dims, numpy.array([user_value], dtype=numpy.float32))
                    return applyFilter
                self.filters[name] = makeApply(name, f)

        return self.loop()

    def message(self, what, where):
        text = self.font.render(what, 1, (255, 255, 255))
        self.screen.blit(text, where)

    def loop(self):
        filter_names = self.filters.keys()
        filter_index = 0

        applied_filters = []

        show_hud = True

        user_value = 0
        user_value_status = 0
        user_values = []
        user_value_change_speed = 13
        while True:
            fps = self.clock.get_fps()

            # Read frame.
            time_start = time.time()
            retval, frame = self.cam.read()
            if not retval:
                return 1
            time_end = time.time()
            cam_read_dur_ms = (time_end - time_start) * 1000

            # Mess with the internal representation.
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Scale if asked to.
            if self.scale_to is not None:
                w, h = self.scale_to
                frame = cv2.resize(frame, (w,h))
                #frame = self.futhark.scale_to(frame, w, h)

            dims = numpy.asarray(frame.shape, dtype=numpy.int32)
            frame = frame.reshape(numpy.product(dims)).astype(numpy.int32)
                
            # Call stacked filters.
            time_start = time.time()
            for i, u in zip(applied_filters, user_values):
                frame = self.filters[filter_names[i]](frame, dims, u)

            # Apply the currently selected filter.
            frame = self.filters[filter_names[filter_index]](frame, dims, user_value).get()

            time_end = time.time()
            futhark_dur_ms = (time_end - time_start) * 1000

            # Mess with the internal representation.
            frame = numpy.transpose(frame.reshape(dims), axes=[1,0,2])

            # Show frame.
            pygame.surfarray.blit_array(self.screen, frame)

            # Render HUD.
            if show_hud:
                for i, fi, u in zip(range(len(applied_filters)), applied_filters, user_values):
                    self.message('%s %.2f' % (filter_names[fi],u), (5, 5 + 30 * i))
                self.message('%s %.2f?' % (filter_names[filter_index], user_value),
                             (5, 5 + 30 * len(applied_filters)))
                self.message('Camera read: {:.02f} ms'.format(cam_read_dur_ms),
                             (self.width - 310, 5))
                self.message('APL: {:.02f} ms'.format(futhark_dur_ms),
                             (self.width - 250, 35))
                self.message('FPS: {:.02f}'.format(fps),
                             (self.width - 210, 65))

            # Show on screen.
            pygame.display.flip()

            # Check events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        return 0

                    elif event.key == pygame.K_UP:
                        filter_index = (filter_index - 1) % len(self.filters)
                    elif event.key == pygame.K_DOWN:
                        filter_index = (filter_index + 1) % len(self.filters)

                    elif event.key == pygame.K_RETURN:
                        applied_filters.append(filter_index)
                        user_values.append(user_value)
                        user_value = 0
                    elif event.key == pygame.K_BACKSPACE:
                        if len(user_values) > 0:
                            filter_index = applied_filters[-1]
                            applied_filters = applied_filters[:-1]
                            user_value = user_values[-1]
                            user_values = user_values[:-1]
                    elif event.key == pygame.K_LEFT:
                        user_value_status = -1
                    elif event.key == pygame.K_RIGHT:
                        user_value_status = 1

                    elif event.key == pygame.K_h:
                        show_hud = not show_hud

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        user_value_status = 0
                    elif event.key == pygame.K_RIGHT:
                        user_value_status = 0

            if user_value_status != 0:
                user_value += user_value_status * (user_value_change_speed / fps)

            self.clock.tick()

def main(args):
    def size(s):
        return tuple(map(int, s.split('x')))

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--resolution', type=size, metavar='WIDTHxHEIGHT',
                            help='set the resolution of the webcam instead of relying on its default resolution')
    arg_parser.add_argument('--scale-to', type=size, metavar='WIDTHxHEIGHT',
                            help='scale the camera output to this size before sending it to a filter')
    args = arg_parser.parse_args(args)

    cam = FutCam(resolution=args.resolution, scale_to=args.scale_to)
    return cam.run()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
