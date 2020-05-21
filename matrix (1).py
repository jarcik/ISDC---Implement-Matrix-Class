import math
from math import sqrt
import numbers

def zeroes(height, width):
        """
        Creates a matrix of zeroes.
        """
        g = [[0.0 for _ in range(width)] for __ in range(height)]
        return Matrix(g)

def identity(n):
        """
        Creates a n x n identity matrix.
        """
        I = zeroes(n, n)
        for i in range(n):
            I.g[i][i] = 1.0
        return I

class Matrix(object):

    # Constructor
    def __init__(self, grid):
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])

    #
    # Primary matrix math methods
    #############################
 
    def determinant(self):
        """
        Calculates the determinant of a 1x1 or 2x2 matrix.
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate determinant of non-square matrix.")
        if self.h > 2:
            raise(NotImplementedError, "Calculating determinant not implemented for matrices largerer than 2x2.")
        
        if(self.h == 1):
            return self[0][0]
        
        if(self.h == 2):
            return self[0][0]*self[1][1] - self[0][1]*self[1][0]

    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate the trace of a non-square matrix.")
        
        s = 0
        
        for i in range(self.h):
            row = []
            for j in range(self.w):
                if(i == j):
                    s += self[i][j]
            
        return s

    def inverse(self):
        """
        Calculates the inverse of a 1x1 or 2x2 Matrix.
        """
        if not self.is_square():
            raise(ValueError, "Non-square Matrix does not have an inverse.")
        if self.h > 2:
            raise(NotImplementedError, "inversion not implemented for matrices larger than 2x2.")
        
        if(self.h == 1):
            return Matrix([[1/self[0][0]]])

        a = self[0][0]
        b = self[0][1]
        c = self[1][0]
        d = self[1][1]
        determinant = self.determinant()
        if(determinant == 0):
            raise ValueError('Matrix 2x2 not invertible')   

        inverse = []
        scalar = 1/determinant
        inverse = [[d*scalar, -1*b*scalar], [-1*c*scalar, a*scalar]]
        return Matrix(inverse)

    def T(self):
        """
        Returns a transposed copy of this Matrix.
        """
        matrix_transpose = []
        row = []

        for i in range(self.w):        
            row = []
            for j in range(self.h):
                row.append(0)
            matrix_transpose.append(row)


        for i in range(self.h):        
            row = []
            for j in range(self.w):
                matrix_transpose[j][i] = self[i][j]

        return Matrix(matrix_transpose)

    def is_square(self):
        return self.h == self.w
    
    # dot product of two vectors as a helper function to multiplication
    def dot_product(self, vectorA, vectorB):
        result = 0

        for i in range(len(vectorA)):
            result += vectorA[i] * vectorB[i]

        return result
    
    
    #
    # Begin Operator Overloading
    ############################
    def __getitem__(self,idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]

        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    def __repr__(self):
        """
        Defines the behavior of calling print on an instance of this class.
        """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s

    def __add__(self,other):
        """
        Defines the behavior of the + operator
        """
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be added if the dimensions are the same") 
        result = []
        
        for i in range(self.h):
            row = []
            for j in range(self.w):
                row.append(self[i][j] + other[i][j])
            result.append(row)
        
        return Matrix(result)

    def __neg__(self):
        """
        Defines the behavior of - operator (NOT subtraction)

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1.0  -2.0
          -3.0  -4.0
        """
        result = []
        
        for i in range(self.h):
            row = []
            for j in range(self.w):
                row.append(-1 * self[i][j])
            result.append(row)
        
        return Matrix(result)

    def __sub__(self, other):
        """
        Defines the behavior of - operator (as subtraction)
        """
        result = []
        
        for i in range(self.h):
            row = []
            for j in range(self.w):
                row.append(self[i][j] - other[i][j])
            result.append(row)
        
        return Matrix(result)

    def __mul__(self, other):
        """
        Defines the behavior of * operator (matrix multiplication)
        """
         
        product = []
        otherTranspose = other.T()

        for i in range(self.h):
            row = []
            for j in range(other.w):
                row.append(self.dot_product(self[i], otherTranspose[j]))
            product.append(row)
            
        return Matrix(product)

    def __rmul__(self, other):
        """
        Called when the thing on the left of the * is not a matrix.

        Example:

        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2.0  0.0
          0.0  2.0
        """
        if isinstance(other, numbers.Number):
            pass
                
        result = []
        
        for i in range(self.h):
            row = []
            for j in range(self.w):
                row.append(other * self[i][j])
            result.append(row)
        
        return Matrix(result)
            