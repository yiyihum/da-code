from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict
import numpy as np
import pandas as pd

@dataclass
class Constraints(ABC):
    _params: str=''
    
    @abstractmethod
    def validate(self, value):
        pass
    
    @abstractmethod
    def process(self, value, map_dict):
        pass
    
    @abstractmethod
    def validate_and_process(self, value, map_dict):
        pass
    
    @abstractmethod
    def __str__(self):
        pass

@dataclass
class ArrayLike(ABC):
    _params: str="array-like"

    def validate(self, value):
        return hasattr(value, "__len__") or hasattr(value, "shape") or hasattr(value, "__array__")
    
    def process(self, value, map_label: Dict={}, target_type: str='int'):
        try:
            if isinstance(value, list): 
                value = np.array(value)
            elif isinstance(value, pd.DataFrame) or isinstance(value, pd.Series):
                value = value.values
            else:
                raise TypeError(f"ArrayLike noly support list, np.ndarray, pd.DataFrame, pd.Series type")
        except Exception as e:
            raise ValueError(f"{value} fails to convert to np.ndarray, because of {e}")
        
        def safe_convert(item, is_map: bool=False):
            try:
                return float(item) if target_type == "float" \
                    else int(item)
            except ValueError:
                if is_map:
                    return map_label.get(item, 0)
                else:
                    map_label[item] = 0
        
        if map_label:
            vectorized_convert = np.vectorize(safe_convert)
            numeric_array = vectorized_convert(numeric_array)
        else:
            vectorized_convert = np.vectorize(safe_convert)
            map_label = {k: idx for idx, k in enumerate(sorted(map_label))} if map_label \
                else {}
            numeric_array = vectorized_convert(safe_convert)
        
            return numeric_array, map_label

    def validate_and_process(self, value, map_dict: Dict={}, target_type: str='int'):
        
        validate_result = self.validate(value)
        if not validate_result:
            return None, {}, validate_result
        
        numeric_array, map_label = self.process(value, map_dict, target_type)
        
        return numeric_array, map_label, validate_result
        
    def __str__(self) -> str:
        return f"need a {self._params}"


