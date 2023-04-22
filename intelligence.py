import numpy as np
from matplotlib import pyplot as mat_plot

def find_red_pixels(map_filename, upper_threshold=100, lower_threshold=50):
    """
    Finds all red pixels in the image and writes the 2D array into a file named as map-red-pixels.jpg

    Returns:
        2D numpy array representing the output binary image 

    Keyword arguments:
    ------------------
    map_filename -- filename
        Filename of the file to be processed
    
    upper_threshold -- 100
        Upper limit for a particular colour channel

    lower_threshold -- 50
        Lower limit for a particular colour channel
    """
    # Read in a color image with PNG format
    rgb_img = mat_plot.imread(map_filename)

    # Convert to [0 - 255] range
    rgb_img = rgb_img * 255

    # Create a copy of 3D array which RGB will be changed i.e., new black and white image will be stored here
    new_img = rgb_img.copy()

    # Iterate over a 3D array and check each pixel for the correspondence to red colour
    for row in range(len(rgb_img)):
        for column in range(len(rgb_img[row])):
            # If red - change to white [255,255,255]
            if new_img[row][column][0] > upper_threshold and new_img[row][column][1] < lower_threshold and new_img[row][column][2] < lower_threshold:
                for i in range(3):
                    new_img[row][column][i] = 255
            # If not red - change to black [0,0,0]
            else:
                for i in range(3):
                    new_img[row][column][i] = 0

    # Convert image back to [0-1] range
    new_img = new_img / 255

    # Save a jpg file with the 3D image
    mat_plot.imsave('map-red-pixels.jpg', new_img)
    
    return new_img


def find_cyan_pixels(map_filename, upper_threshold=100, lower_threshold=50):
    """
    Finds all cyan pixels in the image and writes the 2D array into a file named as map-cyan-pixels.jpg

    Returns:
        2D numpy array representing the output binary image 

    Keyword arguments:
    ------------------
    map_filename -- filename
        Filename of the file to be processed
    
    upper_threshold -- 100
        Upper limit for a particular colour channel

    lower_threshold -- 50
        Lower limit for a particular colour channel
    """
    # Read in a color image with PNG format
    rgb_img = mat_plot.imread(map_filename)

    # Convert to [0 - 255] range
    rgb_img = rgb_img * 255

    # Create a copy of 3D array which RGB will be changed i.e., new black and white image will be stored here
    new_img = rgb_img.copy()

    # Iterate over a 3D array and check each pixel for the correspondence to red colour
    for row in range(len(rgb_img)):
        for column in range(len(rgb_img[row])):
            # If red - change to white [255,255,255]
            if new_img[row][column][0] < lower_threshold and new_img[row][column][1] > upper_threshold and new_img[row][column][2] > upper_threshold:
                for i in range(3):
                    new_img[row][column][i] = 255
            # If not red - change to black [0,0,0]
            else:
                for i in range(3):
                    new_img[row][column][i] = 0

    # Convert image back to [0-1] range
    new_img = new_img / 255

    # Save a jpg file with the 3D image
    mat_plot.imsave('map-cyan-pixels.jpg', new_img)
    
    return new_img


