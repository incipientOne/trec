import subprocess
import os.path
from trec_eval_project.settings import BASE_DIR


# takes file paths for qrel and run files as strings,
# returns map, p_10, p_20 as list of floats.
def trec_wrapper(qrel_file_path, run_file_path):
    
    # trec_eval program is stored in the same directory as the wrapper
    trec_path = os.path.join(BASE_DIR, 'trec_eval/', 'trec_eval')
    
    # This fixes pop script but someone should look into properly
    qrel_file_path = 'static' + qrel_file_path
    run_file_path = 'static' + run_file_path
    
    results = subprocess.check_output([trec_path, qrel_file_path, run_file_path])
    
    results = subprocess.check_output([trec_path,
                                       '-m', 'map',  # tell trec_eval to calculate map
                                       '-m', 'P.5,10,15,20,30,100,200,500,1000',  # and P_10, P_20
                                       '-m', 'iprec_at_recall.0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1',
                                       qrel_file_path,
                                       run_file_path])
    # results returned in human readable format, for example:
    # map                   	all	0.1764
    # P_10                  	all	0.3469
    # P_20                  	all	0.3367
    # so we split by whitespace.
    result_array = results.split()
    #print result_array

    # then return the numeric elements as floats.
    # Return order: 
    # map 
    # recall0.0 - recall0.1 - recall0.2 - recall0.3 - recall0.4 - recall0.5 - recall0.6 - recall0.7 - recall0.8 - recall0.9 - recall1.0
    # p5 - p10 - p15 - p20 - p30 - p100 - p200 - p500 - p1000
    mapVal = float(result_array[2])
    pMap = {}
    rMap = {}
    i = 5
    while i < len(result_array):
        val = float(result_array[i])
        name = result_array[i-2]
        if name[0] == "i":
            r_num = float(name[16:])
            rMap[r_num] = val
        else:
            p_num = int(name[2:])
            pMap[p_num] = val
        i += 3
    return mapVal, rMap, pMap
