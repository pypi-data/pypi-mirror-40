# -*- coding: utf-8 -*-

import pandas as pd
import io
import os
import numpy as np
import datetime as dt
import sys
import pytz
import math

import argparse

from time import sleep

parser = argparse.ArgumentParser()
#if __name__ == '__main__':
parser.add_argument('--exec') # chunk simulation script
parser.add_argument('--first_station_row',
                    help='starting row number of stations table')
parser.add_argument('--last_station_row')
parser.add_argument('--pbs_string',default=' -l walltime=2:0:0')
parser.add_argument('--station_id',
                    help="process a specific station id")
parser.add_argument('--error_handling')
parser.add_argument('--subset_forcing',default='ini') 
                                        # this tells which yaml subset
                                        # to initialize with.
                                        # Most common options are
                                        # 'morning' and 'ini'.

# Tuntime is usually specified from the afternoon profile. You can also just
# specify the simulation length in seconds
parser.add_argument('--runtime',
                    help="set the runtime of the simulation in seconds, or get it from the daytime difference in the profile pairs 'from_profile_pair' (default)")
# delete folders of experiments before running them
parser.add_argument('--cleanup_output_directories',
                    default="False",
                    help="clean up output directories before executing the experiments")
parser.add_argument('--experiments', 
                    help="IDs of experiments, as a space-seperated list (default: 'BASE')")
parser.add_argument('--experiments_names', 
                    help="Alternative output names that are given to the experiments. By default, these are the same as --experiments") 
parser.add_argument('--split_by',
                    default=50,
                    type=int,
                    help="the maxmimum number of soundings that are contained in each output file of a station. -1 means unlimited. The default for array experiments is 50.")

parser.add_argument('--c4gl_path_lib',help="the path of the CLASS4GL program.")#,default='/user/data/gent/gvo000/gvo00090/D2D/software/CLASS/class4gl/lib')
parser.add_argument('--path_forcing',
                    help='directory of forcing data to initialize and constrain the ABL model simulations'
                   )
parser.add_argument('--path_experiments',
                    help='output directory in which the experiments as subdirectories are stored')#,default='/user/data/gent/gvo000/gvo00090/D2D/data/C4GL/')



#arguments only used for update_yaml.py
#parser.add_argument('--path_dataset') 
#parser.add_argument('--global_keys') 
args = parser.parse_args()

if args.c4gl_path_lib is not None:
    sys.path.insert(0, args.c4gl_path_lib)
from class4gl import class4gl_input, data_global,class4gl
from interface_multi import stations,stations_iterator, records_iterator,get_record_yaml,get_records
from class4gl import blh,class4gl_input


# this is a variant of global run in which the output of runs are still written
# out even when the run crashes.

# #only include the following timeseries in the model output
# timeseries_only = \
# ['Cm', 'Cs', 'G', 'H', 'L', 'LE', 'LEpot', 'LEref', 'LEsoil', 'LEveg', 'Lwin',
#  'Lwout', 'Q', 'RH_h', 'Rib', 'Swin', 'Swout', 'T2m', 'dq', 'dtheta',
#  'dthetav', 'du', 'dv', 'esat', 'gammaq', 'gammatheta', 'h', 'q', 'qsat',
#  'qsurf', 'ra', 'rs', 'theta', 'thetav', 'time', 'u', 'u2m', 'ustar', 'uw',
#  'v', 'v2m', 'vw', 'wq', 'wtheta', 'wthetae', 'wthetav', 'wthetae', 'zlcl']



# #SET = 'GLOBAL'
# SET = args.dataset

# path_forcingSET = args.path_forcing+'/'+SET+'/'

print("getting all stations from "+args.path_forcing)
# these are all the stations that are found in the input dataset
all_stations = stations(args.path_forcing,suffix=args.subset_forcing,refetch_stations=False)

