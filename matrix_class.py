class Matrix:

    def __init__(self, arr):
        self.matrix = arr

        for i in range(1,len(arr)):
            if len(arr[0]) != len(arr[i]):
                raise TypeError(
                    "Each row must have an equal number of columns")

        self.num_row = len(arr)
        self.num_col = len(arr[0])

    def show(self):
        for row in self.matrix:
            print(row)

    def transpose(self):
        place_holder_matrix = []

        for i in range(self.num_col):
            place_holder_row = []
            for j in range(self.num_row):
                place_holder_row.append(self.matrix[j][i])
            place_holder_matrix.append(place_holder_row)

        self.matrix = place_holder_matrix
        self.num_row, self.num_col = self.num_col, self.num_row
        return self

    def add(self, other_arr):

        if self.num_row != other_arr.num_row or self.num_col != other_arr.num_col:
            raise TypeError(
                "You cannot add/subtract matrices of differing dimensions.")

        for i in range(self.num_row):
            for j in range(self.num_col):
                self.matrix[i][j] += other_arr.matrix[i][j]
        return self

    def subtract(self, other_arr):

        self.add(other_arr.scalar_multiply(-1))
        return self

    def scalar_multiply(self, scalar):

        for i in range(self.num_row):
            for j in range(self.num_col):
                self.matrix[i][j] *= scalar
        return self

    def matrix_multiply(self, other_arr):
        if self.num_col != other_arr.num_row:
            raise TypeError(
                "The number of columns in the first matrix must equal the number of rows in the second!")
        else:
            other_arr.transpose()
            resultant_matrix = []
            for i in range(self.num_row):
                row_matrix = []
                for j in range(other_arr.num_col):
                    row_matrix.append(dot_product(
                        self.matrix[i], other_arr.matrix[j]))
                resultant_matrix.append(row_matrix)

            other_arr.transpose()

            self.matrix = resultant_matrix
            return self

    def recursive_determinant(self):
        if self.num_col != self.num_row:
            raise TypeError(
                "Rows and Columns must be equal to take the determinant")
        else:
            return calculate_determinant(self.matrix)
        
    def reduced_row_echelon_form(self):
        self.matrix = reduced_row_echelon_form_helper(self.matrix)
        return self
    
    def inverse_matrix_via_rref(self):
        self.matrix = inverse_matrix_via_rref(self.matrix)
        return self
    
    def determinant_via_rref(self):
        return determinant_via_rref(self.matrix)


def dot_product(arr1, arr2):
    if len(arr1) != len(arr2):
        raise TypeError("Vectors must be of equal length/dimension")
    else:
        dot_product_num = 0
        for i in range(len(arr1)):
            dot_product_num += arr1[i]*arr2[i]
        return dot_product_num


# Helper function for calculate_determinant
def remove_row_and_column(matrix, row, column):
    new_matrix = []
    for r in matrix:
        new_matrix.append(r[:]) # must copy in new matrix or else it would just be a reference and pop() the original Matrix object
    new_matrix.pop(row)
    for row in new_matrix:
        row.pop(column)
    return new_matrix

# Helper function for recursive_determinant that reduces overhead
# Ensure we dont need to make many Matrix objects
def calculate_determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]

    determinant = 0
    for i in range(len(matrix[0])):
        determinant += (-1)**i * matrix[0][i] * \
            calculate_determinant(remove_row_and_column(matrix, 0, i))
    return determinant

# ensures we don't need to make many Matrix objects
def reduced_row_echelon_form_helper(matrix):
    row_index = 0

    for column_index in range(len(matrix[0])): # looping through columns

        pivot_row_index = pivot_exists(matrix,row_index, column_index)

        if pivot_row_index != -1:

            if pivot_row_index != row_index:
                swap_rows(matrix, pivot_row_index, row_index)

            pivot_number = matrix[row_index][column_index]
            for i in range(len(matrix[row_index])):
                matrix[row_index][i] /= pivot_number
            
            for row in range(len(matrix)):
                if row == row_index:
                    continue
                else:
                    scalar = matrix[row][column_index]
                    for i in range(len(matrix[row])):
                        matrix[row][i] -= scalar * matrix[row_index][i]

            row_index += 1 
    
    # Deals with the float point issue of -0.0. Visually more appealing. Removable for pure computation speed
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix [i][j] == -0.0:
                matrix[i][j] = 0.0

    return matrix

# helper function for rref function
def pivot_exists(matrix,row_index, column_index):
    for i in range(row_index, len(matrix)):
        if matrix[i][column_index] != 0:
            return i #return index of the first row that isn't 0
    return -1 #signifies false

def swap_rows(matrix, row_index_1, row_index_2):
    matrix[row_index_1], matrix[row_index_2] = matrix[row_index_2], matrix[row_index_1] #tuple unpacking for ease

def inverse_matrix_via_rref(matrix):

    if calculate_determinant(matrix) == 0:
        raise TypeError("This matrix is not invertible, its determinant is 0")
    if len(matrix) != len(matrix[0]):
        raise TypeError("This matrix is not invertible, it is not a square matrix")

    # appending identity matrix
    for row_index in range(len(matrix)):
        for column_index in range(len(matrix[row_index])):
            if row_index == column_index:
                matrix[row_index].append(1)
            else:
                matrix[row_index].append(0)

    # rref
    rref_matrix = reduced_row_echelon_form_helper(matrix)

    # cut off left half (identity matrix)
    for row_index in range(len(rref_matrix)):
        rref_matrix[row_index] = rref_matrix[row_index][len(rref_matrix[row_index])//2:]
    
    return rref_matrix


# rref code + doing operations to reverse engineer determinant
def determinant_via_rref(matrix):

    new_matrix = []
    for row in matrix:
        new_matrix.append(row[:])

    determinant = 1
    row_index = 0

    for column_index in range(len(matrix[0])): # looping through columns

        pivot_row_index = pivot_exists(new_matrix,row_index, column_index)

        if pivot_row_index != -1:

            if pivot_row_index != row_index:
                swap_rows(new_matrix, pivot_row_index, row_index)
                determinant *= -1

            pivot_number = new_matrix[row_index][column_index]
            determinant *= pivot_number
            for i in range(len(new_matrix[row_index])):
                new_matrix[row_index][i] /= pivot_number
            
            for row in range(len(new_matrix)):
                if row == row_index:
                    continue
                else:
                    scalar = new_matrix[row][column_index]
                    for i in range(len(new_matrix[row])):
                        new_matrix[row][i] -= scalar * new_matrix[row_index][i]

            row_index += 1
        else:
            # No pivot found in this column means a row of zeros -> determinant is 0
            return 0
    
    return determinant 