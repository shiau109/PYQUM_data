from abc import ABCMeta, abstractmethod
class QPUBenchmark( metaclass=ABCMeta ):

    @abstractmethod
    def benchmark( self ):
        pass

class ThermalExcitation( QPUBenchmark ):
    def __init__(self):
        pass

    def benchmark( self ):
        pass
        

class ReadoutFidelity( QPUBenchmark ):
    def __init__(self):
        pass

    def benchmark( self ):
        pass

class FluxDepResonator( QPUBenchmark ):
    def __init__(self):
        pass

    def benchmark( self ):
        pass

class DressedResonator(  ):
    def __init__( self ):
        pass
    def import_data( self ):
        pass
    def get_report( self ):
        from find_dress.ZY_method import PowerDepend
        PowerDepend()


if __name__ == '__main__':
    from data_praser import PyqumPraser
    test_files = [ "F_Response.pyqum(PD)" ]
    p_praser = PyqumPraser()
    for fn in test_files:
        print(f"Testing {fn}")
        myexp = p_praser.import_data(f"{fn}" )
        print(myexp.dimension)
        print(myexp.shape)
        print(myexp.settings)
    # my_ana = DressedResonator()
    # my_ana.get_report()



