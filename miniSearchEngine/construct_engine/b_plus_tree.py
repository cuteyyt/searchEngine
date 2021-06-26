import sys
import bisect
import os.path
import time
import numpy


class Node:
    def __init__(self, engine_path, filename=None, ):
        self.keys = list()
        self.children = list()
        self.is_leaf = False
        self.filename = ""
        self.next = ""
        self.engine_path = engine_path

        if filename:
            self.read_data_from_file(filename)

    def read_data_from_file(self, filename):
        global file_counter
        global disk_counter
        disk_counter += 1
        file_path = os.path.join(self.engine_path, 'tree', filename)
        content = [line.strip() for line in open(file_path)]
        self.keys = [float(weight) for weight in content[0].split(',')]
        self.children = [child.strip() for child in content[1].split(',')]
        if content[2] == 'True':
            self.is_leaf = True
        else:
            self.is_leaf = False
        self.filename = filename
        if self.is_leaf and len(content) >= 4:
            self.next = content[3].strip()
        else:
            self.next = None

    def write_data_to_file(self, filename):
        global disk_counter
        disk_counter += 1
        file_path = os.path.join(self.engine_path, 'tree', filename)
        with open(file_path, 'w') as f:
            f.write(str(self.keys).strip('[]').replace("'", ""))
            f.write('\n')
            f.write(str(self.children).strip('[]').replace("'", ""))
            f.write('\n')
            f.write(str(self.is_leaf))
            f.write('\n')
            if self.is_leaf and self.next:
                f.write(str(self.next))
                f.write('\n')

    def print_content(self):
        print(self.keys)
        print(self.children)
        print(self.is_leaf)
        print(self.filename)
        if self.is_leaf:
            print(self.next)
        else:
            print('None')

    def update_node(self):
        self.write_data_to_file(self.filename)

    def split_node(self):
        global file_counter
        new_node = Node(self.engine_path)
        new_node.filename = str(file_counter)
        file_counter = file_counter + 1
        if self.is_leaf:
            new_node.is_leaf = True
            mid = len(self.keys) / 2
            mid_key = self.keys[mid]
            # Update sibling parameters
            new_node.keys = self.keys[mid:]
            new_node.children = self.children[mid:]
            # Update node parameters
            self.keys = self.keys[:mid]
            self.children = self.children[:mid]
            # Update next node pointers
            new_node.next = self.next
            self.next = new_node.filename
        else:
            new_node.is_leaf = False
            mid = len(self.keys) / 2
            mid_key = self.keys[mid]
            # Update sibling parameters
            new_node.keys = self.keys[mid + 1:]
            new_node.children = self.children[mid + 1:]
            # Update node parameters
            self.keys = self.keys[:mid]
            self.children = self.children[:mid + 1]
        self.update_node()
        new_node.update_node()
        return mid_key, new_node


