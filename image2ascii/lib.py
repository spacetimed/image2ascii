import sys
import os.path

from collections import OrderedDict
from colorama import Fore, Back, Style
from PIL import Image, ImageEnhance

from typing import List
from typing import Any
from typing import Tuple
from typing import Dict

SETTINGS: Dict[str, int] = {

    'default_width' : 10,
    'default_height' : 10,
    'show_black' : True,
    'output_file' : 'output.txt',

}

class Create:
    def __init__(self, filename: str, width: int, height: int, greySave: bool = False, colorSave: bool = False) -> None:

        self.logger = Logger(__name__)
        self.RgbToString = RgbToString()
        self.filename = filename
        self.width = width or SETTINGS['default_width']
        self.height = height or SETTINGS['default_height']
        self.colorMap: List[List[int]] = [[]]
        self.image: Any = None
        self.saveToFile = (greySave or colorSave)
        self.greySave = greySave
        self.colorSave = colorSave
        self.tmpFile: Any = None
        self.toWrite: str = ''
        self.outputFileName = SETTINGS['output_file']

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
        self.logger.msg('result', render=self.width)
        self.image = Image.open(self.filename)
        enhancer = ImageEnhance.Contrast(self.image)
        tmpImage = enhancer.enhance(1.5)
        tmpImage = tmpImage.resize((self.width, self.height))
        tmpImage.save('ok.png')
        self.colorMap = [[0] * self.width] * self.height

        if self.saveToFile:
            self.tmpFile = open(self.outputFileName, 'w')
            self.toWrite = ''

        print('- ' * self.width, '+')
        for y in range(self.height):
            for x in range(self.width):
                self.colorMap[y][x] = (tmpImage.getpixel((x,y)))
                localize = self.RgbToString(self.colorMap[y][x], symbol=True)
                print(Style.BRIGHT, end='')
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

        self.asciiTable[0]   = [Style.DIM,    ' .']
        self.asciiTable[20]  = [Style.DIM,    '.,']
        self.asciiTable[40]  = [Style.NORMAL, '.;']
        self.asciiTable[80]  = [Style.BRIGHT, ';;']
        self.asciiTable[120] = [Style.BRIGHT, 'Oo']
        self.asciiTable[160] = [Style.BRIGHT, '@o']
        self.asciiTable[200] = [Style.BRIGHT, '@@']
        self.asciiTable[225] = [Style.BRIGHT, '#@']
        self.asciiTable[250] = [Style.BRIGHT, '##']

        if not SETTINGS['show_black']:
            self.asciiTable[0][1] = '  '

        self.Threshold: int = 100
        self.grayThreshold: int = 10

    def __call__(self, RGB_init, symbol: bool = False) -> str:
        RGB: Tuple = (RGB_init) if (len(RGB_init) == 3) else (( RGB_init[0], RGB_init[1], RGB_init[2] ))
        rgbMAP: List = [int(x > self.Threshold) for x in RGB]
        brightness = (0.2126 * RGB[0] + 0.7152 * RGB[1] + 0.0722 * RGB[2]) #Relative Luminance Formula (from wiki) 

        if ( (abs(RGB[0] - RGB[1]) <= self.grayThreshold) \
         and (abs(RGB[0] - RGB[2]) <= self.grayThreshold) ):
            colorName = Fore.WHITE
            __asciiList: List = self.brightnessToAsciiSymbol(brightness)
            __ascii = __asciiList[1]
            colorName += __asciiList[0]
            return (colorName, __ascii) if (symbol) else (colorName)

        for colorName, colorValues in self.colorBank.items():
            if(rgbMAP == colorValues):
                __asciiList: List = self.brightnessToAsciiSymbol(brightness)
                __ascii = __asciiList[1]
                colorName += __asciiList[0]
                return (colorName, __ascii) if (symbol) else (colorName)

        return (Fore.WHITE, '??') if (symbol) else (Fore.WHITE) #could not find suitable color

    def brightnessToAsciiSymbol(self, b: int) -> str:
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
        self.objectName = objectName
        self.msg('module loaded')
        return
    
    def msg(self, message: str, error: str = '', render: bool = False) -> bool:
        name: str = self.objectName
        color: Any = Fore.GREEN
        if render:
            color = f'\n{Fore.CYAN}{Style.BRIGHT} @'
            name = message
            message = ''
        if error != '':
            error = f'{Fore.RED}[{error}_ERROR] {Style.RESET_ALL}'
        print(f'{color}[{name}]: {error}{Style.RESET_ALL}{message}')
        return True