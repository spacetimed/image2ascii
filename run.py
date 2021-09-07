import image2ascii.boot
import image2ascii.lib
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--filename', required=True, type=str)
parser.add_argument('-W', '--width', type=int)
parser.add_argument('-H', '--height', type=int)
args = parser.parse_args()

image2ascii.boot.BootScreen()
image2ascii.lib.Create( filename = args.filename, \
                        width = args.width, \
                        height = args.height )

print()