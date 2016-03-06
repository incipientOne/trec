import os
import sys
from path_names import TRACK_PATH_SOURCE, USER_RUN_PATH_SOURCE, TEMP_RESULTS_FILE

# Get all of the track topic names
def listdir_track_topics(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f


# Get all of the queries for a particular track topic
def listdir_track_query(path):
    for f in os.listdir(path):
        if not f.startswith('.') and f.endswith(".qrels"):
            yield f


# Get all of the user run names for a particular track
def listdir_user_runs(path):
    for f in os.listdir(path):
        if not f.startswith('.') and f.startswith("input."):
            yield f


# Function to construct the track-query argument of the trec_eval exe
def construct_tq_path(track_name, query_file):
    return TRACK_PATH_SOURCE + track_name + "/" + query_file


# Function to construct the user run argument of the trec_eval exe
def construct_run_path(track_name, run_name):
    return USER_RUN_PATH_SOURCE + track_name + "/" + run_name


# Performs a run on the input parameters and saves results to a text file tempResults.txt
def perform_user_run(track_name, query_name, run_name):
    # Run given input track and save output results to tempResults.txt file
    os.popen("./trec_eval " + construct_tq_path(track_name, query_name) + " " + construct_run_path(track_name, run_name) + " > " + TEMP_RESULTS_FILE)
    return


# This performs all valid runs for all of the tracks
# Possibly make update track methods
def populate_all_tracks():
	track_path = TRACK_PATH_SOURCE
  	user_run_path = USER_RUN_PATH_SOURCE
	results_file = TEMP_RESULTS_FILE
		
	# Dictionary with following key:value pairings
	# 'track_name' : [string, list, of, run, names]
	track_run_dict = {}
	
	# Dictionary of all results to be returned
	# 'track' : track_run_dict
	results_dict = {}
	
	run_results = {}
	user_runs = {}
	query_results = {}
	
	# This is a mess but structured as follows
	# { track :  { query : { run_name : { P10 : string-value , P20: string-value, map: string-value } } } } 
	rtn_results = {}
	
	# Get a list of all track names
  	track_topic_list = listdir_track_topics(track_path)
  	
  	for track in track_topic_list:
  		# Attempt to find runs for a particular track and store in dictionary
  		try:
			temp_run_list = listdir_user_runs(user_run_path + track)
			dic_list = []
			for run in temp_run_list:
				dic_list.append(run)
			track_run_dict[track] = dic_list
		# No runs found then ignore
		except:
			pass


	for key in track_run_dict.keys():
		
		for query in listdir_track_query(track_path + key):
			
			for run in track_run_dict[key]:
				perform_user_run(key, query, run)
				run_results = parse_results(results_file)	
				user_runs[run] = run_results
	
			query_results[query] = user_runs
		
		rtn_results[key] =  query_results

	return rtn_results


# Perform all runs for an input topic name
# Example : (topic = robust) will perform all robust runs
def populate_track(topic):
	track_path = TRACK_PATH_SOURCE
  	user_run_path = USER_RUN_PATH_SOURCE
	results_file = TEMP_RESULTS_FILE
		
	
	user_dict = {}
	
	# Again a bit of a mess but structured as follows
	# { query : { run_name : { P10 : string-value , P20: string-value, map: string-value } } }
	results_dict = {}
	
	# Try and find runs of the input topic name
	# then perform the 
	try:
		temp_run_list = listdir_user_runs(user_run_path + topic)
		for query in listdir_track_query(track_path + topic):
			
			for run in temp_run_list:
				perform_user_run(topic, query, run)
				user_dict[run] = parse_results(results_file)
			
			results_dict[query] = user_dict
	#No runs found then ignore
	except:
		pass
		
	return results_dict


# Returns a dictionary of required results map, p10, p20
# Parses through a text results file to obtain the results
def parse_results(filename):
	
	score_dict = {}
	all_score_dict = {}

	r_file = open(filename, 'rU')
		
	for line in r_file:
		line = line[:-1].split()
		all_score_dict[line[0]] = line[2]

	score_dict['map'] = all_score_dict['map']
	score_dict['P_10'] = all_score_dict['P_10']
	score_dict['P_20'] = all_score_dict['P_20']
	
	return score_dict  


def main():
	

  user = populate_all_tracks()  
  print user
  
  
if __name__ == "__main__":
  main()