print('defining all_stations_select')
# these are all the stations that are supposed to run by the whole batch (all
# chunks). We narrow it down according to the station(s) specified.
if args.station_id is not None:
    print("Selecting stations by --station_id")
    stations_iter = stations_iterator(all_stations)
    STNID,run_station = stations_iter.set_STNID(STNID=int(args.station_id))
    all_stations_select = pd.DataFrame([run_station])
else:
    print("Selecting stations from a row range in the table [--first_station_row,--last_station_row]")
    all_stations_select = pd.DataFrame(all_stations.table)
    if args.last_station_row is not None:
        all_stations_select = all_station_select.iloc[:(int(args.last_station)+1)]
    if args.first_station_row is not None:
        all_stations_select = all_station_select.iloc[int(args.first_station):]
print("station numbers included in the whole batch "+\
      "(all chunks):",list(all_stations_select.index))

print("getting all records of the whole batch")
all_records_morning_select = get_records(all_stations_select,\
                                         args.path_forcing,\
                                         subset=args.subset_forcing,\
                                         refetch_records=False,\
                                        )

print('splitting batch in --split_by='+str(args.split_by)+' jobs.')
totalchunks = 0
for istation,current_station in all_stations_select.iterrows():
    records_morning_station_select = all_records_morning_select.query('STNID == '+str(current_station.name))
    chunks_current_station = math.ceil(float(len(records_morning_station_select))/float(args.split_by))
    totalchunks +=chunks_current_station

print('total chunks of simulations (= size of array-job) per experiment: ' + str(totalchunks))

experiments = args.experiments.strip(' ').split(' ')
if args.experiments_names is not None:
    experiments_names = args.experiments_names.strip(' ').split(' ')
    if len(experiments_names) != len(experiments):
        raise ValueError('Lenght of --experiments_names is different from --experiments')
else:
    experiments_names = experiments

odir_exists = False

cleanup = (args.cleanup_output_directories == 'True')

if not cleanup:
    for expname in experiments_names:
        if os.path.exists(args.path_experiments+'/'+expname):
            print("Output directory already exists: "+args.path_experiments+'/'+expname+". ")
            odir_exists = True
if odir_exists:
    raise IOError("At least one of the output directories exists. Please use '--cleanup_output_directories True' to delete any output directory.")

for iexp,expname in enumerate(experiments_names):
    if cleanup:
        if os.path.exists(args.path_experiments+'/'+expname):
            print("Warning! Output directory '"+args.path_experiments+'/'+expname+"' exists! I'm removing it in 10 seconds!' Press ctrl-c to abort.")
            sleep(10)
            os.system("rm -R "+args.path_experiments+'/'+expname)

    # C4GLJOB_timestamp="+dt.datetime.now().isoformat()+",
    command = 'qsub '+args.pbs_string+' '+args.c4gl_path_lib+'/simulations/batch_simulations.pbs -t 0-'+\
                str(totalchunks-1)+" -v C4GLJOB_experiments="+str(experiments[iexp])+",C4GLJOB_experiments_names="+str(expname)
    # propagate arguments towards the job script
    for argkey in args.__dict__.keys():
        if ((argkey not in ['experiments','experiments_names','pbs_string','cleanup_output_directories']) and \
            # default values are specified in the simulation script, so
            # excluded here
            (args.__dict__[argkey] is not None)
           ):
                command +=',C4GLJOB_'+argkey+'='+str(args.__dict__[argkey])

    print('Submitting array job for experiment '+expname+': '+command)
    os.system(command)

    #os.system(command)
# elif sys.argv[1] == 'wsub':
#     
#     # with wsub
#     STNlist = list(df_stations.iterrows())
#     NUMSTNS = len(STNlist)
#     PROCS = NUMSTNS 
#     BATCHSIZE = 1 #math.ceil(np.float(NUMSTNS)/np.float(PROCS))
# 
#     os.system('wsub -batch /user/data/gent/gvo000/gvo00090/D2D/scripts/C4GL/global_run.pbs -t 0-'+str(PROCS-1))

