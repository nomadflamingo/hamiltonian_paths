# Algorithm description
This algorithm uses python in-built priority queues to insert and get elemenets depending on their priority (i.e. price and duration)

The overall process looks like this:
1. Parse csv file and add all edges to the priority queue
2. Pick a path (for first time, edge) that has the highest priority
3. Iterate through all its end station connections
4. For each connection, add updated paths to the queue
5. Repeat step 2 until we don't find a path that covers all stations
