"""
This is the file for assignment 1 part 1 and 2 for FIT 2004.

Author: Lim Jun Yi
student_id: 32625510
Date: 2023/4/24
"""
from math import inf


class MinHeap:
    """
    This class is a Minimum Heap implementation for the Dijkstra's algorithm.
    Which contained basic operations such as serve and add for the heap array.
    Dijkstra uses the MinHeap to stores and load the discovered location.

    some function in this class are inspired from FIT 1008 and FIT 2004 PASS.

    Author: Lim Jun Yi
    student_id: 32625510
    Date: 2023/4/24
    """

    def __init__(self, size):
        """
        This is the initialisation method for MinHeap, take a size parameter and make an array of it's size+1 and also
        initialise the length of the array as 0, it will be used as the pointer to the end of the array.

        Input:
            size: an int representing the amount of locations.
        Time complexity:
            best/worst: O(|L|) where |L| is the number of locations.
        Space complexity:
            O(|L|) for space complexity.
            Aux: O(|L|), where it created an array for 'size+1' and an index map for 'size' and |L| is the number of locations.
        """
        self.length = 0
        self.my_array = [None] * (size + 1)
        self.index_map = [None] * size

    def rise(self, index):
        """
        This function rise the location stored in the MinHeap at index to the correct place.
        Rise compare time from source (location, key), by using the second item in the tuple as the key.

        This function is inspired from FIT1008 Week 12 lecture and modified on top of it to meet the required of this assignment.

        Input:
            index: an int value, representing the index of the element that need to be risen to the correct position.
        Time complexity:
            best: O(1), when the element being compared is greater or equal to its parent.
            worst: O(log|L|), when the element rises all the way to the root and |L| is the number of elements in minheap.
        Space complexity:
            O(1) for space complexity.
            Aux: O(1), no additional space needed.
        """
        while index > 1 and self.my_array[index][1] < self.my_array[index // 2][1]:
            self.swap(index, index // 2)
            self.index_swap(self.my_array[index][0], self.my_array[index // 2][0])
            index = index // 2

    def swap(self, x, y):
        """
        This function is used to swap the element during rise operation.

        Input:
            x: index of the element to be swapped
            y: index of the element to be swapped
        Time complexity:
            best/worst: O(1)
        Space complexity:
            O(1) for space complexity.
            Aux: O(1), no additional space needed.
        """
        self.my_array[x], self.my_array[y] = self.my_array[y], self.my_array[x]

    def index_swap(self, x, y):
        """
        This function is used to swap the index for the two items in the minheap, to keep track of their index in the minheap.

        Input:
            x: index of the element to be swapped
            y: index of the element to be swapped
        Time complexity:
            best/worst: O(1)
        Space complexity:
            O(1) for space complexity.
            Aux: O(1), no additional space needed.
        """
        self.index_map[x], self.index_map[y] = self.index_map[y], self.index_map[x]

    def add(self, location, key):
        """
        This function is used for the Dijkstra's algorithm to add the newly discovered location into the MinHeap.
        Add the newly discovered location with its time from start as a tuple to the end of the array.

        This function is inspired from FIT1008 Week 12 lecture and modified on top of it to meet the requirements of this assignment.

        Input:
            location: an int representing the id of the location.
            key: an int representing the time taken from start to this location.
        Time complexity:
            best: O(1), the newly added element does not need to be risen and stay at the end of the heap.
            worst: O(log|L|), the newly added element needed to be risen to the root position,
                    where |L| is the number of elements in minheap.
        Space complexity:
            O(1) for space complexity.
            Aux: O(1), no additional space needed.
        """
        self.length += 1
        self.my_array[self.length] = (location, key)
        self.index_map[location] = self.length
        self.rise(self.length)

    def serve(self):
        """
        This function return the root of the heap(location with the shortest time from the start).

        This function is inspired from FIT1008 Week 12 lecture and modified on top of it to meet the requirements of this assignment.

        Return:
            smallest: the root item in the heap, the location with the shortest time from start.
        Time complexity:
            best: O(1), when there is no sinking operation after the root element has been served.
            worst: O(log|L|), when after serving the root element, the swapped element has to be sunk all the way down
                    to the bottom of the heap. |L| is the number of elements in minheap.
        Space complexity:
            O(1) for space complexity.
            Aux: O(1), no additional space needed.
        """
        smallest = self.my_array[1][0]      # O(1)
        largest = self.my_array[self.length][0]
        self.swap(1, self.length)           # swap the root( the smallest item ) with the last item in the heap, O(1)
        self.index_swap(self.my_array[1][0], largest)         # swap the index mapping for the two items
        self.length -= 1                    # length decrease by 1, O(1)
        self.sink(1)                        # sink the swapped item to correct position
        return smallest                     # O(1)

    def sink(self, index):
        """
        This function sink the element at index to correct place.
        Sink compare time from source (location, key), by using the second item in the tuple as the key.

        This function is inspired from FIT 2004 Week 7 PASS, modified on top of it to meet the requirement.

        Input:
            index: an int value, representing the index of the element that need to be sunken to the correct position.
        Time complexity:
            best: O(1), when the element to be sunk is smaller than all its direct child.
            worst: O(log|L|), when the element sinks all the way to the bottom and |L| is the number of elements in minheap.
        Space complexity:
            O(1) for space complexity.
            Aux: O(1), no additional space needed.
        """
        # find the direct child of the element at this index
        child = 2 * index

        while child <= self.length:
            # if the right child is smaller than the left child, child index + 1
            if child < self.length and self.my_array[child + 1][1] < self.my_array[child][1]:
                child += 1
            # if the direct child of the element is smaller
            if self.my_array[index][1] > self.my_array[child][1]:
                self.swap(index, child)
                self.index_swap(self.my_array[index][0], self.my_array[child][0])
                index = child
                child = 2 * index
            else:
                break

    def update(self, location, key):
        """
        This function update the location and its time form start in the Heap if a shorter path if found during Dijkstra
        , it replaces the corresponding element in the Heap with its new time from start.

        Input:
            location: the location id of the location that needed to be updated.
            key: the new time from start value for this location, shorter than the current one.
            position: int value representing the index of the location in heap to be updated.
        Time complexity:
            best/worst: O(log|L|), for calling the rise operation. where |L| is the number of elements in heap.
        Space complexity:
            O(1) for space complexity.
            Aux: O(1), no additional space needed.
        """
        index = self.index_map[location]
        self.my_array[index] = (location, key)  # O(1)
        self.rise(index)                        # O(log|L|)


class Graph:
    """
    This is a class for making the Graph of locations and road, and searching for the shortest path using Dijkstra.

    Author: Lim Jun Yi
    student_id: 32625510
    Date: 2023/4/24
    """

    def __init__(self, locations):
        """
        Function description: This is the initialisation method for the Graph class.

        Approach description: It first finds the largest location id in 'locations', so we know the amount of locations and the
                                size of the list we need. Then it creates a location object for each index in the list where it represented the
                                location id.

        Input:
            locations: a list of tuples where each tuple in the list represented a road. The tuple included the start(a),
                        end(b), travel time for alone(c) and travelling time for carpool(d). (a, b, c, d)
        Time complexity:
            best/worst: O(|R| + |L|), where |R| is the number of roads and |L| is the number of locations.
                            It first has to loop through the roads to find the max location id and loop through the
                            range of amount_locations to assign the location object.
        Space complexity:
            O(|L|) for space complexity as the input in size |L|.
            Aux: O(|L|), where |L| is the number of locations.
        """
        self.amount_locations = max(r[1] for r in locations) + 1  # O(|R|), loop through roads

        self.locations = [None] * self.amount_locations      # O(|L|)

        for i in range(self.amount_locations):       # O(|L|)
            self.locations[i] = Location(i)

    def add_road_prep(self, roads, carpool):
        """
        Function description: This function is to extract the information from each road and create a Road object using the extracted information.
                                The road then will be added into each location object inside the graph with their corresponding id and later be
                                used in the Dijkstra's path algorithm.

        Approach description: Two types of graph is being made base on the mode selected. A normal graph will be made if
                                carpool lane is not being used while a reversed graph will be made if carpool lane is being used.

        Input:
            roads: a list of tuples where each tuple in the list represented a road. The tuple included the start(a),
                        end(b), travel time for alone(c) and travelling time for carpool(d). (a, b, c, d)
            carpool: a boolean value, True if carpool lane being used, False otherwise.
        Time complexity:
            best/worst: O(|R|), where |R| is the numbers of roads.
        Space complexity:
            O(|R|) for space complexity as the input is a list of roads, where |R| is the number of roads in 'roads'
            Aux: O(1), no additional space needed.
        """
        for item in roads:      # O(|R|)
            start = item[0]
            end = item[1]
            inv_time = item[2]
            carp_time = item[3]

            # conditioning, add roads for each location, if carpool then add time corresponding to carpool and vise versa
            if not carpool:
                current_road = Road(start, end, inv_time)   # O(1)
                self.locations[start].add_road(current_road)  # O(1)

            else:
                current_road = Road(end, start, carp_time)  # O(1)
                self.locations[end].add_road(current_road)  # O(1)

    def dijkstra(self, s):
        """
        Function description: This is a function to find the shortest path in a graph. It uses the MinHeap class where a minimum heap is being
                                used to store the discovered locations. inspired from FIT2004 week 5 lecture notes.

        Approach description: The Dijkstra algorithm traverse through the graph and find all the shortest time from the
                                current location to the source(s) location. It works by first searching through all the roads
                                that pointed out from the source location and check whether the destination of that road
                                has been discovered or visited yet. if not discovered, the destination(des) will be added
                                to the heap and given a key where the key is the time taken from source to this location.

                                if the current location is discovered, then if there's any shorter path being found, it will
                                update the destination time from start to a shorter one and given it a new parent. The location
                                will be sorted again to its correct position in the minheap.

                                when the minheap is emtpy mean the traversal has finished and all location has its parent
                                and shortest time from source.

        Input:
            s: an int representing the starting location of the graph
        Time complexity:
            The time complexity of this Dijkstra path algorithm is O(|L|+|L|*log|L|*n*2*log|L|), which simplify to
            O(|L|log|L|*nlog|L|), which can be further simplify to O(n|L|log|l|).
            And n is the maximum number of roads attached to a single location, |L| is the number of locations, we can
            conclude that n|L| = total number of roads and the final complexity will be O(|R|log|L|) where |R| is the total number of roads
            and |L| is the number to locations.
        Space complexity:
            O(|L|) for space complexity as the input is only an integer, and we have to create a MinHeap to stores all the discovered locations
            , O(|L| + 1) = O(|L|), where |L| is the number of locations.
            Aux: O(|L|), for creating the MinHeap.
        """
        self.locations[s].time_from_start = 0
        discovered = MinHeap(self.amount_locations)               # O(|L|)
        discovered.add(s, 0)                                    # O(1), first item, no need to rise.
        self.locations[s].discovered = True

        while discovered.length > 0:                            # O(|L|)
            current = discovered.serve()                        # current = integer representing a location id         O(log|L|)
            c_loc = self.locations[current]                     # c_loc = location obj
            c_loc.visited = True

            for road in c_loc.roads:                            # road = each edge of the vertex. (start, end, time)    O(n), where n is the numbers of roads start from each location
                des = self.locations[road.end]                  # road.end is integer, des = location obj

                if not des.discovered:                          # if not discovered, add to heap.
                    des.discovered = True
                    des.time_from_start = c_loc.time_from_start + road.time
                    des.previous = current
                    discovered.add(des.id, des.time_from_start)     # O(log|L|)

                elif not des.visited:                                              # if not visited, and there's shorter route, update it in heap.
                    if des.time_from_start > c_loc.time_from_start + road.time:
                        des.time_from_start = c_loc.time_from_start + road.time
                        des.previous = current
                        discovered.update(des.id, des.time_from_start)    # O(log|L|)

    def path(self, end, carpool):
        """
        Function description: This is a function to return the path of the shortest path found by the Dijkstra algorithm. It searches through
                                the self.previous instance variable in the location object and make a path list out of it.

        precondition: end is an integer representing the ending of a path and start != end.
        post-condition: path will contain the locations for shortest path.

        Approach description: Make a path array to store the path. Once it reaches a location with previous
                                equal to None, the while loop exit and finishing finding the path. the index is used to
                                keep track of the current last element in the array for path, so we can perform O(1) operation to
                                add in new path location.

                              The carpool param indicate whether we are finding a path for travelling alone or travelling
                               using carpool lane. It's also been used to deciding whether to revert the path or slice the path
                               from index 1 onwards till index. Useful for combining of two paths in OptimumRoute().
        Input:
            end: an int representing the destination.
            carpool: a boolean value, True if finding path for using carpool lane, False otherwise.
        Return:
            path[1:index]: path for travelling from 'end' to the destination using carpool lane
            path[-index:]: path for travelling from the source to 'end' using only non-carpool lane.
        Time complexity:
            best/worst: O(|L|), the while looping having overall O(|L|) complexity as it at most loop |L| times.
                        Returning of the path required list slicing which is also O(|L|). O(|L| + |L|) = O(|L|)
                        |L| is the number of locations.
        Space complexity:
            O(|L|) for space complexity as the input is only an integer and a boolean value, and a path array is needed to store the path from start to end.
            Aux: O(|L|), extra spaces needed for path. |L| is the numbers of locations.

        """
        path = [None] * self.amount_locations       # O(|L|)
        path[0] = end
        index = 1

        while self.locations[end].previous is not None:     # O(|L|)
            path[index] = self.locations[end].previous      # O(1)
            end = self.locations[end].previous          # O(1)
            index += 1

        if carpool:
            return path[1:index]     # O(|L|)
        else:
            reverse(path)      # O(|L|)
            return path[-index:]       # O(|L|)


def reverse(lst):
    """
    A function to reverse a list

    Input:
        lst: a list of item.
    Return:
        lst: a list that has been reversed.
    Time complexity:
        best/worst: O(n), where n is the number of items in the list.
    Space complexity:
        O(n) for space complexity, where n is the number of items in the list.
        Aux: O(1), no additional space is needed.
    """
    m = len(lst) // 2   # O(1)
    n = len(lst) - 1    # O(1)

    for i in range(m):          # O(n/2)
        lst[i], lst[n] = lst[n], lst[i]
        n -= 1
    return lst


class Location:
    """
    This class is for creating the location(vertex) for the Graph class. Each location will have 6 instance variables
     upon initiation.

    Author: Lim Jun Yi
    student_id: 32625510
    Date: 2023/4/24
    """

    def __init__(self, location_id):
        """
        This is the initialisation method for the Location class. Creating instance variable for each location in graph.

        Input:
            location_id: an int representing the location.
        Time complexity:
            best/worst: O(1)
        Space complexity:
            O(1) for space complexity.
            Aux: O(1), no additional space needed.
        """
        self.id = location_id
        self.roads = []     # a list containing all road that start from self
        self.time_from_start = inf     # set time taken from source to inf, so we can change we found a shorter time
        # backtracking uses for path
        self.previous = None
        self.discovered = False
        self.visited = False

    def add_road(self, road):
        """
        This is a method for adding the road to the 'roads' instance variable for location.

        Input:
            road: a road object where it started from this location and end somewhere.
        Time complexity:
            best/worst: O(1)
        Space complexity:
            O(1) for space complexity as the input is a Road object.
            Aux: O(1)
        """
        self.roads.append(road)


class Road:
    """
    This class is for creating the road(edge) object for the Graph class. Each road will consist of a starting point(start)
    , ending point(end) and the time taken to travel.

    Author: Lim Jun Yi
    student_id: 32625510
    Date: 2023/4/24
    """

    def __init__(self, start, end, time):
        """
        This is the initialisation method for the Road class. Create the object with 3 attributes, start, end and time.

        Input:
            start: an int representing the starting location of this road.
            end: an int representing the ending location of this road.
            time: an int representing the time taken to travel from start to end on this road.
        Time complexity:
            best/worst: O(1)
        Space complexity:
            O(1) for space complexity.
            Aux: O(1), no additional space needed.
        """
        self.start = start  # start
        self.end = end      # stop
        self.time = time  # time taken for alone


def optimalRoute(start, end, passengers, roads):
    """
    Function description: This function is used to find the fastest route between start and end. It achieved the goal
                            by representing the roads in a graph form and uses dijkstra's algorithm to find the shortest time
                            for each location form the start.

    Approach description: The approach is to first make two graph representing travelling alone without using any carpool lane
                            and make another graph for only travelling using carpool lane, which this graph is in reverse.
                            Then followed by adding the roads for each location in the graph, which is done by the add_road_prep
                            function in the Graph class.
                            Two dijkstra will run simultaneously to find the shortest time form source for each location in the graph,
                            where for travelling alone it starts from 'start' to 'end'; and 'end' to 'start' for travelling with
                            carpool.
                            After the dijkstra has complete, a function called passenger_pickup will determine whether is it worth it
                            to pick up any passenger alone the way by comparing the time from start for the destination location.
                            If not worth it the function return the shortest path for travelling alone and vise versa.
    Input:
        start: an int, departure location.
        end: an int, destination location.
        passengers: a list locations where there are potential passengers.
        roads: a list of roads with the corresponding travel times
    Return:
        carpool_travel: The shortest path for travelling where it picked up a passenger.
        alone_travel: The shortest path for travelling where it doesn't pick up passenger.
    Time complexity:
        Best/Worst: O(|R|log|L|), as this is the most significant complexity in the function.
                    where |R| is numbers of roads and |L| is the number of locations. Break down see individual function's doc above.
    Space complexity:
        The space complexity will be O(|L| + |P| + |R|), simplify to O(|L| + |R|), where |L| is the number of unique locations
                in the 'roads' and |R| is the number of roads.
        Aux: O(|L|), Graph(), dijkstra and the output path list both required O(|L|) aux space. O(|L|)+O(|L|)+O(|L|)+O(|L|)+O(|L|)+O(|L|) = O(|L|)

    """

    # make a graph consisted of all the locations for traveling alone and travelling with carpool
    alone = Graph(roads)    # O(|R| + |L|), Aux: O(|L|)
    carpool = Graph(roads)  # O(|R| + |L|), Aux: O(|L|)
    # add the roads to each corresponding location, if using carpool then True for the second param
    alone.add_road_prep(roads, False)   # O(|R|), Aux: O(1)
    carpool.add_road_prep(roads, True)  # O(|R|), Aux: O(1)
    # conducting Dijkstra on the two graph to find the distances from source for each location
    alone.dijkstra(start)   # O(|R|log|L|), Aux: O(|L|)
    carpool.dijkstra(end)   # O(|R|log|L|), Aux: O(|L|)

    def passenger_pickup(p_location, end):
        """
        This function to find the best place to pick up the passenger.

        Input:
            p_location: a list locations where there are potential passengers.
            end: an int presenting the destination location
        Return:
            pick_up: the location to pick up the passenger, None if all passenger location slow you down.
        Time complexity:
            best/worst: O(|P|), where |P| is the number of locations where there are potential passengers.
        Space complexity:
            The space complexity is O(P) where P is the numbers of locations with passenger.
            Aux: O(1), no additional space is needed
        """
        comb_time = alone.locations[end].time_from_start    # use the shortest time for travelling along as base case
        pick_up = None
        for p in p_location:    # O(|P|)
            if alone.locations[p].time_from_start + carpool.locations[p].time_from_start < comb_time:
                comb_time = alone.locations[p].time_from_start + carpool.locations[p].time_from_start   # O(1)
                pick_up = p     # O(1)
        return pick_up

    alone_travel = alone.path(end, False)   # O(|L|), Aux: O(|L|)
    pickup_loc = passenger_pickup(passengers, end)    # O(|P|)

    # if it's worth picking up passenger
    if pickup_loc is not None:
        carpool_travel = alone.path(pickup_loc, False) + carpool.path(pickup_loc, True)     # O(|L| + |L|), Aux: O(|L|)
        return carpool_travel  # O(|L|)

    # if it's not worth picking up passenger
    return alone_travel         # O(|L|)


def select_sections(occupancy_probability):
    """
    Function description: This function uses the dynamic programming to find the best place to store the HPC with the goal of using the minimum total space.
                            It returns a list consist of an integer which is the total space occupy by the placement of HPC and a list of tuples represents the
                            location of one section selected for removal.

    Approach description: The function will first find out the dimension of the given input(n*m), where n is the number of rows and m is the number of columns.
                            After knowing the dimension, I built a memo which is a matrix of the same size n*m to stores all the tabulated values from the recurrence relation,
                            follow the recurrence relation, the function filled up all the space in memo. This is achieved by using the bottom-up approach of dynamic programming.
                            To get the solution, I find the smallest value from the top of the memo(memo[0]) where it will contain the minimum total occupancy,
                            to get the location of each space that is removed from each row, a top to down backtracking on the memo is being conducted. And the result is added
                            to the selections_location list. The final result of minimum_total_occupancy and sections_location is being combined into a list and return as
                            the solution of the function.

    Input:
        occupancy_probability: It is a list of list, where there are n amount of interior lists and within the interior list there are m amount of columns.
                                Each interior list represented a different row of sections, where occupancy_probability[x][y] is an integer number of range 1 to 100(include) which
                                represent how many percent of that space is being used.
    Return:
        minimum_total_occupancy: an int showing the total occupancy that has been removed by the function.
        sections_location: a list of n amount of tuples(i,j), which indicate the location of the space that is being removed.
    Time complexity:
        best/worst: O(nm), because O(n+2m+3nm) = O(nm) as nm is the most significant in the bound. Where n is the number of rows, and m is the number of columns.
    Space complexity:
        The space complexity is O(nm), where n is the number of rows, and m is the number of columns.
        Aux: O(nm), as we need to create a memo matrix of size n*m to do backtracking and storing of tabulation values.
    """
    sections_location = []

    n = len(occupancy_probability)  # numbers of rows in occupancy_probability,     O(1) for time, O(1) for space
    m = len(occupancy_probability[0])  # numbers of columns/aisles in occupancy_probability,        O(1) for time, O(1) for space

    memo = [[0 for i in range(m)] for j in range(n)]     # making the memo matrix to store the tabulated value, O(nm) for both time and space
    memo[n-1] = occupancy_probability[n-1]  # O(1)

    # filling up the matrix with value, from the last row up
    for x in range(n-2, -1, -1):     # O(n)
        for y in range(m):    # O(m)
            # if y at the start of the row (conor), they can only choose to remove the space directly below or to the right
            if y == 0:
                memo[x][y] = min(memo[x+1][y], memo[x+1][y+1]) + occupancy_probability[x][y]     # O(1), only comparing two items
            # if y at the end of the row (conor), they can only choose to remove the space directly below or to the left from the next row
            elif y == m-1:
                memo[x][y] = min(memo[x+1][y], memo[x+1][y-1]) + occupancy_probability[x][y]     # O(1), only comparing two items
            # if y at any place in-between, they can choose to remove the space below, to the right or to the left from next row
            else:
                memo[x][y] = min(memo[x+1][y-1], memo[x+1][y], memo[x+1][y+1]) + occupancy_probability[x][y]    # O(1), only comparing three items

    minimum_total_occupancy = min(memo[0])  # O(m)

    start_pos = None    # O(1)

    for i in range(m):  # O(m)
        if memo[0][i] == minimum_total_occupancy:
            start_pos = i

    # to backtracking and get back the answer
    for x in range(n):      # O(n)
        # if the position of the item is at the start, it can only choose the one below or to the right
        if start_pos == 0:
            # find the minimum space for the two possible option a row below
            min_space = min(memo[x][start_pos], memo[x][start_pos+1])
            # find the index of that chosen space in the below row, slicing is used to prevent the returning of the index of the first similar item in the list.
            start_pos = memo[x][start_pos:].index(min_space) + start_pos           # O(m + m) = O(m)
            # add the chosen row(n) and column(m) into the result
            sections_location.append((x, start_pos))    # O(1)

        # if the position of the item is at the end, it can only choose the one below or to the left
        elif start_pos == m-1:
            # find the minimum space for the two possible option a row below
            min_space = min(memo[x][start_pos], memo[x][start_pos-1])
            # find the index of that chosen space in the below row, slicing is used to prevent the returning of the index of the first similar item in the list.
            start_pos = memo[x][start_pos-1:].index(min_space) + start_pos - 1     # O(m + m) = O(m)
            # add the chosen row(n) and column(m) into the result
            sections_location.append((x, start_pos))    # O(1)

        # else it can have three options adjacent to it.
        else:
            # find the minimum space for the three possible option a row below
            min_space = min(memo[x][start_pos-1], memo[x][start_pos], memo[x][start_pos+1])
            # find the index of that chosen space in the below row, slicing is used to prevent the returning of the index of the first similar item in the list.
            start_pos = memo[x][start_pos-1:].index(min_space) + start_pos - 1     # O(m + m) = O(m)
            # add the chosen row(n) and column(m) into the result
            sections_location.append((x, start_pos))    # O(1)

    return [minimum_total_occupancy, sections_location]     # O(n)
