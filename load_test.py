import expdata as expdata
from data_praser import PyqumPraser

test_files = [ "F_Response.pyqum", "CW_Sweep.pyqum", "Single_Qubit.pyqum(17)", "Single_Qubit.pyqum(19)" ]
p_praser = PyqumPraser()
for fn in test_files:
    print(f"Testing {fn}")
    myexp = p_praser.import_data(f"test_file/{fn}" )
    print(myexp.exp_vars)




# for container in pqdata.datacontainer.values() :
#     print(f"{container}/n")

# print( data_obj.datacontainer.items())


