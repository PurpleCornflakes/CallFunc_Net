import re
import networkx as nx 
import glob

# nodes' attributes: name, type
# 3 types of nodes: 'def_file', 'func', 'call_file'


def file2str(fpath):
	with open(fpath, 'r') as myfile:
		script = myfile.read().replace('\n', '')
	file_name = fpath[len(base):]
	return file_name, script


class CallFunc_Net(object):
	def __init__(self, base):
		self.graph = nx.DiGraph()
		# find files in the base directory recursively
		self.fpaths = glob.glob(base + '**/*.py', recursive = True)
		self.funcs = []
		self.node_dict = {}
		self.num_gen = None

	def gen_node_num(self):
		num = 0
		while True:
			yield num
			num += 1

	def create_num_gen(self):
		self.num_gen = self.gen_node_num()

	def add_DefFiles(self):
		for fpath in self.fpaths:
			node_num = next(self.num_gen)
			file_name = fpath[len(base):]
			self.graph.add_node(node_num, name = file_name, type = 'def_file')
			self.node_dict[file_name] = node_num

	# use regular expression to find funcs defined in script
	def find_add_DefFuncs(self, fpath):
		file_name, script = file2str(fpath)
		func_list = re.findall(pattern = r'def\s[\w\W]*?\(', string = script)
		for func in func_list:
			func_name = func[4:-1]
			self.funcs.append(func_name)
			func_node_num = next(self.num_gen)
			self.graph.add_node(func_node_num, name = func_name, type = 'func')
			self.node_dict[func_name] = func_node_num
			self.graph.add_edge(self.node_dict[func_name], self.node_dict[file_name])

	def find_add_CallFuncs(self, fpath):
		file_name, script = file2str(fpath)
		node_num = next(self.num_gen)
		self.graph.add_node(node_num, name = file_name, type = 'call_file')
		self.node_dict[file_name] = node_num
		for func_name in self.funcs:
			flag = script.find(func_name)
			if flag > 0:
				self.graph.add_edge(self.node_dict[file_name], self.node_dict[func_name])

	def create_graph(self):
		self.create_num_gen()
		self.add_DefFiles()
		for fpath in self.fpaths:
			self.find_add_DefFuncs(fpath)
		for fpath in self.fpaths:
			self.find_add_CallFuncs(fpath)

	def draw_graph(self):
		pass


if __name__ == '__main__':
	base = "/Users/qinglingzhang/IDNNs/idnns/"
	Net = CallFunc_Net(base = base)

	Net.create_graph()
	print(Net.graph.number_of_edges())
	nx.write_gml(Net.graph, "call_net.gml")
	# print(Net.graph.edges)
	colormap = {'def_file': 'r', 'func': 'b', 'call_file': 'k'}

