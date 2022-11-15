# This script opens a database and queries a variable for all time slices. The user specifies
# the database and variable, and the time, maximum value, and coordinate where the maximum value
# was found is printed to a file.
#
# Run this with
#
# Serial: visit -cli -nowin -s GetMax.py -database "..." -variable "..." -output "..."
# Parallel: visit -nn <num_nodes> -np <procs_per_node> -cli -nowin -s GetMax.py  -database "..." -variable "..." -output "..."
#
# If using slurm, one can allocate with
#
# > salloc --account=nnXXXXk --time=00:30:00 --nodes=4 --qos=devel 
# 

import argparse

FileFormat = "{: <20} {: <20} {: <20} {: <20} {: <20}\n"

# # Input argument parser.
parser = argparse.ArgumentParser()
parser.add_argument('-database',    type=str, help="Absolute path to database. Use e.g. with 'plt/simulation2d.step*.hdf5 database' if opening multiple files", required=True)
parser.add_argument('-variable',    type=str, help="Which variable to query", required=True)
parser.add_argument('-output_file', type=str, help="Output file", default="output.dat", required=False)
parser.add_argument('-every_nth', type=int, help="Every nth step", default=1, required=False)

args,unknown = parser.parse_known_args()

# Open output file and write header
fout = open(args.output_file, 'w')
fout.write("# DB = " + args.database + "\n")
fout.write("# Variable = " + args.variable + "\n")

header = ["# Time", "Max val", "x", "y", "z"]
fout.write(FileFormat.format(*header))
fout.close()

# Open database.
OpenDatabase(args.database)

# Pseudo-color plot of variable
AddPlot("Pseudocolor", args.variable)
DrawPlots()

for i in range(0,TimeSliderGetNStates(), args.every_nth):
    SetTimeSliderState(i)

    curTime  = GetQueryOutputValue(Query("Time"))
    queryMax = Query("Max")
    curMax   = GetQueryOutputObject()['max']
    maxCoord = GetQueryOutputObject()['max_coord'] + (0.,)

    data = [curTime, curMax, maxCoord[0], maxCoord[1], maxCoord[2]]

    # Opening/closing because file buffers are not always immediately updated on
    # the clusters we use. 
    fout = open(args.output_file, 'a')
    fout.write(FileFormat.format(*data))
    fout.close()

# Close database
DeleteAllPlots()
CloseDatabase(args.database)

exit()
