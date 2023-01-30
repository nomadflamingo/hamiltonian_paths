# Task definition
Train schedule between several stations is given in the format “train number; departure station; arrival station; cost; departure time; arrival time” (it is guaranteed that there are no crossings for more than a day) . It is necessary to get the “best” options (several, if possible) of travel between all stations so that you visit each station 1 time. Requests for the best options:
* Best by price
* Best by time


# My solution description
The algorithm uses priority queues to add and remove items depending on their priority (price or duration)

The algorithm looks like this:
1. Parse the csv file and adding routes to the priority queue
2. Select the route with the highest priority (lowest price or fastest time)
3. Iterate over all connections of the final station of the route
4. For each connection, add the updated route to the queue
5. Repeat steps 2-4 until you find a route that passes through all stations
6. Take all the following routes in the queue, if their priority is the same as that of the found route (because all the remaining ones will be more expensive or slower)
7. Reconstruct the found routes along the vertices (the route itself is not stored in the queue to save memory)