def detect_connected_components(img):
    """
    Determines all connected components in a binary image taking into account 8 neighbours of each pavement pixel.
    Writes (and creates if this file does not exist) the length of each connected component and the total number of connected components into the file 'cc-output-2a.txt'

    Returns:
        2D numpy array mark which stores the detected connected components
        
    Keyword argument:
    -----------------
    img -- ndarray
        2D array which represents the binary image output from either find_red_pixels or find_cyan_pixels function
    """

    image = img
    # Converting the image array from [0 - 1] to [0 - 255]
    image = image * 255
    # Convert image into 2D numpy array for convenience of checking the value of a pixel
    image = image[:,:,0]
    
    # Finding the shape of the image array
    shapes = image.shape

    # Creating mark array which will store the connected components: 0 - unvisited
    # Values greater than 0 correspond to the corresponding connected component
    # Initially set all elements as unvisited
    mark = np.zeros(shapes)

    # Empty queue-liked ndarray
    q = np.array([], dtype=np.int32)

    # Index variable which will be assinged to the element in the corresponding connected component 
    # e.g., all elements in Connected component 1 will have value 1 etc.
    index = 1

    # Iterate over each pixel in imgage array 
    for pixel_row in range(shapes[0]):
        for pixel_column in range(shapes[1]):
            # Check if it's the pavement pixel and the element in mark is still unvisited
            if image[pixel_row][pixel_column] == 255 and mark[pixel_row][pixel_column] == 0:
                # Assign the element in mark with the corresponding number of the connected component
                mark[pixel_row][pixel_column] = index
                # Append the row and column of that pixel into the queue
                q = np.append(q, [int(pixel_row), int(pixel_column)])

                # Do until queue is empty
                while np.any(q):
                    # Take the first pixel in the queue i.e., its row and column value into the temporary variable
                    temp_pixel = [q[0], q[1]]
                    # Delete this pixel from the queue i.e., its row and column since they are stored one after the other
                    q = np.delete(q, 0)
                    q = np.delete(q, 0)

                    # Check if the pixel corresponds to the one in the left top corner
                    # Add only 3 neighbours since it only borders 3 elements
                    if temp_pixel[0] == 0 and temp_pixel[1] == 0:
                        neighbours = [
                                [temp_pixel[0],temp_pixel[1]+1],
                                [temp_pixel[0]+1,temp_pixel[1]],
                                [temp_pixel[0]+1,temp_pixel[1]+1]]

                    # Else check if the pixel corresponds to the one in the right top corner
                    # Add only 3 neighbours since it only borders 3 elements
                    elif temp_pixel[0] == 0 and temp_pixel[1] == shapes[1]:
                        neighbours = [
                                [temp_pixel[0],temp_pixel[1]-1],
                                [temp_pixel[0]+1,temp_pixel[1]-1],
                                [temp_pixel[0]+1,temp_pixel[1]]]

                    # Else check if the pixel corresponds to the one in the left bottom corner
                    # Add only 3 neighbours since it only borders 3 elements
                    elif temp_pixel[0] == shapes[0] and temp_pixel[1] == 0:
                        neighbours = [
                                [temp_pixel[0]-1,temp_pixel[1]],
                                [temp_pixel[0]-1,temp_pixel[1]+1],
                                [temp_pixel[0],temp_pixel[1]+1]]

                    # Else check if the pixel corresponds to the one in the right bottom corner
                    # Add only 3 neighbours since it only borders 3 elements
                    elif temp_pixel[0] == shapes[0] and temp_pixel[1] == shapes[1]:
                        neighbours = [
                                [temp_pixel[0]-1,temp_pixel[1]-1], 
                                [temp_pixel[0]-1,temp_pixel[1]],
                                [temp_pixel[0],temp_pixel[1]-1]]
                    
                    # Else check if the pixel corresponds to the any pixel in the first row
                    # Add only 5 neighbours since it does not have neighbours above it
                    elif temp_pixel[0] == 0:
                        neighbours = [
                                [temp_pixel[0],temp_pixel[1]-1],
                                [temp_pixel[0],temp_pixel[1]+1],
                                [temp_pixel[0]+1,temp_pixel[1]-1],
                                [temp_pixel[0]+1,temp_pixel[1]],
                                [temp_pixel[0]+1,temp_pixel[1]+1]]

                    # Else check if the pixel corresponds to the any pixel in the last row
                    # Add only 5 neighbours since it does not have neighbours underneath it
                    elif temp_pixel[0] == shapes[0]:
                        neighbours = [
                                [temp_pixel[0]-1,temp_pixel[1]-1], 
                                [temp_pixel[0]-1,temp_pixel[1]],
                                [temp_pixel[0]-1,temp_pixel[1]+1],
                                [temp_pixel[0],temp_pixel[1]-1],
                                [temp_pixel[0],temp_pixel[1]+1]]

                    # Else check if the pixel corresponds to the any pixel in the first column
                    # Add only 5 neighbours since it does not have neighbours on the left
                    elif temp_pixel[1] == 0:
                        neighbours = [
                                [temp_pixel[0]-1,temp_pixel[1]],
                                [temp_pixel[0]-1,temp_pixel[1]+1],
                                [temp_pixel[0],temp_pixel[1]+1],
                                [temp_pixel[0]+1,temp_pixel[1]],
                                [temp_pixel[0]+1,temp_pixel[1]+1]]

                    # Else check if the pixel corresponds to the any pixel in the last column or the one before the last 
                    # Otherwise a neighbour with non-existing column index would be added
                    # Add only 5 neighbours since it does not have neighbours on the right
                    elif temp_pixel[1] == shapes[1] or temp_pixel[1] == (shapes[1] - 1):
                        neighbours = [
                                [temp_pixel[0]-1,temp_pixel[1]-1], 
                                [temp_pixel[0]-1,temp_pixel[1]],
                                [temp_pixel[0],temp_pixel[1]-1],
                                [temp_pixel[0]+1,temp_pixel[1]-1],
                                [temp_pixel[0]+1,temp_pixel[1]]]

                    # Else if it's a 'normal' pixel - add row, column of all its 8 neighbours
                    else:
                        neighbours = [[temp_pixel[0]-1,temp_pixel[1]-1], 
                                    [temp_pixel[0]-1,temp_pixel[1]],
                                    [temp_pixel[0]-1,temp_pixel[1]+1],
                                    [temp_pixel[0],temp_pixel[1]-1],
                                    [temp_pixel[0],temp_pixel[1]+1],
                                    [temp_pixel[0]+1,temp_pixel[1]-1],
                                    [temp_pixel[0]+1,temp_pixel[1]],
                                    [temp_pixel[0]+1,temp_pixel[1]+1]]
                    
                    # Iterate over each neighbour pixel
                    for neighbour in neighbours:
                        # Check if it's the pavement pixel and the element in mark is still unvisited
                        if image[neighbour[0]][neighbour[1]] == 255 and mark[neighbour[0]][neighbour[1]] == 0:
                            # Assign the element in mark with the corresponding number of the connected component
                            mark[neighbour[0]][neighbour[1]] = index
                            # Append the row and column of that pixel into the queue
                            q = np.append(q, [int(neighbour[0]),int(neighbour[1])])

                # If the queue is empty meaning that the whole connected component was found:
                # Open 'cc-ouput-2a.txt' file to append a string which contains the number of the current connected component and its length in pixels
                with open('cc-output-2a.txt', 'a') as f:
                    f.write(f'Connected component {index}, number of pixels = {len(np.where(mark == index)[0])}\n')
                
                # Add 1 to the index variable corresponding to the number of the next connected component
                index += 1
    
    # Once each pixel was iterated over:
    # Open 'cc-ouput-2a.txt' file to append a string which contains the total number of connected components 
    # (index -1) since after the last connected component index was still increased by 1
    with open('cc-output-2a.txt', 'a') as f:
        f.write(f'Total number of connected components = {index - 1}')

    return mark


