#ImportAPCSE

from Aviation import *
from AircraftDictionaries import *


main_dir = os.getcwd()
embr_dir = main_dir + '\Embraer_Classes'
engine_dir = main_dir + '\Engine'
perf_dir = main_dir + '.\Performance_Classes'



'''
os.chdir(embr_dir)
import ImportEmbraer as Embraer
'''
#   Different Aircraft components will be uploaded and handled within the "Aircraft" Class because otherwise the different 
#   parts will be impossible to parse. i.e. : how can we know if its a piper vs. an Embraer wing???

os.chdir(engine_dir)
from Engine import *

os.chdir(perf_dir)
from AircraftConventional import *
from Control import *
from AircraftElectric import *
#MUST NOT DELETE THIS ONE, STUFF WILL STOP WORKING IF DELETED
os.chdir(main_dir)