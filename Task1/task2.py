#Function for the desired operations
def min_max_from_unique(nums):
    # Remove duplicates using set and convert back to list
    unique_nums = list(set(nums))
    
    # Create a tuple from the unique numbers
    unique_tuple = tuple(unique_nums)
    
    # Find minimum and maximum numbers
    min_num = min(unique_nums)
    max_num = max(unique_nums)
    
    return unique_tuple, min_num, max_num

# Read numbers from the user as input
nums = input("Enter a list of integers separated by commas: ").split(',')
nums = [int(num) for num in nums]

# Call the function and assign them to the unique variables
unique_tuple, min_num, max_num = min_max_from_unique(nums)

# Output the results
print("Unique tuple:", unique_tuple)
print("Minimum number:", min_num)
print("Maximum number:", max_num)

