"""Utilities for measuring performance metrics in tests"""
import time
import functools
from typing import Callable, Any
import psutil
import pytest

def measure_performance(func: Callable) -> Callable:
    """Decorator to measure runtime and memory usage of a function
    
    Args:
        func (Callable): Function to measure
        
    Returns:
        Callable: Wrapped function that prints performance metrics
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        # Get initial memory usage
        process = psutil.Process()
        memory_before = process.memory_info().rss / 1024 / 1024  # Convert to MB
        
        # Time the function
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        # Get final memory usage
        memory_after = process.memory_info().rss / 1024 / 1024
        
        # Print metrics
        print(f"\nPerformance metrics for {func.__name__}:")
        print(f"Runtime: {end_time - start_time:.4f} seconds")
        print(f"Memory usage: {memory_after - memory_before:.2f} MB")
        
        return result
    return wrapper 