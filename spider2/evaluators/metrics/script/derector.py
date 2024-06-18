from typing import Any, Dict
from inspect import signature
from functools import wraps


class Processparams:
    
    def __init__(self, params_dict: Dict,skip_process: bool=False):
        self.params_dict = params_dict
        self.skip_process = skip_process
        
    def get_constraint(self, constraint):
        pass
    
    def validate_and_convert(self, params: Dict, callname: str):
        map_dict = {}
        processed_params = []
        #TODO
        #Edit the process of params
        for param_name, param_val in params.items():
            constraints = self.params_dict[param_name]            
            if constraints.lower() == 'no_validate':
                continue
            constraints = constraints if isinstance(constraints, list) \
                else [constraints]
            constraints = [self.get_constraint(constraint) for constraint in constraints]

            for constraint in constraints:
                pass

            
        
    
    def __call__(self,func) -> Any:
        @wraps(func)
        def wrapper(*args, **kwargs):
            setattr(func, "_ml_parameter_constraints", self.params_dict)
            if self.skip_process:
                return func(*args, **kwargs)
            
            func_sig = signature(func)
            # Map *args/**kwargs to the function signature
            params = func_sig.bind(*args, **kwargs)
            params.apply_defaults()
            
            to_ignore = [
                p.name
                for p in func_sig.parameters.values()
                if p.kind == p.VAR_POSITIONAL
            ]
            to_ignore += ["self"]
            params = {k: v for k, v in params.arguments.items() if k not in to_ignore}

            self.validate_and_convert(params, callname=func.__qualname__)
        
        return wrapper
            
            

        
            
    