class BPlusTree:
    def __init__(self, engine_path, order, root_file=-1):
        self.factor = order
        self.engine_path = engine_path
        if root_file == -1:
            self.root = Node(engine_path)
            # Initialize root_
            global file_counter
            self.root.is_leaf = True
            self.root.keys = []
            self.root.children = []
            self.root.next = None
            self.root.filename = str(file_counter)
            file_counter += 1
            self.root.update_node()
        else:
            self.root = Node(root_file)

    def search(self, key_):
        return self.tree_search(key_, self.root)

    def tree_search(self, key_, node):
        if node.is_leaf:
            return node
        else:
            if key_ < node.keys[0]:
                return self.tree_search(key_, Node(node.children[0]))
            for i in range(len(node.keys) - 1):
                if node.keys[i] <= key_ < node.keys[i + 1]:
                    return self.tree_search(key_, Node(node.children[i + 1]))
            if key_ >= node.keys[-1]:
                return self.tree_search(key_, Node(node.children[-1]))

    def tree_search_for_query(self, key_, node):
        if node.is_leaf:
            return node
        else:
            if key_ <= node.keys[0]:
                return self.tree_search_for_query(key_, Node(node.children[0]))
            for i in range(len(node.keys) - 1):
                if node.keys[i] < key_ <= node.keys[i + 1]:
                    return self.tree_search_for_query(key_, Node(node.children[i + 1]))
            if key_ > node.keys[-1]:
                return self.tree_search_for_query(key_, Node(node.children[-1]))

    def point_query(self, key_):
        all_keys = []
        all_values = []
        start_leaf = self.tree_search_for_query(key_, self.root)
        keys_, values_, next_node = self.get_data_in_key_range(key_, key_, start_leaf)
        all_keys += keys_
        all_values += values_
        while next_node:
            keys_, values_, next_node = self.get_data_in_key_range(key_, key_, Node(next_node.filename))
            all_keys += keys_
            all_values += values_
        return all_keys, all_values

    def range_query(self, key_min, key_max):
        all_keys = []
        all_values = []
        start_leaf = self.tree_search_for_query(key_min, self.root)
        keys_, values_, next_node = self.get_data_in_key_range(key_min, key_max, start_leaf)
        all_keys += keys_
        all_values += values_
        while next_node:
            keys_, values_, next_node = self.get_data_in_key_range(key_min, key_max, Node(next_node.filename))
            all_keys += keys_
            all_values += values_
        return all_keys, all_values

    def get_data_in_key_range(self, key_min, key_max, node):
        keys_ = []
        values_ = []
        for i in range(len(node.keys)):
            key_ = node.keys[i]
            if key_min <= key_ <= key_max:
                keys_.append(key_)
                values_.append(self.read_data_file(node.children[i]))
        if node.keys[-1] > key_max:
            next_node = None
        else:
            if node.next:
                next_node = Node(node.next)
            else:
                next_node = None
        return keys_, values_, next_node

    def insert(self, key_, value_):
        ans, new_filename = self.tree_insert(key_, value_, self.root)
        if ans:
            global file_counter
            new_root = Node(self.engine_path)
            new_root.is_leaf = False
            new_root.filename = str(file_counter)
            file_counter += 1
            new_root.keys = [ans]
            new_root.children = [self.root.filename, new_filename]
            new_root.update_node()
            self.root = new_root

    def tree_insert(self, key_, value_, node):
        if node.is_leaf:
            index = bisect.bisect(node.keys, key_)
            node.keys[index:index] = [key_]
            filename = self.create_data_file(value_)
            node.children[index:index] = [filename]
            node.update_node()
            if len(node.keys) <= self.factor - 1:
                return None, None
            else:
                mid_key, new_node = node.split_node()
                return mid_key, new_node.filename
        else:
            if key_ < node.keys[0]:
                ans, new_filename = self.tree_insert(key_, value_, Node(node.children[0]))
            for i in range(len(node.keys) - 1):
                if node.keys[i] <= key_ < node.keys[i + 1]:
                    ans, new_filename = self.tree_insert(key_, value_, Node(node.children[i + 1]))
            if key_ >= node.keys[-1]:
                ans, new_filename = self.tree_insert(key_, value_, Node(node.children[-1]))
        if ans:
            index = bisect.bisect(node.keys, ans)
            node.keys[index:index] = [ans]
            node.children[index + 1:index + 1] = [new_filename]
            if len(node.keys) <= self.factor - 1:
                node.update_node()
                return None, None
            else:
                mid_key, new_node = node.split_node()
                return mid_key, new_node.filename
        else:
            return None, None

    def create_data_file(self, value_):
        global file_counter
        global disk_counter
        disk_counter += 1
        filename = str(file_counter)
        file_path = 'data/' + filename
        with open(file_path, 'w') as f:
            f.write(str(value_))
        file_counter += 1
        return filename

    def read_data_file(self, filename):
        global disk_counter
        disk_counter += 1
        file_path = 'data/' + filename
        content = [line.strip() for line in open(file_path)]
        return content[0].strip()


def save_tree(root_):
    file_path = '.bPlusTree'
    with open(file_path, 'w') as f:
        f.write(root_)
        f.write('\n')
        f.write(str(file_counter))
        f.write('\n')


