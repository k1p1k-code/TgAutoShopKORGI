from progress.bar import IncrementalBar
import os
from importlib import __import__
from loader import dp
import sys

class load():
        def __init__(self):
                self.plagins=list()
                self.plagins_object=dict()
                for name in os.listdir(os.path.join('plugins')):
                        if name[-2:] == 'py':
                                self.plagins.append(name)

                bar = IncrementalBar('Loading plugins...', max=len(self.plagins))
                for name in self.plagins:
                        plugin=name[:-3]
                        imported = __import__(f"plugins.{plugin}")
                        self.plagins_object[name]=(getattr(imported, plugin)).Main
                        bar.next()      

                        
                bar.finish()
                
