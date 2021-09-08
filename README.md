# image2ascii
This is tool converts images inside a directory to ASCII characters. It can be used to transform images into text. Output is colored in most terminals, including Windows command-line and Linux terminal.

-----
## Examples

-----

**Example 1**

_Original Image_

![Example 1](/examples/ex1_before.png)
```
$ python3 run.py -f windows.png -W 200
```
![Example 1](/examples/ex1_after.png)

-----

**Example 2**

_Original Image_

![Example 1](/examples/ex2_before.png)
```
$ python3 run.py -f painting.png -W 200
```
![Example 1](/examples/ex2_after.png)

-----

**Example 3**

_Original Image_

![Example 1](/examples/ex3_before.png)
```
$ python3 run.py -f google.png -W 60
```
![Example 1](/examples/ex3_after.png)

-----

**Example 4**

_Original Image_

![Example 1](/examples/ex4_before.png)
```
$ python3 run.py -f image2.png -W 20 -greysave
```
![Example 1](/examples/ex4_after.png)

_Contents of *output.txt* after running `-greysave` command_
```
 . . . . . . . . . . . . . . ,.,.;q;PlPl
 . . . . . . . . . . . . . ,.,.;q;3;PlP9
 . . . . . . . . . . . . ,.,.;q;3;PlP9$j
 . . . . . . . . . . . ,.,.;q;3;PlP9$j$i
 . . . . . . . . . . ,.,.;q;3;PlP9$j$i#$
 . . . . . . . . . ,.,.;q;3;PlP9$j$i#$@@
 . . . . . . . . ,.,.;q;3;PlP9$j$i#$@@@@
 . . . . . . . ,.,.;q;3;PlP9$j$i#$@@@@@@
 . . . . . . ,.,.;q;3;PlP9$j$i#$@@@@@@@@
 . . . . . ,.,.;q;3;PlP9$j$i#$@@@@@@@@@@
 . . . . ,.,.;q;3;PlP9$j$i#$@@@@@@@@@@@@
 . . . ,.,.;q;3;PlP9$j$i#$@@@@@@@@@@@@@@
 . . ,.,.;q;3;PlP9$j$i#$@@@@@@@@@@@@@@@@
 . ,.,.;q;3;PlP9$j$i#$@@@@@@@@@@@@@@@@@@
 ,.,.;q;3;PlP9$j$i#$@@@@@@@@@@@@@@@@@@@@
.,.;q;T;PlP9$j$i#$@@@@@@@@@@@@@@@@@@@@@@
.;q;3;PlP9$j$i#$@@@@@@@@@@@@@@@@@@@@@@@@
q;3;PlP9$j$i#$@@@@@@@@@@@@@@@@@@@@@@@@@@
T;PlP9$j$i#$@@@@@@@@@@@@@@@@@@@@@@@@@@@@
PlP9$j$i#$@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
```


-----
## Install
Installing **image2ascii** is relatively simple. 

**Start by downloading the GitHub repository:**
```
git clone https://github.com/FFFFFF-base16/image2ascii
```
**Install Python 3.6+, Pillow, and Colorama.**
To install Pillow and Colorama (required modules):
```
pip install pillow colorama
```

-----
## Run
Now that the required packages have been installed, you can run **image2ascii** with the following command:
```
python3 run.py -f filename.png -W 40 -H 40
```
The command above will open "filename.png" (from the same directory), and display a 40x40 command output. A full breakdown of all the possible flags in the command is given below. 

-----
## Settings
When launching **image2ascii** through the command-line, there are different flags you can attach to the command. The table below shows all possible settings.

Argument | Function | Syntax Example
---------|----------|--------
`-h` | Show help. | `-h`
`-f` | The filename of the image inside the directory. _**\*Required**_ | `-f dog.png`
`-W` | The width of the command line output. _Optional_ | `-W 100`
`-H` | The height of the command line output. _Optional_ <br> _Note that if a width flag `-W` is passed but not a height flag `-H`, the height will be automatically calculated to match the aspect ratio of the given width._ | `-H 100`
`-greysave` | Save a file `output.txt` in the directory of the text output. | `-greysave`
`-colorsave` | Save a file `output.txt` in the directory of the text output with ANSI colors flags included (characters will be distorted). | `-colorsave`

-----
## Compatibility
As of September 2021, **image2ascii** has not been tested completely in all operating systems and terminals. So far, it is expected to work in both Linux and Windows.

The color accuracy in the script may be off for certain images, and may require tweaking of the image contrast or the RGB dominant color detection algorithm. Simple, small images will work best with **image2ascii**, such as in _Example 4_ above.