import os.path
import sys
from collections import OrderedDict

from colorama import Fore, Back, Style
from PIL import Image

from typing import List
from typing import Any
from typing import Tuple
from typing import Dict

SETTINGS = {
    'default_width' : 10, #Height/Width if argument is not passed
    'default_height' : 10, # "
}

class Create:
    def __init__(self, filename: str, width: int, height: int) -> None:
        self.logger = Logger(__name__)
        self.RgbToString = RgbToString()
        self.filename = filename
        self.width = width or SETTINGS['default_width']
        self.height = height or SETTINGS['default_height']
        self.colorMap: List[List[int]] = [[]]
        self.image: Any = None #Pillow does not support typing yet, from what I've gathered
        self.load()
        self.buildOutput()
        return

    def load(self) -> None:
        if not os.path.exists(self.filename):
            self.logger.msg(f'failed to load <{self.filename}>', error='FATAL')
            sys.exit()
        else:
            self.logger.msg(f'image loaded <{self.filename}> (output dimensions: {self.width},{self.height})')
        return None
    
    def buildOutput(self) -> bool:
        self.logger.msg('ascii render', render=self.width)
        self.image = Image.open(self.filename)
        tmpImage = self.image.resize((self.width, self.height))
        self.colorMap = [[0] * self.width for i in range(self.height)]
        print('- ' * self.width, '+')

        for y in range(self.height):
            for x in range(self.width):
                self.colorMap[y][x] = (tmpImage.getpixel((x,y)))
                localize = self.RgbToString(self.colorMap[y][x], symbol=True)
                print(Style.BRIGHT, end='')
                print(f'{localize[0]}{localize[1]}{Style.RESET_ALL}', end='')
            print()

        print('- ' * self.width, '+')
        return None

class RgbToString:
    def __init__(self) -> None:
        self.colorBank: Dict[str, List] = {
            Fore.BLACK :   [0, 0, 0],
            Fore.RED :     [1, 0, 0],
            Fore.GREEN :   [0, 1, 0],
            Fore.YELLOW :  [1, 1, 0],
            Fore.BLUE :    [0, 0, 1],
            Fore.WHITE :   [1, 1, 1], #supported (not included) MAGENTA, CYAN
            Fore.MAGENTA : [1, 0, 1],
            Fore.CYAN :    [0, 1, 1],
        }

        self.asciiTable: Dict[int, str] = OrderedDict()
        self.asciiTable[0]   = Style.DIM    + ' .'
        self.asciiTable[20]  = Style.DIM    + '.,'
        self.asciiTable[40]  = Style.BRIGHT    + '.;'
        self.asciiTable[80]  = Style.BRIGHT + ';;'
        self.asciiTable[120] = Style.BRIGHT + 'Oo'
        self.asciiTable[160] = Style.BRIGHT + '@o'
        self.asciiTable[200] = Style.BRIGHT + '@@'
        self.asciiTable[225] = Style.BRIGHT + '#@'
        self.asciiTable[250] = Style.BRIGHT + '##'

        self.Threshold: int = 100
        self.grayThreshold: int = 10

    def __call__(self, RGB, symbol: bool = False) -> str:
        RGB: Tuple = RGB
        rgbMAP: List = [int(x > self.Threshold) for x in RGB]

        if ( (abs(RGB[0] - RGB[1]) <= self.grayThreshold) \
         and (abs(RGB[0] - RGB[2]) <= self.grayThreshold)):
            colorName = Fore.WHITE
            #brightness = int(sum(RGB) / len(RGB))
            brightness = (0.2126 * RGB[0] + 0.7152 * RGB[1] + 0.0722 * RGB[2]) #luminance 
            __ascii = self.brightnessToAsciiSymbol(brightness)
            return (colorName, __ascii) if (symbol) else (colorName)

        for colorName, colorValues in self.colorBank.items():
            if(rgbMAP == colorValues):
                brightness = int(sum(RGB) / len(RGB))
                __ascii = self.brightnessToAsciiSymbol(brightness)
                return (colorName, __ascii) if (symbol) else (colorName)

        return (Fore.WHITE, '??') if (symbol) else (Fore.WHITE)

    def brightnessToAsciiSymbol(self, b: int) -> str:
        keys: List = list(self.asciiTable.keys())
        if(b <= keys[1]):
            return self.asciiTable[keys[0]]
        if(b >= keys[-2]):
            return self.asciiTable[keys[-1]]
        for i in range(len(keys)):
            if(b >= keys[i] and b <= keys[i+1]):
                return self.asciiTable[keys[i]]
        
class Logger:
    def __init__(self, objectName: str) -> None:
        self.objectName = objectName
        self.msg('module loaded')
        return
    
    def msg(self, message: str, error: str = '', render: bool = False) -> bool:
        name = self.objectName
        color = Fore.GREEN
        if render:
            color = f'{Fore.CYAN}@@'
            name = message
            message = ''
        if error != '':
            error = f'{Fore.RED}[{error}_ERROR] {Style.RESET_ALL}'
        print(f'{color}[{name}]: {error}{Style.RESET_ALL}{message}')
        return True