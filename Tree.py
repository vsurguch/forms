

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

    def to_layers(self):

        layers = []
        current_layer = 0

        for node_index in self.iter_nodes2(0):
            if node_index != -1:
                if len(layers) < current_layer + 1:
                    layers.append([])
                layers[current_layer].append(node_index)
                current_layer += 1
            else:
                current_layer -= 1

        return layers

    def weigths(self):

        def process_node(index, result):
            sum = 1
            for child in self.nodes[index].children:
                sum += process_node(child, result)
            result[index] = sum
            return sum

        result = [0 for i in range(len(self.nodes))]

        process_node(0, result)

        return result

    def widths(self):

        def process_node(index, result):
            self_width = len(self.nodes[index].children)
            width = 0
            for child in self.nodes[index].children:
                width += process_node(child, result)
            if width == 0:
                width = 1
            res = self_width if self_width >= width else width
            result[index] = res
            return res

        result = [0 for i in range(len(self.nodes))]

        process_node(0, result)

        return result

    def positions(self):
        layers = self.to_layers()
        widths = self.widths()
        result = [0 for i in range(len(self.nodes))]

        result[0] = widths[0] / 2

        for layer in layers:
            for node_index in layer:
                node_pos = result[node_index]
                node_width = widths[node_index]
                leading_pos = node_pos - node_width / 2
                for child in self.nodes[node_index].children:
                    child_pos =  leading_pos + widths[child] / 2
                    leading_pos += widths[child]
                    result[child] = child_pos
        return result


def change_str_at_index(s, i, ch):
    s_start = s[:i]
    s_end = s[i:]
    return s_start + ch + s_end



def main():

    def f(something):
        print(something, end='\t')


    root = Node('Root')

    tree = GenericTree()
    tree.add_root(root)
    tree.add_node(Node('ch1'), 0)
    tree.add_node(Node('ch2'), 0)
    tree.add_node(Node('ch3'), 0)
    tree.add_node(Node('ch4'), 1)
    tree.add_node(Node('ch5'), 1)
    tree.add_node(Node('ch6'), 1)
    tree.add_node(Node('ch7'), 2)
    tree.add_node(Node('ch8'), 2)
    tree.add_node(Node('ch9'), 2)
    tree.add_node(Node('ch7'), 3)
    tree.add_node(Node('ch8'), 3)
    tree.add_node(Node('ch9'), 3)
    # tree.add_node(Node('ch10'), 2)

    tree.process_nodes(f)
    print()
    g = tree.iter_nodes2(0)



    for node in g:
        if node != -1:
            print(tree.nodes[node])

    layers = tree.to_layers()
    widths = tree.widths()
    positions = tree.positions()
    print(widths)
    print(positions)
    # strlength = widths[0] * 5
    # strcount = len(layers)
    #
    # for i in range(strcount):
    #     layerstr = ' ' * strlength
    #     layer =  layers[i]
    #     for node_index in layer:
    #         node_pos = positions[node_index]
    #         layerstr = change_str_at_index(layerstr, node_pos, str(node_index))
    #     print(layerstr)


if __name__ == '__main__':
    main()


