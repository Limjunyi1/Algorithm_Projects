"""
This is the file for assignment 2 part 1 and 2 for FIT 2004.

Author: Lim Jun Yi
student_id: 32625510
Date: 2023/5/26
"""
from collections import deque
from math import inf


class Network:
    """
    This is the graph class of the data centers, where it is represented as a network flow.

    Author: Lim Jun Yi
    student_id: 32625510
    Date: 2023/5/26
    """
    def __init__(self, maxIn, maxOut):
        """
        This is the initialisation method for the Network class.

        Approach: Find the amount of data center and create an array of its size + 1 to stores all the data centers.
                    Then loop through all the id for the data center and add them into the network correspondingly.

        Input:
            maxIn: A list of integers in which maxIn[i] specifies the maximum amount of incoming data that data centre i can process per second.
            maxOut: A list of integers in which maxOut[i] specifies the maximum amount of outgoing data that data centre i can process per second.
        Time complexity:
            best/worst: O(|D|), where checking the length of the maxIn and looping through the id of data centers costs a complexity of O(2|D|)=O(|D|).
                        Where |D| is the numbers of data centers.
        Space complexity:
            Aux: O(|D|), for making a network array of size |D|. Where |D| is the numbers of data centers.
        """
        self.sink_id = len(maxIn)  # O(|D|) # find the amount of data center, will also use this as the id for the sink node
        self.network = [None] * (self.sink_id + 1)  # make the graph, +1 for sink, +1 for source

        for i in range(self.sink_id):  # O|D|
            self.network[i] = DataCenter(i, maxIn[i], maxOut[i])    # O(1)

        self.network[self.sink_id] = DataCenter(self.sink_id)  # add sink node # O(1)

    def add_connection_prep(self, connections, target):
        """
        This is the method for adding the connections into the residue network.

        Approach: Loop through every connection in connections and add them into each data center correspondingly.

        Input:
            connections: A list of tuples (a, b, t) where: a is the ID of the data centre from which the communication channel departs.
                                                           b is the ID of the data centre to which the communication channel arrives.
                                                           t is a positive integer representing the maximum throughput of that channel.
            target: A list of data centres that are deemed appropriate locations for the backup data to be stored.
        Time complexity:
            best/worst: O(|C| + |T|), where looping the connections and target costs O(|C| + |T|).
                            |C| is number of connection and |T| is number of target centers.
        Space complexity:
            Aux: O(1), no additional space is needed.
        """
        # adding all the connections into the residue network
        for connection in connections:  # O|C|
            start = connection[0]
            end = connection[1]
            throughput = connection[2]

            forward_connection = Connection(start, end, throughput)
            backward_connection = Connection(end, start)
            self.network[start].add_connection(forward_connection)  # adding forward
            self.network[end].add_connection(backward_connection)   # adding backward

        # connect all the targets to a single sink
        for t in target:  # O|T|
            to_sink = Connection(t, self.sink_id, inf)
            from_sink = Connection(self.sink_id, t)
            self.network[t].add_connection(to_sink)
            self.network[self.sink_id].add_connection(from_sink)

    def bfs(self, parent_array, origin):
        """
        This is the method for find available path from origin to the sink.

        Approach: by using a deque data structure, the bfs algorithm traverse into the network layer by layer and find all the unvisited centers and set their index in the
                    visited array to true. it is done by going through all the connection for each center in the deque and stop once it reaches the sink node.

        Input:
            parent_array: An array that stores the parents of the center, where the center is represented by the index in the array.
            origin: The starting center id
        Return:
            True if there is a path and False otherwise.
        Time complexity:
            best/worst: O(|D| + |C|), where it is the complexity of BFS. Each center is entering and leaving at most 1 time and scanning for all adjacent connections takes O(|C|).
                            Where |D| is the number of data centers and |C| is the number of total connections.
        Space complexity:
            Aux: O(|D|), for making the visited array and deque.
        """
        visited = [False] * (self.sink_id + 1)  # O(|D|) # sink_id + 2 = the total amount of data centers + 2(sink and source)

        my_queue = deque([origin])
        visited[origin] = True  # set origin as visited

        while my_queue:
            current_id = my_queue.popleft()  # O(1)

            for connection in self.network[current_id].connection:
                # only go in if this the target is not visited and the target still can take in more data or source still can give out.
                if not visited[connection.end] and connection.flow > 0 and self.network[connection.end].maxIn > 0 and self.network[connection.start].maxOut > 0:
                    visited[connection.end] = True
                    my_queue.append(connection.end)
                    parent_array[connection.end] = connection

                    if connection.end == self.sink_id:
                        return True

        return False

    def ford_fulkerson(self, origin):
        """
        This is the method for finding the maximum flow of this network.

        Approach: Making a parent array to store the path of the BFS traversal, this will be used to determine the smallest flow along this particular path.
                    We will run the residue network that we had made earlier on BFS until there is no more possible path from the origin to any of the targets.
                    If there is a path in the residue network, the BFS will fill up the parent array, and we will loop through the parent array from back to front and check for the
                    smallest flow within the path, after we got the smallest flow in this path, we will update the path from target to origin with the minimum flow.
                    Where the MaxIn of the receiving center on that connection will be deducted by the min flow and the maxOut on the source center will also be deducted by that amount,
                    follow by deducting the amount on the connection itself. And the opposite if done to the backward flow where we add the flow amount onto it, so it can be used later by the bfs
                    if out current path is not optimal.

                    The process is repeated until there is no path left on the residue network( BFS returned False ), all the min flow of the path will be added and sum to a max flow.

        Input:
            origin: The starting center id
        Return:
            max_throughput: The maximum possible data throughput from the data centre origin to the data centres specified in targets.
        Time complexity:
            best/worst: O(|D||C|^2), where it is deveried from O(|D|+(|D|+|C|)(|D|+|D||C|)) = O(|D|+|D|^2+|D|^2|C|+|C||D|+|D||C|^2). Taking the largest complexity we will end up with
                         O(|D||C|^2), where |D| is the number of data centers and |C| is the number of total connections.
        Space complexity:
            Aux: O(|D|), for making the parent array.
        """
        parent_array = [-1] * (self.sink_id + 1)  # O(|D|) # sink_id + 1= the total amount of data centers + 1(sink)
        max_throughput = 0

        while self.bfs(parent_array, origin):  # O(|D|+|C|) # while there is path in residue
            current_id = parent_array[self.sink_id].start
            flow = inf
            while current_id != origin:  # O(|D|) # to find the smallest flow along the path
                parent_connection = parent_array[current_id]  # get the connection from parent to current
                flow = min(parent_connection.flow, flow)  # find the smallest flow
                # update the smallest flow along the path
                # if flow > source's maxOut
                if flow > self.network[parent_connection.start].maxOut:
                    flow = self.network[parent_connection.start].maxOut
                    parent_connection.flow = flow
                # if flow > target's maxIn
                if flow > self.network[parent_connection.end].maxIn:
                    flow = self.network[parent_connection.end].maxIn
                    parent_connection.flow = flow
                current_id = parent_array[current_id].start  # update current

            # after the second while loop, the flow should be the smallest flow along the path.
            # update the residue
            current_id = parent_array[self.sink_id].start

            while current_id != origin:  # O(|D|)
                backward_connection = None
                parent_connection = parent_array[current_id]  # get the connection from parent to current

                for connection in self.network[parent_connection.end].connection:  # O(|C|)
                    if connection.end == parent_connection.start:
                        backward_connection = connection
                        break

                # update the maxIn and maxOut and connection flow
                parent_connection.flow -= flow
                self.network[parent_connection.start].maxOut -= flow
                self.network[parent_connection.end].maxIn -= flow

                # update the backward connection flow
                backward_connection.flow += flow

                current_id = parent_array[current_id].start

            max_throughput += flow

        return max_throughput


