#!/bin/zsh

export PYTHONPATH="~/Desktop/Repos/NCUT/Computer-Networking/lab3-socket:$PYTHONPATH"

# Run server code
python server/run.py &

sleep 1

# Run client code
num_clients=2

for ((i=0; i<num_clients; i++))
do
    python client/run.py &
done
