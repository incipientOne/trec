import subprocess
import os.path


# takes file paths for qrel and run files as strings,
# returns map, p_10, p_20 as list of floats.
def trec_wrapper(qrel_file_path, run_file_path):
    # trec_eval program is stored in the same directory as the wrapper
    trec_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'trec_eval')

    results = subprocess.check_output([trec_path,
                                       '-m', 'map',  # tell trec_eval to calculate map
                                       '-m', 'P.10,20',  # and P_10, P_20
                                       qrel_file_path,
                                       run_file_path])
    # results returned in human readable format, for example:
    # map                   	all	0.1764
    # P_10                  	all	0.3469
    # P_20                  	all	0.3367
    # so we split by whitespace.
    result_array = results.split()

    # then return the 3rd, 6th and 9th elements as floats.
    return float(result_array[2]), float(result_array[5]), float(result_array[8])

# some code to test the above.

#this_files_path = os.path.dirname(os.path.abspath(__file__))

#test_qrel = os.path.join(this_files_path, 'qrels/aq.trec2005.qrels.txt')
#test_run = os.path.join(this_files_path, 'aq.trec.bm25.0.50.res.txt')
#result = trec_wrapper(test_qrel, test_run)

#print result
