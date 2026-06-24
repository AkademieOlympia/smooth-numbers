"""
Catalan Tree Generation and Manipulation

Implements binary tree structures, Catalan number generation,
and tree canonicalization for the EABC-Catalan project.
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple
from functools import cache


@dataclass(frozen=True)
class BinaryTree:
    """Immutable binary tree structure."""
    left: Optional['BinaryTree'] = None
    right: Optional['BinaryTree'] = None
    value: Optional[int] = None  # Leaf value (prime factor)
    
    @property
    def is_leaf(self) -> bool:
        return self.left is None and self.right is None
    
    @property
    def height(self) -> int:
        if self.is_leaf:
            return 0
        left_h = self.left.height if self.left else 0
        right_h = self.right.height if self.right else 0
        return 1 + max(left_h, right_h)
    
    @property
    def num_leaves(self) -> int:
        if self.is_leaf:
            return 1
        left_n = self.left.num_leaves if self.left else 0
        right_n = self.right.num_leaves if self.right else 0
        return left_n + right_n
    
    def __repr__(self) -> str:
        if self.is_leaf:
            return str(self.value)
        return f"({self.left}, {self.right})"


@cache
def catalan_number(n: int) -> int:
    """Compute n-th Catalan number: C_n = (2n)! / ((n+1)! * n!)"""
    if n <= 1:
        return 1
    
    result = 1
    for i in range(2, n + 1):
        result = result * (n + i) // i
    return result // (n + 1)


def generate_all_trees(k: int) -> List[BinaryTree]:
    """
    Generate all binary trees with k leaves (unlabeled).
    
    Returns C_{k-1} trees.
    """
    if k == 1:
        return [BinaryTree(value=0)]  # Placeholder leaf
    
    trees = []
    for i in range(1, k):
        left_trees = generate_all_trees(i)
        right_trees = generate_all_trees(k - i)
        
        for left in left_trees:
            for right in right_trees:
                trees.append(BinaryTree(left=left, right=right))
    
    return trees


def construct_left_tree(factors: List[int]) -> BinaryTree:
    """
    Construct left-heavy tree: (((p1 p2) p3) ... pk)
    """
    if len(factors) == 1:
        return BinaryTree(value=factors[0])
    
    # Build recursively from left
    tree = BinaryTree(
        left=BinaryTree(value=factors[0]),
        right=BinaryTree(value=factors[1])
    )
    
    for i in range(2, len(factors)):
        tree = BinaryTree(
            left=tree,
            right=BinaryTree(value=factors[i])
        )
    
    return tree


def construct_right_tree(factors: List[int]) -> BinaryTree:
    """
    Construct right-heavy tree: (p1 (p2 (... pk)))
    """
    if len(factors) == 1:
        return BinaryTree(value=factors[0])
    
    # Build recursively from right
    tree = BinaryTree(
        left=BinaryTree(value=factors[-2]),
        right=BinaryTree(value=factors[-1])
    )
    
    for i in range(len(factors) - 3, -1, -1):
        tree = BinaryTree(
            left=BinaryTree(value=factors[i]),
            right=tree
        )
    
    return tree


def construct_balanced_tree(factors: List[int]) -> BinaryTree:
    """
    Construct balanced tree via recursive bisection.
    """
    if len(factors) == 1:
        return BinaryTree(value=factors[0])
    
    mid = len(factors) // 2
    left = construct_balanced_tree(factors[:mid])
    right = construct_balanced_tree(factors[mid:])
    
    return BinaryTree(left=left, right=right)


def is_balanced(tree: BinaryTree, k: int) -> bool:
    """Check if tree has minimal height."""
    import math
    min_height = math.ceil(math.log2(k))
    return tree.height == min_height


def label_tree(tree: BinaryTree, factors: List[int]) -> BinaryTree:
    """
    Label leaves of unlabeled tree with prime factors (in-order).
    """
    counter = [0]  # Mutable counter
    
    def label_recursive(t: BinaryTree) -> BinaryTree:
        if t.is_leaf:
            result = BinaryTree(value=factors[counter[0]])
            counter[0] += 1
            return result
        else:
            return BinaryTree(
                left=label_recursive(t.left),
                right=label_recursive(t.right)
            )
    
    return label_recursive(tree)


# Example usage
if __name__ == "__main__":
    print("Catalan numbers:")
    for n in range(10):
        print(f"C_{n} = {catalan_number(n)}")
    
    print("\nAll trees with k=4 leaves:")
    trees_4 = generate_all_trees(4)
    print(f"Count: {len(trees_4)} (expected {catalan_number(3)})")
    
    print("\nCanonical trees for factors [2, 3, 5, 7]:")
    factors = [2, 3, 5, 7]
    print(f"Left:     {construct_left_tree(factors)}")
    print(f"Right:    {construct_right_tree(factors)}")
    print(f"Balanced: {construct_balanced_tree(factors)}")
