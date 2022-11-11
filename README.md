# LCD162VIDEO
Play videos using an Arduino and a 16x2 character LCD.

## Step 1 - Extract frames from your video
Sample frames from your video to get individual images. _Requires `opencv-python`._
```shell
$ # Recommended: make a directory for all the frames
$ mkdir frames
$ # input, output, input FPS, output FPS
$ python3 convert.py video.mp4 'frames/video-' 30 8
$ ls frames
video-frame-00000000.png
video-frame-00000001.png
video-frame-00000002.png
video-frame-00000003.png
video-frame-00000004.png
video-frame-00000005.png
...
```

## Step 2 - Downscale frames to fit screen
On a 16x2 LCD, 20x16 is a good resolution (4x2 characters). Use something like ImageMagick to do the scaling.
```bash
for f in $(ls frames); do
  convert frames/$f -scale 20x16\! -colorspace gray -depth 8 -type Grayscale converted/$f;
done
```

## Step 3 - Extract raw pixel data from frames
Convert frames into raw data readable by `lcd162video.ino`. _Requires Pillow._
```shell
$ touch rawpixeldata.hpp
$ echo -e <<HEREDOC
#include <Arduino.h>

#define MAGIC __attribute__ ((__section__ (".fini1")))

const uint8_t rawpixeldata[] MAGIC {
HEREDOC >>rawpixeldata.hpp
$
$ # Get maximum frame number from frames/ directory
$ maxframe=$(( $(ls -Uba1 frames | wc -l) - 3 ))
$
$ # Run python script to dump pixel data into C++ header
$ # 128 is threshold for black/white; noinvert/invert controls whether colors are inverted
$ for i in $(seq -f '%08g' 0 $maxframe); do
>   python3 grab-pixels.py converted/video-frame-"$i".png rawpixeldata.hpp "$i" 128 noinvert;
> done
$
$ # End the array with a closing curly bracket and a semicolon
$ echo -e '\n};' >>rawpixeldata.hpp
```

## Step 4 - Edit Arduino program to use your video data
```c++
...

void loop() {
  play(lcd, pgm_get_far_address(rawpixeldata), number_of_frames);

  // Short pause when video finishes
  delay(5000);
}
```

## Step 5 - Compile and upload program to Arduino
Wire up your LCD as follows:
| LCD     | RS | RW | EN | D4 | D5 | D6 | D7 |
|---------|----|----|----|----|----|----|----|
| Arduino | 22 | 24 | 26 | 28 | 30 | 32 | 34 |

Then run `make` to build the program.
```shell
$ make # Plug in your board when it tells you to. Default port is /dev/ttyACM0.
```
