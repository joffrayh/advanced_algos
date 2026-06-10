import networkx as nx
import random
import math

def generate_island_graph(n_nodes, n_islands):
    """
    Generates a graph with distinct connected components (islands).
    """
    if n_islands > n_nodes:
        print("Error: Number of islands cannot exceed number of nodes.")
        return nx.Graph()

    G = nx.Graph()
    nodes_per_island = n_nodes // n_islands
    
    # Create disjoint islands
    for i in range(n_islands):
        # Create a cluster of nodes
        start_node = i * nodes_per_island
        # If it's the last island, take all remaining nodes
        end_node = (i + 1) * nodes_per_island if i < n_islands - 1 else n_nodes
        nodes = list(range(start_node, end_node))
        
        G.add_nodes_from(nodes)
        
        # Connect nodes within the island randomly to ensure it's connected
        # Create a path first to guarantee connectivity
        for j in range(len(nodes) - 1):
            G.add_edge(nodes[j], nodes[j+1])
        
        # Add random extra edges within the island for complexity
        for _ in range(len(nodes) * 2):
            if len(nodes) > 1:
                u, v = random.sample(nodes, 2)
                if u != v:
                    G.add_edge(u, v)
                
    return G

def run_bfs_with_budget(G, start_node, budget):
    """
    Runs BFS starting from start_node but stops if we exceed the budget X.
    Returns: (is_fully_discovered, size_of_component)
    """
    visited = {start_node}
    queue = [start_node]
    
    while queue:
        # If we have already exceeded our budget, stop early
        if len(visited) > budget:
            return False, len(visited)

        current = queue.pop(0)
        
        neighbors = list(G.neighbors(current))
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                
                # Check budget immediately upon adding
                if len(visited) > budget:
                    return False, len(visited)
                    
    # If queue is empty, we explored the whole component
    return True, len(visited)

def estimate_connected_components(G, samples=50):
    """
    Implements the lecture algorithm to estimate connected components.
    """
    n = G.number_of_nodes()
    b_values = []
    
    print(f"--- Running Estimation with r={samples} samples ---")
    
    for _ in range(samples):
        # 1. Pick a random vertex v
        v = random.choice(list(G.nodes()))
        
        # 2. Sample random variable X
        # Pr[X >= k] = 1/k.
        u = random.random()
        if u == 0: u = 0.0001 # Avoid division by zero
        X = math.floor(1 / u)
        
        # Cap X at n because component size can't exceed n
        if X > n: X = n
        
        # 3. Run BFS with budget X 
        fully_discovered, comp_size = run_bfs_with_budget(G, v, X)
        
        # 4. Determine b_i
        # If component is fully discovered (meaning Size <= X), b=1, else b=0
        if fully_discovered and comp_size <= X:
            b_i = 1
        else:
            b_i = 0
        b_values.append(b_i)

    # 5. Calculate final estimate: n/r * sum(b_i) 
    average_b = sum(b_values) / samples
    estimate = n * average_b
    
    return estimate

# --- Main Execution ---
if __name__ == "__main__":
    try:
        # 1. User Inputs
        print("\n--- Sublinear Time Algorithm Simulation ---")
        total_nodes = int(input("Enter total number of nodes (e.g., 1000): "))
        true_islands = int(input("Enter number of connected components (islands) (e.g., 20): "))
        
        # 2. Setup Graph
        print(f"\nGenerating graph with {total_nodes} nodes and {true_islands} components...")
        G = generate_island_graph(total_nodes, true_islands)

        if G.number_of_nodes() == 0:
            print("Graph generation failed. Exiting.")
        else:
            # 3. Get Ground Truth (for comparison)
            true_count = nx.number_connected_components(G)
            print(f"Ground Truth: The graph actually has {true_count} connected components.")
            print("-" * 40)

            # 4. Run the Sublinear Algorithm with existing list of r values
            sample_sizes = [10, 50, 100, 200, 2000]
            
            for r in sample_sizes:
                est = estimate_connected_components(G, samples=r)
                error = abs(est - true_count)
                percent_error = (error / true_count) * 100 if true_count > 0 else 0
                
                print(f"Sample size r={r}: Estimated Count = {est:.2f} (Error: {percent_error:.1f}%)")
                
    except ValueError:
        print("Invalid input. Please enter integer numbers.")