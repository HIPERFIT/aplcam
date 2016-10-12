APLCAM
======

This is a ripoff of [futcam](https://github.com/nqpz/futcam), probably
with more bugs, but with filters written in APL!

A filter consists of an APL program that is applied to every frame.
When the program starts, the following variables will be defined:

  * `image`, which is an array of rank three with dimensions _height_,
    _width_, and 3, where _height_ and _width_ are the dimensions of
    the image and the three inner values are values for the different
    color channels.

  * `h`, which contains the height of the image.

  * `w`, which contains the width of the image.

  * `degree`, which is a floating-point scalar.  This values indicates
    how much the filter should be applied, for instance, how a
    brightness filter should change the intensity.  This parameter can
    be changed at runtime by the user using the arrow keys.

To make a change, a filter should set the `image` variable to a new
value.  The value of `image` at the end of the program constitutes the
new color data.  The size and rank of `image` should not be changed.
Changes to `degree` have no effect.

To add a filter, put it in an `.apl` file.  The Makefile should
automatically pick it up.  The name of the filter must not be a
Futhark keyword.
