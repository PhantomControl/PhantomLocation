from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS
from opencage.geocoder import OpenCageGeocode
from pprint import pprint
import pyfiglet
from colorama import init, Fore, Back, Style
import colorama

colorama.init(autoreset=True)
print(Fore.MAGENTA + "Please enter image name to begin.")
simage = input('')

def mainMenu():
    banner = pyfiglet.figlet_format("PhantomLocation", font="rectangles")
    print(Fore.MAGENTA + banner)
    print("+-+" * 22)
    print(Fore.MAGENTA + "[1] Extract Exif data")
    print(Fore.MAGENTA + "[2] Obtain location data")
    print(Fore.MAGENTA + "[3] Exit")
    while True:
        try:
            selection = int(input(Fore.MAGENTA + "Enter choice:>> "))
            if selection == 99:
                crt()
                break
                #Debug command for checking selected image
            elif selection == 1:
                edata()
                break
            elif selection == 2:
                ldata()
                break
            elif selection == 3:
                break
            else:
                print("Invalid choice. Enter 1-3")
                mainMenu()
        except ValueError:
            print(Fore.RED + "Invalid choice. Enter 1-3")
    exit()

def crt():
    print(simage)
    anykey = input(Fore.MAGENTA + "Enter anything to return to the main menu")
    mainMenu()

def sphoto():
    print(Fore.MAGENTA + "Select Photo")
    simage = input()
    mainMenu()

def edata():
    print(Fore.RED + "Extracting Exif Data")
    print(exif)
    print(labeled)
    print(get_coordinates(geotags))

    anykey = input(Fore.MAGENTA + "Enter anything to return to the main menu")
    mainMenu()


def ldata():
    print(Fore.RED + "Obtaining Location Data")

    key = 'fe27ab7fb62a4cffaeaee666a642d749'
    geocoder = OpenCageGeocode(key)

    print(Fore.MAGENTA + "Input latitude")

    lat = eval(input())

    print(Fore.MAGENTA + "Input longitude")

    lon = eval(input())

    print(Fore.RED + "*Obtaining Location Data*")

    results = geocoder.reverse_geocode(lat, lon)
    pprint(results)

    anykey = input(Fore.MAGENTA + "Enter anything to return to the main menu")
    mainMenu()





def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()


exif = get_exif(simage)
#print(exif)


def get_labeled_exif(exif):
    labeled = {}
    for (key, val) in exif.items():
        labeled[TAGS.get(key)] = val

    return labeled


exif = get_exif(simage)
labeled = get_labeled_exif(exif)
#print(labeled)


def get_geotagging(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging


exif = get_exif(simage)
geotags = get_geotagging(exif)
#print(geotags)


def get_decimal_from_dms(dms, ref):
    degrees = dms[0][0] / dms[0][1]
    minutes = dms[1][0] / dms[1][1] / 60.0
    seconds = dms[2][0] / dms[2][1] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)


def get_coordinates(geotags):
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])

    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return lat, lon


exif = get_exif(simage)
geotags = get_geotagging(exif)
#print(get_coordinates(geotags))

mainMenu()