def write_stats():
    file_path = 'stats.txt'
    global insert_time
    global search_time
    global range_time
    insert_time = numpy.array(insert_time)
    search_time = numpy.array(search_time)
    range_time = numpy.array(range_time)
    with open(file_path, 'w') as f:
        if len(insert_time) > 0:
            f.write('Insert time statistics (In seconds)..\n')
            f.write('Min : ' + str(numpy.amin(insert_time)) + '\n')
            f.write('Max : ' + str(numpy.amax(insert_time)) + '\n')
            f.write('Mean: ' + str(numpy.mean(insert_time)) + '\n')
            f.write('STD : ' + str(numpy.std(insert_time)) + '\n')

            f.write('Insert disk statistics..\n')
            f.write('Min : ' + str(numpy.amin(insert_disk)) + '\n')
            f.write('Max : ' + str(numpy.amax(insert_disk)) + '\n')
            f.write('Mean: ' + str(numpy.mean(insert_disk)) + '\n')
            f.write('STD : ' + str(numpy.std(insert_disk)) + '\n')
            f.write('\n')
        if len(search_time) > 0:
            f.write('Point time statistics (In seconds)..\n')
            f.write('Min : ' + str(numpy.amin(search_time)) + '\n')
            f.write('Max : ' + str(numpy.amax(search_time)) + '\n')
            f.write('Mean: ' + str(numpy.mean(search_time)) + '\n')
            f.write('STD : ' + str(numpy.std(search_time)) + '\n')

            f.write('Point disk statistics..\n')
            f.write('Min : ' + str(numpy.amin(search_disk)) + '\n')
            f.write('Max : ' + str(numpy.amax(search_disk)) + '\n')
            f.write('Mean: ' + str(numpy.mean(search_disk)) + '\n')
            f.write('STD : ' + str(numpy.std(search_disk)) + '\n')
            f.write('\n')
        if len(range_time) > 0:
            f.write('Range time statistics (In seconds)..\n')
            f.write('Min : ' + str(numpy.amin(range_time)) + '\n')
            f.write('Max : ' + str(numpy.amax(range_time)) + '\n')
            f.write('Mean: ' + str(numpy.mean(range_time)) + '\n')
            f.write('STD : ' + str(numpy.std(range_time)) + '\n')

            f.write('Range disk statistics..\n')
            f.write('Min : ' + str(numpy.amin(range_disk)) + '\n')
            f.write('Max : ' + str(numpy.amax(range_disk)) + '\n')
            f.write('Mean: ' + str(numpy.mean(range_disk)) + '\n')
            f.write('STD : ' + str(numpy.std(range_disk)) + '\n')
            f.write('\n')


if __name__ == '__main__':
    # Initialize variables
    file_counter = 0  # Used to keep track of filename
    disk_counter = 0  # Used to count disk access
    start_time = 0  # Used to store start time
    end_time = 0  # Used to store end time
    insert_time = []
    search_time = []
    range_time = []
    insert_disk = []
    search_disk = []
    range_disk = []
    # Load Configuration
    configs = [line.strip() for line in open('bPlusTree.config')]
    max_num_keys = int(configs[0].strip())
    factor = max_num_keys - 1

    # Do not initialize the tree.. Load from .bPlusTree
    if os.path.isfile('.bPlusTree'):
        filepath = '.bPlusTree'
        lines = [line.strip() for line in open(filepath)]
        root = lines[0].strip()
        tree = BPlusTree(factor, root)
        file_counter = int(lines[1].strip())
    # Initialize the tree
    else:
        engine_path = "engine/"
        tree = BPlusTree(factor, engine_path)

    # Perform insert operations
    if sys.argv[1] == 'insert':
        print('Inserting Data')
        if len(sys.argv) >= 3:
            filepath = sys.argv[2]
        else:
            filepath = 'assign2_b_plus_data.txt'
        lines = [line.strip() for line in open(filepath)]
        for line in lines:
            line = line.split()
            key = float(line[0].strip())
            value = line[1].strip()
            start_time = time.clock()
            disk_counter = 0
            tree.insert(key, value)
            end_time = time.clock()
            insert_time.append(end_time - start_time)
            insert_disk.append(disk_counter)
        print('Insertions successfully completed')

    # Perform query operations
    if sys.argv[1] == 'query':
        print('Running queries')
        if len(sys.argv) >= 3:
            filepath = sys.argv[2]
        else:
            filepath = 'query_sample.txt'
        # Query
        lines = [line.strip() for line in open(filepath)]
        for line in lines:
            line = line.split()
            operation = int(line[0].strip())
            # Insertion
            if operation == 0:
                key = float(line[1].strip())
                value = line[2].strip()
                start_time = time.clock()
                disk_counter = 0
                tree.insert(key, value)
                end_time = time.clock()
                insert_time.append(end_time - start_time)
                insert_disk.append(disk_counter)
                print('insert:', key, value)
            # Point Query
            elif operation == 1:
                key = float(line[1].strip())
                start_time = time.clock()
                disk_counter = 0
                keys, values = tree.point_query(key)
                end_time = time.clock()
                search_time.append(end_time - start_time)
                search_disk.append(disk_counter)
                print('search:', key)
                if len(values) > 0:
                    print(values)
                else:
                    print('Not Found')
            # Range Query
            elif operation == 2:
                center = float(line[1].strip())
                q_range = float(line[2].strip())
                keyMin = center - q_range
                keyMax = center + q_range
                print('range:')
                eps = 0.00000001
                start_time = time.clock()
                disk_counter = 0
                keys, values = tree.range_query(keyMin - eps, keyMax + eps)
                end_time = time.clock()
                range_time.append(end_time - start_time)
                range_disk.append(disk_counter)
                if len(values) > 0:
                    zipped = zip(keys, values)
                    print(zipped)
                else:
                    print('Not Found')

    # Save tree configuration
    write_stats()
    save_tree(tree.root.filename)
