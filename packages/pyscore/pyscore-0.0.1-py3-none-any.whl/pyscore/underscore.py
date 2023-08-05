class _: 

    #Array/Tuple utilities
    
    # Returns everything but the last entry of the array. Pass n to exclude the last n elements from the result.
    def first(self, array, n = 1):
        return array[:n]
    
    # Returns the last element of an array. Passing n will return the last n elements of the array.
    def last(self, array, n = 1):
        return array[len(array)-n:]
    
    # Returns the rest of the elements in an array. Pass an index to return the values of the array from that index onward.
    def rest(self, array, index = 1):
        return array[index:]
    
    #Flattens a nested array (the nesting can be to any depth). If you pass shallow, the array will only be flattened a single level.
    def flatten(self, array, shallow = False):
        if shallow:
            flat_list = []
            for sublist in array: 
                if type(sublist) == list:
                    for item in sublist:
                        flat_list.append(item)
                else:
                    flat_list.append(sublist)
            return flat_list
        else:
            if array == []:
                return array
            if isinstance(array[0], list):
                return self.flatten(array[0], False) + self.flatten(array[1:], False)
            return array[:1] + self.flatten(array[1:], False) 
    
    # Returns a copy of the array with all instances of the values removed.
    def without(self, array, *values):
        result_list = array
        for value in values:
            result_list = list(filter(lambda val: val != value, result_list))
        return result_list
        
    # Computes the union of the passed-in arrays: the list of unique items, in order, that are present in one or more of the arrays.
    def union(self, *arrays):
        result_set = set()
        for array in arrays:
            result_set.update(array)
        return list(result_set)
    
    # Computes the list of values that are the intersection of all the arrays. Each value in the result is present in each of the arrays.
    def intersection(self, *arrays):
        if (len(arrays) == 1): return arrays[0]
        result_set = set(arrays[0]).intersection(arrays[1])
        for array in arrays:
            result_set.intersection(array)
        return list(result_set)

    # Similar to without, but returns the values from array that are not present in the other arrays.
    def difference(self, array, *others):
        #create a single array
        combined_array, result_array = [], []
        for other_array in others:
            combined_array.extend(other_array)
        for value in array:
            if not value in combined_array:
                result_array.append(value)
        return result_array


_ = _()
array = [1,1,2,2,4,5,8]
tpl = (1,2,3,4,5,6,7,8,9,10)

print (_.difference([1, 2, 3, 4, 5], [5, 2, 10]))