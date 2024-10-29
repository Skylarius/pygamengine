from math import sqrt
from deprecated import deprecated
from typing import Tuple

class Transform:
    def __init__(self) -> None:
        self.__position: Tuple[float, float] = (0,0)
        self.__rotation: float = 0
        self.__scale: Tuple[float, float] = (1,1)
        self.__dirty = False
    
    def set_position(self, position: Tuple[float, float]):
        self.__position = position
        self.__dirty = True
    
    def set_rotation(self, rotation: float):
        self.__rotation = rotation
        self.__dirty = True

    def set_scale(self, scale: Tuple[float, float]):
        self.__scale = scale
        self.__dirty = True
    
    def get_position(self) -> Tuple[float, float]:
        return self.__position
    
    def get_rotation(self) -> float:
        return self.__rotation
    
    def get_scale(self) -> Tuple[float, float]:
        return self.__scale
    
    def force_update(self):
        self.__dirty = True

    def is_dirty(self) -> bool:
        return self.__dirty

    def clean(self):
        self.__dirty = False

    def is_dirty_and_then_clean(self):
        if self.__dirty:
            self.__dirty = False
            return True
        return False

    @staticmethod
    def lerp(A: tuple[float, float], B: tuple[float, float], t: float) -> tuple[float, float]:
        return A[0] + t * (B[0] - A[0]), A[1] + t * (B[1] - A[1])
    
    def get_relative_position(self, position: tuple[float, float]) -> tuple[float, float]:
        return (position[0] - self.__position[0], position[1] - self.__position[1])
    
    @staticmethod
    @deprecated("Use get_displacement() instead")
    def get_vectors_distance(A: tuple[float, float], B: tuple[float, float]) -> tuple[float, float]:
        return B[0] - A[0], B[1] - A[1]
    
    """
    Get displacement vector A and B (returns B - A vector)
    """
    @staticmethod
    def get_displacement(start_V: tuple[float, float], end_V: tuple[float, float]) -> tuple[float, float]:
        return end_V[0] - start_V[0], end_V[1] -  start_V[1]

    """Get vector lenght but don't apply square root (faster)"""    
    @staticmethod
    def get_vector_length_squared(V: tuple[float, float]) -> float:
        x, y = V
        return x*x + y*y
    
    @staticmethod
    def get_vector_length(V: tuple[float, float]) -> float:
        return sqrt(Transform.get_vector_length_squared(V))
    
    """
    Get squared distance between vectors (faster)
    """
    @staticmethod
    def get_distance_squared(A: tuple[float, float], B: tuple[float, float]) -> float:
        x, y = B[0] - A[0], B[1] - A[1]
        return x*x + y*y

    """
    Get distance between vectors
    """
    @staticmethod
    def get_distance(A: tuple[float, float], B: tuple[float, float]) -> float:
        return sqrt(Transform.get_distance_squared(A, B))
    
    @staticmethod
    def get_vectors_sum(*vectors: tuple[float, float]):
        sum_x = 0
        sum_y = 0
        for v in vectors:
            sum_x+=v[0]
            sum_y+=v[1]
        return sum_x, sum_y
    
    @staticmethod 
    def get_vectors_diff(A: tuple[float, float], B: tuple[float, float]) -> tuple[float, float]:
        return A[0] - B[0], A[1] - B[1]