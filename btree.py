class BTreeNode:
    def __init__(self, order, leaf=False):
        self.order = order
        self.leaf = leaf
        self.keys = []
        self.children = []

    def insert_non_full(self, key, value):
        i = len(self.keys) - 1
        if self.leaf:
            while i >= 0 and key < self.keys[i]:
                i -= 1
            self.keys.insert(i + 1, key)
            self.children.insert(i + 1, value)
        else:
            while i >= 0 and key < self.keys[i]:
                i -= 1
            i += 1
            if len(self.children[i].keys) == (2 * self.order) - 1:
                self.split_child(i)
                if key > self.keys[i]:
                    i += 1
            self.children[i].insert_non_full(key, value)

    def split_child(self, i):
        order = self.order
        new_node = BTreeNode(order, self.children[i].leaf)
        parent_node = self.children[i]
        
        self.keys.insert(i, parent_node.keys[order - 1])
        self.children.insert(i + 1, new_node)
        
        new_node.keys = parent_node.keys[order: (2 * order) - 1]
        parent_node.keys = parent_node.keys[0: order - 1]
        
        if not parent_node.leaf:
            new_node.children = parent_node.children[order: (2 * order)]
            parent_node.children = parent_node.children[0: order]
            
    def traverse(self):
        # Traverse the B-Tree in order
        for i in range(len(self.keys)):
            if not self.leaf:
                yield from self.children[i].traverse()
            yield self.keys[i]
        if not self.leaf:
            yield from self.children[len(self.keys)].traverse()


class BTree:
    def __init__(self, order):
        self.root = BTreeNode(order, True)
        self.order = order

    def insert(self, key, value):
        if self.root is None:  # Check if the root is None (empty tree)
            self.root = BTreeNode(self.order, True)  # Create a new root

        root = self.root
        if len(root.keys) == (2 * self.order) - 1:
            new_node = BTreeNode(self.order)
            new_node.children.append(self.root)
            new_node.split_child(0)
            new_node.insert_non_full(key, value)
            self.root = new_node
        else:
            root.insert_non_full(key, value)

    def search(self, key):
        if self.root is None:  # Check if the root is None
            return None  # Return None if the tree is empty
        return self._search(self.root, key)

    def _search(self, node, key):
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if i < len(node.keys) and node.keys[i] == key:
            return node.children[i]  # Return the value associated with the key
        if node.leaf:
            return None
        return self._search(node.children[i], key)

    def update(self, key, new_value):
        # Find the key and update its value
        node = self.search(key)
        if node is not None:
            # Here we assume that the node returned is the value associated with the key
            # Update the value
            index = self._find_key(self.root, key)
            if index < len(self.root.keys) and self.root.keys[index] == key:
                self.root.children[index] = new_value  # Update the value directly

    def _find_key(self, node, key):
        idx = 0
        while idx < len(node.keys) and node.keys[idx] < key:
            idx += 1
        return idx

    def traverse(self):
        return list(self.root.traverse())
