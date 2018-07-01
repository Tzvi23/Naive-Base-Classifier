# Author: Tzvi Puchinsky
from GUI import GUI
from ModelBuilder import model_builder
from StructureBuilder import structure_builder
from Tkinter import *

root = Tk()
GUI(root, structure_builder(), model_builder())