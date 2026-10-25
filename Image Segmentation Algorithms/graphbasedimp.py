# -------------------------------------------------------------
# Graph-Based Image Segmentation (Felzenszwalb-Huttenlocher)
# Pure Python Implementation (NO IMPORT MODULES USED)
# -------------------------------------------------------------

# Graph-Based Segmentation Algorithm:
# 1. Represent image as an undirected graph G = (V, E) where:
#    - Vertices V are image pixels.
#    - Edges E connect 4-neighbor pixels with weight w(u, v) = |I(u) - I(v)|.
# 2. Sort edges by weight in non-decreasing order.
# 3. Use Disjoint Set Union (DSU / Union-Find) to maintain components C.
#    Internal difference: Int(C) = maximum edge weight in MST of C.
#    Threshold function: tau(C) = k / |C| (where k is scale parameter).
# 4. For each edge (u, v) with weight w:
#    If components C1 = find(u) and C2 = find(v) are distinct, and
#    w <= min(Int(C1) + tau(C1), Int(C2) + tau(C2)):
#        Merge C1 and C2 into a single component!
# 5. Output segmented component labels.

class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n
        self.internal_diff = [0.0] * n
        
    def find(self, u):
        path = []
        while self.parent[u] != u:
            path.append(u)
            u = self.parent[u]
        # Path compression
        for node in path:
            self.parent[node] = u
        return u
        
    def union(self, u, v, weight):
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u == root_v:
            return
            
        # Union by rank
        if self.rank[root_u] < self.rank[root_v]:
            root_u, root_v = root_v, root_u
            
        self.parent[root_v] = root_u
        self.size[root_u] += self.size[root_v]
        self.internal_diff[root_u] = weight
        if self.rank[root_u] == self.rank[root_v]:
            self.rank[root_u] += 1

def graph_based_segmentation(image, k_scale=100.0):
    H = len(image)
    W = len(image[0])
    N = H * W
    
    # 1. Build edges between 4-connected neighbors
    edges = []
    for r in range(H):
        for c in range(W):
            u = r * W + c
            # Right neighbor
            if c + 1 < W:
                v = r * W + (c + 1)
                w = abs(float(image[r][c]) - float(image[r][c + 1]))
                edges.append((w, u, v))
            # Bottom neighbor
            if r + 1 < H:
                v = (r + 1) * W + c
                w = abs(float(image[r][c]) - float(image[r + 1][c]))
                edges.append((w, u, v))
                
    # 2. Sort edges by weight in ascending order
    edges.sort(key=lambda e: e[0])
    
    # 3. Initialize Disjoint Set
    dsu = DisjointSet(N)
    
    # 4. Greedily merge components
    for w, u, v in edges:
        root_u = dsu.find(u)
        root_v = dsu.find(v)
        
        if root_u != root_v:
            # Mint1 = Int(C1) + k / |C1|
            m_int1 = dsu.internal_diff[root_u] + (k_scale / dsu.size[root_u])
            # Mint2 = Int(C2) + k / |C2|
            m_int2 = dsu.internal_diff[root_v] + (k_scale / dsu.size[root_v])
            
            # Boundary threshold predicate
            if w <= min(m_int1, m_int2):
                dsu.union(root_u, root_v, w)
                
    # 5. Extract segmented labels
    label_map = {}
    current_label = 1
    segmented_labels = [[0 for _ in range(W)] for _ in range(H)]
    
    for r in range(H):
        for c in range(W):
            u = r * W + c
            root = dsu.find(u)
            if root not in label_map:
                label_map[root] = current_label
                current_label += 1
            segmented_labels[r][c] = label_map[root]
            
    return segmented_labels, len(label_map)

# Sample 8x8 image with two distinct regions (Left half vs Right half)
sample_image = [
    [ 30,  32,  28,  35, 190, 195, 205, 200],
    [ 28,  30,  34,  28, 195, 200, 198, 202],
    [ 32,  29,  31,  33, 200, 205, 202, 198],
    [ 30,  32,  28,  35, 192, 198, 200, 204],
    [ 34,  30,  32,  30, 190, 195, 202, 198],
    [ 28,  34,  30,  28, 195, 200, 198, 202],
    [ 32,  28,  30,  32, 200, 205, 202, 198],
    [ 30,  32,  28,  30, 192, 198, 200, 204]
]

labels, num_components = graph_based_segmentation(sample_image, k_scale=50.0)

print("=" * 65)
print(" GRAPH-BASED IMAGE SEGMENTATION (Felzenszwalb-Huttenlocher)")
print(" Pure Python Implementation (NO IMPORT MODULES USED)")
print("=" * 65)

print("\n--- Original Input Image (8x8) ---")
for row in sample_image:
    print("  ", [f"{p:3d}" for p in row])

print(f"\nNumber of Segmented Components: {num_components}")

print("\n--- Segmented Component Labels ---")
for row in labels:
    print("  ", [f"{p:2d}" for p in row])

print("\n--- ASCII Visual of Graph Segments (A = Component 1, B = Component 2) ---")
symbols = ["A", "B", "C", "D", "E"]
for row in labels:
    print("  " + " ".join(symbols[(p - 1) % len(symbols)] for p in row))
print("=" * 65)
