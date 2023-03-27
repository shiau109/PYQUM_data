from abc import ABC, abstractmethod


class Extractor(ABC):
    @abstractmethod
    def __init__():
        pass
    @abstractmethod
    def import_data( self, data ):
        pass
    @abstractmethod
    def extract():
        pass
class ResonatorExtractor(Extractor,ABC):
    def __init__( self ):
        print(f"Create {self.__class__} object.")
    @abstractmethod
    def import_data():
        pass
    @abstractmethod
    def extract( self, guess=None, fixed=None ):
        pass


class TLSLossExtractor(Extractor):
    def __init__( self ):
        print(f"Create {self.__class__} object.")



