import networkx as nx
import math
import random

class RouteOptimizer:
    def __init__(self, bins, depot, num_trucks=1):
        """
        bins: List of dictionaries [{'lat': ..., 'lng': ..., 'id': ...}]
        depot: Dictionary {'lat': ..., 'lng': ...}
        num_trucks: Number of trucks to split the work between
        """
        self.bins = bins
        self.depot = depot
        self.num_trucks = num_trucks
        self.graph = nx.Graph()
        self.nodes = [('depot', depot['lat'], depot['lng'])] + \
                     [(f"bin_{b['id']}", b['lat'], b['lng']) for b in bins]
        self._build_graph()

    def _build_graph(self):
        """Builds a complete graph where nodes are locations and edges are Euclidean distances."""
        for i, (id1, lat1, lng1) in enumerate(self.nodes):
            for j, (id2, lat2, lng2) in enumerate(self.nodes):
                if i < j:
                    dist = math.sqrt((lat1 - lat2)**2 + (lng1 - lng2)**2)
                    self.graph.add_edge(id1, id2, weight=dist)

    def _get_path_for_bins(self, bin_subset):
        """Finds the shortest path for a specific subset of bins starting from the depot."""
        if not bin_subset:
            return []
            
        target_node_ids = [f"bin_{b['id']}" for b in bin_subset]
        unvisited = list(target_node_ids)
        current_node = 'depot'
        path_nodes = ['depot']

        while unvisited:
            nearest_neighbor = None
            min_dist = float('inf')

            for neighbor in unvisited:
                dist = nx.dijkstra_path_length(self.graph, current_node, neighbor)
                if dist < min_dist:
                    min_dist = dist
                    nearest_neighbor = neighbor
            
            path_nodes.append(nearest_neighbor)
            unvisited.remove(nearest_neighbor)
            current_node = nearest_neighbor

        node_map = {n[0]: {'lat': n[1], 'lng': n[2]} for n in self.nodes}
        return [node_map[node_id] for node_id in path_nodes]

    def solve_for_fleet(self):
        """Groups bins into geographic clusters and calculates a shortest path for each truck."""
        if not self.bins:
            return {}

        # Sort bins to ensure consistent clustering results
        self.bins.sort(key=lambda x: x['id'])
        
        # Use K-Means clustering to group bins spatially
        clusters = cluster_bins(self.bins, self.num_trucks)
        
        fleet_routes = {}
        for i, bin_subset in enumerate(clusters):
            truck_id = i + 1
            if bin_subset:
                fleet_routes[truck_id] = self._get_path_for_bins(bin_subset)
            else:
                fleet_routes[truck_id] = []
                
        return fleet_routes

    def _get_path_for_bins(self, bin_subset):
        """Finds the shortest path for a specific subset of bins starting from the depot."""
        if not bin_subset:
            return []
            
        target_node_ids = [f"bin_{b['id']}" for b in bin_subset]
        unvisited = list(target_node_ids)
        current_node = 'depot'
        path_nodes = ['depot']

        # Greedy Nearest Neighbor within the cluster
        while unvisited:
            nearest_neighbor = None
            min_dist = float('inf')

            for neighbor in unvisited:
                # Use Euclidean distance for speed at this scale, or Dijkstra if graph is complex
                dist = self.graph[current_node][neighbor]['weight']
                if dist < min_dist:
                    min_dist = dist
                    nearest_neighbor = neighbor
            
            path_nodes.append(nearest_neighbor)
            unvisited.remove(nearest_neighbor)
            current_node = nearest_neighbor

        node_map = {n[0]: {'id': n[0].replace('bin_', ''), 'lat': n[1], 'lng': n[2]} for n in self.nodes}
        # Special case for depot
        node_map['depot'] = {'id': None, 'lat': self.depot['lat'], 'lng': self.depot['lng']}
        
        return [node_map[node_id] for node_id in path_nodes]