class DataCenter:
    """
    This is the class for the Data center.

    Author: Lim Jun Yi
    student_id: 32625510
    Date: 2023/5/26
    """

    def __init__(self, center_id, maxIn=None, maxOut=None):
        """
        This is the initialisation method for the DataCenter class. Where each data center is being assigned to its corresponding value.

        Input:
            center_id: An int, representing the center id.
            maxIn: An int, representing the max inflow of data to this center. Default = None
            maxOut: An int, representing the max outflow of this center. Default = None
        Time complexity:
            best/worst: O(1)
        Space complexity:
            Aux: O(1)
        """
        self.center_id = center_id
        self.connection = []  # a list that containing all the connection that start from self
        if maxIn is not None and maxOut is not None:
            self.maxIn = maxIn
            self.maxOut = maxOut
        else:
            self.maxIn = inf

    def add_connection(self, connection):
        """
        This is the method to add connection into the data center.

        Input:
            connection: A Connection object, representing the flow from one center to another center.
        Time complexity:
            best/worst: O(1)
        Space complexity:
            Aux: O(1)
        """
        self.connection.append(connection)


class Connection:
    """
    This is the class for the connection(edge) of the data centers, it is one directional from start center to an end center.

    Author: Lim Jun Yi
    student_id: 32625510
    Date: 2023/5/26
    """

    def __init__(self, start, end, flow=0):
        """
        This is the initialisation method for the Connection class. Where each connection is being assigned to its corresponding value.

        Input:
            start: An int, representing the source center.
            end: An int, representing the target center.
            flow: An int, representing the maximum data flow of this connection can take. Default = 0
        Time complexity:
            best/worst: O(1)
        Space complexity:
            Aux: O(1)
        """
        self.start = start
        self.end = end
        self.flow = flow


