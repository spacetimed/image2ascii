from io import TextIOWrapper
import sys
import os.path

from collections import OrderedDict
from colorama import Fore, Back, Style
from PIL import Image, ImageEnhance

from typing import List, Sized
from typing import Any
from typing import Tuple
from typing import Dict
from typing import Type
from typing import Optional

SETTINGS: Dict[str, int] = {

    'default_width' : 10,
    'default_height' : 10,
    'show_black' : True,
    'output_file' : 'output.txt',

}

class Create:
    def __init__(self, filename: str, width: int, height: int, greySave: bool = False, colorSave: bool = False) -> None:

        self.logger: Type[Logger] = Logger(__name__)
        self.RgbToString: Type[RgbToString] = RgbToString()
        self.filename: str = filename
        self.width: int = width or SETTINGS['default_width']
        self.height: int = height or SETTINGS['default_height']
        self.colorMap: List[List[int]] = [[]]
        self.image: Image = None
        self.saveToFile: bool = (greySave or colorSave)
        self.greySave: bool = greySave
        self.colorSave: bool = colorSave
        self.tmpFile: TextIOWrapper = None
        self.toWrite: str = ''
        self.outputFileName: str = SETTINGS['output_file']

        self.load()
        self.render()

        return

    def load(self) -> None:
        if not os.path.exists(self.filename):
            self.logger.msg(f'failed to load <{self.filename}>', error='FATAL')
            sys.exit()
        return None
    
    def render(self) -> bool:
        self.logger.msg('result', render=self.width)
        self.image = Image.open(self.filename)
        if(self.width != SETTINGS['default_width'] and self.height == SETTINGS['default_width']):
            realW, realH = self.image.size
            factor = self.width / realW
            self.height = int( realH * factor )
        self.logger.msg(f'image loaded <{self.filename}> (output dimensions: {self.width},{self.height})')
        enhancer: Any = ImageEnhance.Contrast(self.image)
        tmpImage: Image = enhancer.enhance(1.4)
        tmpImage: Image = tmpImage.resize((self.width, self.height))
        self.colorMap = [[0] * self.width] * self.height

        if self.saveToFile:
            self.tmpFile = open(self.outputFileName, 'w')
            self.toWrite = ''

        print('- ' * self.width, '+')

        for y in range(self.height):
            for x in range(self.width):
                self.colorMap[y][x] = (tmpImage.getpixel((x,y)))
                localize: RgbToString = self.RgbToString(self.colorMap[y][x], symbol=True)
                print(f'{localize[0]}{localize[1]}{Style.RESET_ALL}', end='')
                if self.saveToFile:
                    if self.colorSave:
                        self.toWrite += localize[0] + localize[1]
                    elif self.greySave:
                        self.toWrite += localize[1]
            print()
            if self.saveToFile:
                self.toWrite += '\n'

        print('- ' * self.width, '+')

        if self.saveToFile:
            self.tmpFile.write(self.toWrite)
            self.tmpFile.close()
            self.logger.msg(f'output successfully saved to <{self.outputFileName}>.')

        return None

class RgbToString:
    def __init__(self) -> None:

        self.colorBank: Dict[str, List] = {
            Fore.BLACK :   [0, 0, 0],
            Fore.RED :     [1, 0, 0],
            Fore.GREEN :   [0, 1, 0],
            Fore.YELLOW :  [1, 1, 0],
            Fore.BLUE :    [0, 0, 1],
            Fore.WHITE :   [1, 1, 1], 
            Fore.MAGENTA : [1, 0, 1],
            Fore.CYAN :    [0, 1, 1],
        }

        self.asciiTable: Dict[int, List] = OrderedDict()
        self.asciiTable[0]   =  [Style.DIM,    ' .']
        self.asciiTable[20]  =  [Style.DIM,    ' ,']
        self.asciiTable[40]  =  [Style.DIM,    '.,']
        self.asciiTable[60]  =  [Style.DIM,    '.;']
        self.asciiTable[80]  =  [Style.NORMAL, 'q;']
        self.asciiTable[100] =  [Style.NORMAL, '3;']
        self.asciiTable[110] =  [Style.NORMAL, 'T;']
        self.asciiTable[120] =  [Style.NORMAL, 'Pl']
        self.asciiTable[140] =  [Style.NORMAL, 'P9']
        self.asciiTable[160] =  [Style.NORMAL, '$j']
        self.asciiTable[180] =  [Style.BRIGHT, '$i']
        self.asciiTable[200] =  [Style.BRIGHT, '#$']
        self.asciiTable[220] =  [Style.BRIGHT, '@#']
        self.asciiTable[240] =  [Style.BRIGHT, '@@']

        if not SETTINGS['show_black']:
            self.asciiTable[0][1] = '  '

        self.Threshold: int = 100
        self.grayThreshold: int = 10

    def __call__(self, RGB_init: Tuple, symbol: bool = False) -> str:
        RGB: Tuple = (RGB_init) if (len(RGB_init) == 3) else (( RGB_init[0], RGB_init[1], RGB_init[2] ))
        rgbMAP: List = [int(x > self.Threshold) for x in RGB]
        brightness: float = (0.2126 * RGB[0] + 0.7152 * RGB[1] + 0.0722 * RGB[2]) #Relative Luminance Formula (from wiki) 

        #if grayscale
        if ( (abs(RGB[0] - RGB[1]) <= self.grayThreshold) \
         and (abs(RGB[0] - RGB[2]) <= self.grayThreshold) ):
            colorName: str = Fore.WHITE
            __asciiList: List = self.brightnessToAsciiSymbol(brightness)
            __ascii: str = __asciiList[1]
            colorName += __asciiList[0]
            return (colorName, __ascii) if (symbol) else (colorName)

        #if color
        if(rgbMAP == [0,0,0]):
            #print('_==>', end='')
            rgbMAP[RGB.index(max(RGB))] = True

        for colorName, colorValues in self.colorBank.items():
            if(rgbMAP == colorValues):
                __asciiList: List = self.brightnessToAsciiSymbol(brightness)
                __ascii: str = __asciiList[1]
                colorName += __asciiList[0]
                return (colorName, __ascii) if (symbol) else (colorName)

        #if unrecognized rgb (todo: use most recent previous color instead of WHITE)
        return (Fore.WHITE, '??') if (symbol) else (Fore.WHITE)

    def brightnessToAsciiSymbol(self, b: int) -> Optional[str]:
        keys: List = list(self.asciiTable.keys())

        if(b <= keys[1]):
            return self.asciiTable[keys[0]][0], self.asciiTable[keys[0]][1]
        if(b >= keys[-2]):
            return self.asciiTable[keys[-1]][0], self.asciiTable[keys[-1]][1]
        for i in range(len(keys)):
            if(b >= keys[i] and b <= keys[i+1]):
                return self.asciiTable[keys[i]][0], self.asciiTable[keys[i]][1]
            
        return None
        
class Logger:
    def __init__(self, objectName: str) -> None:
        self.objectName: str = objectName
        self.msg('module loaded')
        return
    
    def msg(self, message: str, error: str = '', render: bool = False) -> None:
        name: str = self.objectName
        color: Any = Fore.GREEN
        if render:
            color = f'\n{Fore.CYAN}{Style.BRIGHT} @'
            name = message
            message = ''
        if error != '':
            error = f'{Fore.RED}[{error}_ERROR] {Style.RESET_ALL}'
        print(f'{color}[{name}]: {error}{Style.RESET_ALL}{message}')
        return