import sys
import os

# Add backend directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from logic.optimizer import RouteOptimizer

def test_optimizer():
    depot = {'lat': 19.0760, 'lng': 72.8777}
    bins = [
        {'id': 1, 'lat': 19.0800, 'lng': 72.8800},
        {'id': 2, 'lat': 19.0700, 'lng': 72.8700},
        {'id': 3, 'lat': 19.0750, 'lng': 72.8900}
    ]
    
    optimizer = RouteOptimizer(bins, depot)
    path = optimizer.get_shortest_path()
    
    print("Optimization Path:")
    for i, point in enumerate(path):
        print(f"{i}: {point}")
    
    assert len(path) == 4
    assert path[0] == depot
    print("Test Passed!")

if __name__ == "__main__":
    test_optimizer()