def detect_connected_components_sorted(mark):
    """
    Sorts the connected components returned from detect_connected_components function in descending order.
    Writes (and creates if this file does not exist) the sorted by length connected components into the file 'cc-output-2b.txt'
    Writes the top two largest connected components into a file 'cc-top-2.jpg'

    Returns:
        0

    Keyword argument:
    -----------------
    mark -- ndarray
        2D numpy array returned from detect_connected_components function which contains elements with numbers corresponding to the connected components 
    """

    # Create a temporary list which will store the number of pixels and a corresponding connected component number
    components = []

    # Interate over mark array to find out the number of pixels in each corresponding connected component
    for row_index in range(len(mark)):
        for column_index in range(len(mark[row_index])):
            # Check if it's the element of a connected component
            if mark[row_index][column_index] > 0:
                # Check if the number of added connected components is smaller than the current connected component number
                # If smaller - this means that it's the first element of this connected component
                # Thus, append a list where first element is the 1 (first element of this component) and the second element is the number of this connected component
                if len(components) < int(mark[row_index][column_index]):
                    components.append([1,int(mark[row_index][column_index])])
                # Else if not - this means that the list for this connected component already exists
                # Add 1 to the number of pixels of this connected component 
                else:
                    components[int(mark[row_index][column_index])-1][0] += 1
    
    # Perform insertion sorting
    for i in range(1, len(components)):
        key = components[i]
        j = i
        while j >= 1 and components[j-1][0] > key[0]:
            components[j] = components[j-1]
            j = j - 1
        components[j] = key

    # Write all connected components into the file in a descending order
    with open('cc-output-2b.txt', 'a') as f:
        for index in range(len(components)-1,-1,-1):
            f.write(f'Connected component {components[index][1]}, number of pixels = {components[index][0]}\n')
        f.write(f'Total number of connected components = {len(components)}')
    
    # Create a temporary list for binary image of two largest connected components
    image_array = []

    # Retrieve the numbers of the two largest connected components
    two_largest = [components[-1][1], components[-2][1]]

    # Iterate over each element in mark array to find the pixels corresponding to the two largest connected components
    for pixel_row in range(len(mark)):
        # For each new row append an empty list to the image_array
        image_array.append([])
        for pixel_column in range(len(mark[pixel_row])):
            # If the element is in either of the two largest connected components - add a white pixel ([255, 255, 255]) to image_array
            if int(mark[pixel_row][pixel_column]) in two_largest:
                image_array[pixel_row].append([255,255,255])
            # Else add a black pixel ([0, 0, 0]) to image_array
            else:
                image_array[pixel_row].append([0,0,0])

    # Convert image_array into ndarray
    nump_array = np.array(image_array) 
    # Convert the range of the array form [0 - 255] into [0 - 1]
    nump_array = nump_array / 255
    
    # Save the ndarray as a binary image containing two largest connected components
    mat_plot.imsave('cc-top-2.jpg', nump_array)

    return 0