

class Node(object):

    def __init__(self, key, parent=0):
        self.children = []
        self.key = key
        self.parent = parent
        self.pos = 0
        self.pos_in_ch = -1

    def __repr__(self):
        return '<Node: {}; +{}>'.format(self.key, len(self.children))


class GenericTree(object):

    def __init__(self):
        self.nodes = []
        self.root = 0

    def add_root(self, node):
        new_node_pos = len(self.nodes)
        node.pos = new_node_pos
        node.parent = -1
        self.nodes.append(node)

    def add_node(self, node, parent_index):
        if (len(self.nodes) == 0):
            self.add_root(node)
        else:
            new_node_pos = len(self.nodes)
            node.pos = new_node_pos
            node.parent = parent_index
            self.nodes.append(node)
            node.pos_in_ch = len(self.nodes[parent_index].children)
            self.nodes[parent_index].children.append(new_node_pos)


    def process_nodes(self, func):
        def process(index):
            func(index)
            for child in self.nodes[index].children:
                process(child)

        process(self.root)


    def iter_nodes2(self, index):

        current_node = index
        came_from = -1
        came_from_parent = True
        came_to_end = False
        skip = False

        while (not came_to_end):
            if came_from_parent:
                skip = False
                if len(self.nodes[current_node].children) > 0:
                    came_from = current_node
                    current_node = self.nodes[current_node].children[0]
                    came_from_parent = True
                else:
                    came_from = current_node
                    current_node = self.nodes[current_node].parent
                    came_from_parent = False
            else:
                skip = True
                if came_from == self.nodes[current_node].children[-1]:
                    came_from = current_node
                    if self.nodes[current_node].parent != -1:
                        current_node = self.nodes[current_node].parent
                        came_from_parent = False
                    else:
                        came_to_end = True
                else:
                    # next_child = self.nodes[current_node].children.index(came_from) + 1
                    next_child = self.nodes[came_from].pos_in_ch + 1
                    came_from = current_node
                    current_node = self.nodes[current_node].children[next_child]
                    came_from_parent = True
            if not skip:
                yield came_from
            else:
                yield -1

        raise StopIteration

def main():

    def f(something):
        print(something, end='\t')


    root = Node('Root')

    tree = GenericTree()
    tree.add_root(root)
    tree.add_node(Node('ch1'), 0)
    tree.add_node(Node('ch2'), 0)
    tree.add_node(Node('ch3'), 1)
    tree.add_node(Node('ch4'), 1)
    tree.add_node(Node('ch5'), 2)
    tree.add_node(Node('ch6'), 2)
    tree.add_node(Node('ch7'), 2)
    tree.add_node(Node('ch8'), 3)

    tree.process_nodes(f)
    print()
    g = tree.iter_nodes2(0)

    for node in g:
        if node != -1:
            print(tree.nodes[node])


if __name__ == '__main__':
    main()


