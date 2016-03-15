import subprocess
import os.path
from trec_eval_project.settings import BASE_DIR


# takes file paths for qrel and run files as strings,
# returns map, p_10, p_20 as list of floats.
def trec_wrapper(qrel_file_path, run_file_path):
    
    # trec_eval program is stored in the same directory as the wrapper
    trec_path = os.path.join(BASE_DIR, 'trec_eval/', 'trec_eval')

    results = subprocess.check_output([trec_path, qrel_file_path, run_file_path])
    
    """
    out = []
    
    for i in results.split():
    	out = out + [i]
    	if len(out) % 3 == 0:
    		print out
    		out = []
    """
    
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

    # then return the 3rd, 6th and 9th elements as floats.
    # Return order: 
    # map 
    # recall0.0
    # p5 - p10 - p15 - p20 - p30 - p100 - p200 - p500 - p1000
    return float(result_array[2]), float(result_array[5]), float(result_array[8]), float(result_array[11]), float(result_array[14]), float(result_array[17]) ,float(result_array[20]), float(result_array[23]), float(result_array[26]), float(result_array[29]), float(result_array[32]), float(result_array[35]), float(result_array[38]), float(result_array[41]), float(result_array[44]), float(result_array[47]), float(result_array[50]), float(result_array[53]), float(result_array[56]), float(result_array[59]), float(result_array[62])

# some code to test the above.

#test_qrel = os.path.join(BASE_DIR, 'pop script data','qrels', 'aq.trec2005.qrels.txt')
#test_run = os.path.join(BASE_DIR, 'pop script data', 'runs', 'aq.trec.bm25.0.50.res.txt')
#result = trec_wrapper(test_qrel, test_run)

#print result
