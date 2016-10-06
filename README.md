APLCAM
======

This is a ripoff of [futcam](https://github.com/nqpz/futcam), probably
with more bugs, but with filters written in APL!

A filter consists on an APL program that is applied to every frame.
When the program starts, three variables will be defined:

  * `image`, which is a flat integer array containing pixel data in
    RGB format.  Each element encodes one channel of each pixel, and
    the elements are interleaved.  This means that `image[1],
    image[2], image[3]` together describe the red, green, and blue
    channels for the first pixel (row-major I think).

  * `dims`, which is a 3-element vector describing the structure of
    `image`.  You can reshape `image` using this vector to restore the
    original nested structure.  The fact that `image` is a
    1-dimensional array is due to TAIL limitations that should be
    fairly easy to fix.

  * `factor`, which is a floating-point scalar.  This indicates how
    much the filter should be applied, e.g. how a brightness filter
    should change the intensity.  This parameter can be changed at
    runtime by the user using the arrow keys.

If you want to add a filter, just put it in an `.apl` file.  The
Makefile should automatically pick it up.
