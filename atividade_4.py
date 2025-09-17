# -*- coding: utf-8 -*-
import random

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    # ---------------- MÉTODOS AUXILIARES ----------------
    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def update_height(self, node):
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    # ---------------- ROTAÇÕES ----------------
    def rotate_right(self, z):
        y = z.left
        T3 = y.right

        # Rotação
        y.right = z
        z.left = T3

        # Atualiza alturas
        self.update_height(z)
        self.update_height(y)

        return y

    def rotate_left(self, z):
        y = z.right
        T2 = y.left

        # Rotação
        y.left = z
        z.right = T2

        # Atualiza alturas
        self.update_height(z)
        self.update_height(y)

        return y

    # ---------------- INSERÇÃO ----------------
    def insert(self, node, key):
        if not node:
            return Node(key)

        # Inserção padrão BST
        if key < node.key:
            node.left = self.insert(node.left, key)
        elif key > node.key:
            node.right = self.insert(node.right, key)
        else:
            return node  # duplicatas não permitidas

        # Atualiza altura
        self.update_height(node)

        # Verifica balanceamento
        balance = self.get_balance(node)

        # Casos de rotação
        # Caso Esquerda-Esquerda
        if balance > 1 and key < node.left.key:
            return self.rotate_right(node)

        # Caso Direita-Direita
        if balance < -1 and key > node.right.key:
            return self.rotate_left(node)

        # Caso Esquerda-Direita
        if balance > 1 and key > node.left.key:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        # Caso Direita-Esquerda
        if balance < -1 and key < node.right.key:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def insert_key(self, key):
        self.root = self.insert(self.root, key)

    # ---------------- VISUALIZAÇÃO ----------------
    def print_tree(self, node=None, level=0, prefix="Raiz: "):
        if node is None:
            node = self.root
        if node:
            print(" " * (level * 4) + prefix + str(node.key) + f" (h={node.height})")
            if node.left:
                self.print_tree(node.left, level + 1, "L--- ")
            if node.right:
                self.print_tree(node.right, level + 1, "R--- ")

# ---------------- DEMONSTRAÇÃO ----------------
if __name__ == "__main__":
    avl = AVLTree()

    print("\n=== DEMONSTRAÇÃO COM VALORES FIXOS ===")
    print("\nCaso 1: Inserindo [10, 20, 30] (força rotação simples)")
    for val in [10, 20, 30]:
        avl.insert_key(val)
        avl.print_tree()
        print("---------------")

    avl = AVLTree()
    print("\nCaso 2: Inserindo [10, 30, 20] (força rotação dupla)")
    for val in [10, 30, 20]:
        avl.insert_key(val)
        avl.print_tree()
        print("---------------")

    print("\n=== DEMONSTRAÇÃO COM VALORES ALEATÓRIOS ===")
    avl_random = AVLTree()
    valores = random.sample(range(1, 100), 20)  # 20 inteiros aleatórios únicos
    print("Inserindo:", valores)
    for val in valores:
        avl_random.insert_key(val)

    print("\nÁrvore final balanceada:")
    avl_random.print_tree()