def maxThroughput(connections, maxIn, maxOut, origin, targets):
    """
    This is the method for finding the maximum flow of this network.

    Approach: Check the approaches for ford_fulkerson(self, origin) in the Network class as they're having the same approaches.

    Input:
        connections: A Connection object, representing the flow from one center to another center.
        maxIn: A list of integers in which maxIn[i] specifies the maximum amount of incoming data that data centre i can process per second.
        maxOut: A list of integers in which maxOut[i] specifies the maximum amount of outgoing data that data centre i can process per second.
        origin: The starting center id
        targets: A list of data centres that are deemed appropriate locations for the backup data to be stored.
    Return:
        max_throughput: The maximum possible data throughput from the data centre origin to the data centres specified in targets.
    Time complexity:
        best/worst: O(|D||C|^2), as the ford_fulkerson(origin) is the method that contribute the most significant complexity.
    Space complexity:
        Aux: O(|D|), for making the parent array and a network array of size |D|. Where |D| is the numbers of data centers.
    """
    residue = Network(maxIn, maxOut)    # O(|D|)
    residue.add_connection_prep(connections, targets)  # O(|C| + |T|)
    max_throughput = residue.ford_fulkerson(origin)  # O(|D||C|^2)
    return max_throughput


# The following codes are for the assignment part 2, CatGPT
class CatsTrie:
    """
    This is the class for that encapsulates all the cat sentences and make it into a trie data structure.
    It includes all the necessary methods and attributes that is needed to perform the auto complication of the cat sentences.

    Author: Lim Jun Yi
    student_id: 32625510
    Date: 2023/5/26
    """

    def __init__(self, sentences):
        """
        This is the initialisation method for the CatsTrie class. Creating the Trie from the given sentences list.
        Done by first creating a root Node and loop through all the sentences in the sentences list and add them into the
        Trie.

        Detailed explanation see sub method(@insert_sentence(self, sentence)).

        Input:
            sentences: A list of String with all the sentences.
        Time complexity:
            best/worst: O(NM), where looping each sentence in the input costs O(N) time complexity and inserting each sentence costs O(M) time complexity.
                        Where N = the number of sentence in sentences and M = the number of characters in the longest sentence.
        Space complexity:
            Aux: O(M), as we need to create the parent list in the sub method(insert_sentence) in order to go back up and update the occurrence of each character.
                    M = the number of characters in the longest sentence.
        """
        self.root = Node()  # O(1)

        for sentence in sentences:  # O(N)
            self.insert_sentence(sentence)  # O(M + M + M) = O(M)

    def insert_sentence(self, sentence):
        """
        This method insert the given sentence into the Trie data structure, from root going downward.

        Approach: The method will create a path array which is also kind of like a parent array, where it will store the parent of current node by the index of the array. For example,
                    current index of the array is 0 and in path[0] it will be filled with the root node as its parent.
                  Then the method loop through the given sentence to obtain the characters in the sentence then adding them into the Trie following the conditions in the below codes.
                  After all the characters has been inserted and path being filled up, I created an exit which is located at the 0th index of the link array. And follow by a call to a sub
                    method(@update_max_occur(self, path)) to update the occurrence of each character.

        Input:
            sentences: A String representing a sentence from the cat language.
        Time complexity:
            best/worst: O(M), where it is derived from M+M+M=3M, ignoring the constant of 3, hence O(M).
                            Coming the making the path array which take a complexity of O(M), looping through the sentence with also take a complexity of O(M) and
                            updating occurrence with O(M) time complexity. Where M = the number of characters in the longest sentence.
        Space complexity:
            Aux: O(M), as we need to create the parent list in the sub method(insert_sentence) in order to go back up and update the occurrence of each character.
        """
        current_node = self.root
        index = 0
        path = [-1] * (len(sentence) + 1)   # O(M), making parent list

        for char in sentence:   # O(M)
            mapping = ord(char) - 96  # O(1) # map a = 1, b = 2, c = 3 etc...

            if current_node.link[mapping] is None:      # if new, create a new connection
                current_node.link[mapping] = Node(char)

            # else, move on
            path[index] = current_node
            current_node = current_node.link[mapping]
            index += 1

        if current_node.link[0] is None:        # if a new word, create a new exit
            current_node.link[0] = Node(sentence)   # O(1)

        # occurrence of this word + 1
        current_node.link[0].occurrence += 1
        path[index] = current_node        # add the last char into the path list.

        self.update_max_occur(path)   # O(M), calling sub method to update the occurrence of all character in this sentence

    def update_max_occur(self, path):
        """
        This method is being used to update the occurrence of each character if they have a smaller occurrence than the current sentence.

        Input:
            path: A list of Node objects, representing the path/parents array of the current sentence in the Trie.
        Time complexity:
            best: O(1), in best case, the while loop will run only one time when the second last character in the sentence has a greater occurrence
                    than the occurrence of the current sentence.
            worst: O(M), updating all the characters' occurrence in the sentence. And M = the number of characters in the longest sentence.
        Space complexity:
            Aux: O(1), no additional space is needed.
        """
        index = -1
        occurrence = path[index].link[0].occurrence     # getting the occurrence of the current sentence

        while path[index] != self.root and path[index].occurrence < occurrence:     # O(M) # checking whether the previous character has a smaller occurrence than this sentence
            path[index].occurrence = occurrence     # update the occurrence
            index -= 1

    def search_emtpy(self, current):
        """
        This is a recursion method to find the most frequent sentence in sentences that begins with the prompt.

        Approach: The base case check whether there is an exit for the current node's link array, if there is an exit and the occurrence of the last character( the current node )
                    of the sentence have a similar occurrence with the exit( the sentence stored in the exit node ), it will return the data stored within the exit which is the auto-completed sentence.
                   In case those two occurrence does not meet( not same ), we will loop from 1-27 to find the max occurrence from a to b, we continue update the max_occur variable which will
                    stores the value of the max occurrence in those a-b and the mapping index of the corresponding character.
                   After we found the mapping index of the character that has the max occurrence, we recall the method itself and feed the new node into the parameter and repeat until the
                    most frequent sentence in sentences that begins with the prompt is found.

        Input:
            current: The starting node/character to begin the search with.
        Return:
            current.data: The completed sentence with the highest frequency in the
                            cat Trie data structure.
        Time complexity:
            best: O(1), when the current node has an exit in its node.link array and the sentence has the same occurrence/frequency as the last character,
                    where it will return the sentence stored in the exit node.
            worst: O(Y), when it does not find the sentence within the first given node. It will have to search down the Trie and look for the most frequent sentence in the Trie
                    that begin with the character in the current node(current.data). Where the current node can be the root of the Trie in the case of an emtpy input for auto-completion,
                    or it also can be the last character of the input prompt.
                    Y is the remaining length of the most frequent sentence in sentences that has the prompt as its prefix, remaining length can be seen as having the same complexity as the full length.
        Space complexity:
            Aux: O(1), no additional space is needed
        """

        # if the node has an exit and the current node have the same occurrence has the sentence in the node does, return the sentence.
        if current.link[0] is not None and current.link[0].occurrence == current.occurrence:    # O(1)
            current = current.link[0]
            return current.data

        max_occur = [0, 0]  # The occurrence of the letter, the position of the letter

        for i in range(1, 27):  # O(26) = O(1)
            if current.link[i] is not None and current.link[i].occurrence > max_occur[0]:
                max_occur = [current.link[i].occurrence, i]

        return self.search_emtpy(current.link[max_occur[1]])

    def autoComplete(self, prompt):
        """
        This method will perform the operation needed to complete the prompt, based on the most commonly used sentences.

        Approach: First set the current start node as the root of the Trie, then check the length of the input prompt.
                    If the input prompt has a length greater than 0, we will loop through each character in the sentence and jumping into each level of Trie respectively.
                    If there is a mapping index that lead to None in the current node.link array, we should return None as this sentence is not in sentences.
                    After we traversed through all the character, and they all do not lead to None, we will the sub method self.search_emtpy(current) to search for the auto-completion.
                    Same for when the input prompt have a length of 0, we also call the sub method self.search_emtpy(current), where we feed the current node as the starting search point.

                    For detailed explanation and approaches on self.search_emtpy(current), check corresponding docs for such method.

        Input:
            prompt: A string with characters in the set of [a...z]. This string represents the
                        incomplete sentence that is to be completed by the catGPT.
        Return:
            self.search_emtpy(current): The result gotten back from this sub method. The completed sentence with the highest frequency in the
                            cat Trie data structure. None if it does not exit.
        Time complexity:
            The time complexity for this method is output sensitive.
            The time complexity will be O(X+Y) if there is a sentence begin with the prompt, as we will first need to check the length of the prompt and looping through the characters in prompt
                , then we will move into the Trie to traverse through the character and find the last character's node, to find whether there is an exit, if not we continue to traverse by looking for the
                node with the most occurrence until we found an exit with the similar occurrence. The total complexity will be O(X+X+Y) which simplify to O(X+Y).
            The time complexity will be O(X) if sentences that begins with the prompt does not exit, O(X+X)=O(X), for checking the size and going looping through the sentence.
            The time complexity will also be O(X+Y) when the input prompt is emtpy, just that in this case the X would be 0.
            Where X is the length of the prompt and Y is the remaining length of the most frequent sentence in sentences that begins with the prompt, remaining length can be seen as having the same complexity as the full length.
        Space complexity:
            Aux: O(1), no additional space is needed.
        """
        current = self.root     # O(1)
        size = len(prompt)      # O(X)

        if size != 0:    # O(1)
            for char in prompt:     # O(X)
                mapping = ord(char) - 96
                if current.link[mapping] is not None:
                    current = current.link[mapping]
                else:
                    return None

            return self.search_emtpy(current)   # O(Y)

        return self.search_emtpy(current)       # O(Y)


class Node:
    """
    This is the class for the character in the sentence, each character is represented as a node in the Trie data structure.

    Author: Lim Jun Yi
    student_id: 32625510
    Date: 2023/5/26
    """
    def __init__(self, data=None):
        """
        This is the initialising method for the Node class.

        Input:
            data: The data to be stores in the node, default to None.
        Time complexity:
            best/worst: O(1)
        Space complexity:
            Aux: O(27) which is O(1) constant.
        """
        self.link = [None] * 27
        self.data = data
        self.occurrence = 0
