import image2ascii.boot
import image2ascii.lib
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', required=True, type=str)
    parser.add_argument('-W', '--width', type=int)
    parser.add_argument('-H', '--height', type=int)
    parser.add_argument('-greysave', '--greysave', action='store_true')
    parser.add_argument('-colorsave', '--colorsave', action='store_true')
    args = parser.parse_args()

    image2ascii.boot.BootScreen()
    image2ascii.lib.Create( filename = args.filename, \
                            width = args.width, \
                            height = args.height, \
                            greySave = args.greysave, \
                            colorSave = args.colorsave )

if __name__ == '__main__':
    main()
    print()