def optimize_route(bins, depot, num_trucks=1):
    """Wrapper function for backward compatibility."""
    optimizer = RouteOptimizer(bins, depot, num_trucks)
    return optimizer.solve_for_fleet()


def cluster_bins(bins, k):
    """
    Groups bins into k clusters based on spatial proximity.
    bins: List of dicts with lat/lng
    k: Number of clusters (trucks)
    """
    if not bins or k <= 0:
        return []
    if k == 1:
        return [list(bins)]

    # Geographic Sector Clustering (Angular Sorting)
    # This ensures trucks cover distinct "pie-shaped" sectors of the city
    # which is the most efficient way to prevent route overlap.
    
    depot_lat, depot_lng = 20.9374, 77.7796
    
    def get_angle(b):
        return math.atan2(b['lat'] - depot_lat, b['lng'] - depot_lng)
    
    bins_sorted = sorted(bins, key=get_angle)
    
    clusters = []
    chunk_size = math.ceil(len(bins_sorted) / k)
    for i in range(k):
        start = i * chunk_size
        end = start + chunk_size
        subset = bins_sorted[start:end]
        if subset:
            clusters.append(subset)
            
    return clusters

def get_predicted_bins():
    """
    Optimized: Fetches all necessary logs in a single query and processes them.
    """
    from models import Bin, FillLog
    from datetime import datetime
    from collections import defaultdict
    
    predicted_bins = []
    # Only check bins > 60%
    bins_to_collect = Bin.query.filter(Bin.fill_level > 60).all()
    if not bins_to_collect:
        return []
        
    bin_map = {b.id: b for b in bins_to_collect}
    bin_ids = list(bin_map.keys())
    
    # Fetch all logs for these bins, ordered by timestamp desc
    # This might return many logs, but we only need the top 3 per bin.
    # We'll fetch them all and then filter in memory for simplicity at this scale.
    all_logs = FillLog.query.filter(FillLog.bin_id.in_(bin_ids)).order_by(FillLog.bin_id, FillLog.timestamp.desc()).all()
    
    logs_by_bin = defaultdict(list)
    for log in all_logs:
        if len(logs_by_bin[log.bin_id]) < 3:
            logs_by_bin[log.bin_id].append(log)
            
    for bin_id, logs in logs_by_bin.items():
        if len(logs) < 3:
            continue
            
        newest = logs[0]
        oldest = logs[2] # Since we ordered by desc
        
        time_diff = (newest.timestamp - oldest.timestamp).total_seconds() / 3600.0
        fill_diff = newest.fill_level - oldest.fill_level
        
        if time_diff > 0:
            fill_rate_per_hour = fill_diff / time_diff
            bin_item = bin_map[bin_id]
            predicted_fill = bin_item.fill_level + (fill_rate_per_hour * 2)
            
            if predicted_fill > 80:
                predicted_bins.append({
                    'id': bin_item.id,
                    'lat': bin_item.latitude,
                    'lng': bin_item.longitude,
                    'is_predicted': True
                })
                
    return predicted_bins


def get_priority_bins():
    """
    Calculates a Priority Score for each bin: 
    Score = Fill_Level + (Hours_Since_Last_Collection * 1.5).
    Returns bins with Score > 80.
    """
    from models import Bin
    from datetime import datetime
    
    priority_bins = []
    all_bins = Bin.query.all()
    now = datetime.utcnow()
    
    for bin_item in all_bins:
        # Avoid null checks if possible by using defaults
        last_t = bin_item.last_collected_at or bin_item.last_updated or now
        hours_since = (now - last_t).total_seconds() / 3600.0
            
        priority_score = bin_item.fill_level + (hours_since * 1.5)
        
        if priority_score > 80:
            priority_bins.append({
                'id': bin_item.id,
                'lat': bin_item.latitude,
                'lng': bin_item.longitude,
                'priority_score': priority_score,
                'is_priority': True
            })
            
    return priority_bins


