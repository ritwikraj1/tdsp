import psycopg2
import pandas as pd
import sys
import time
from collections import defaultdict
import pickle
from sqlalchemy import create_engine

# start_time = time.time()

def make_dict():
	return defaultdict(make_dict)

class make_graph:
	def __init__(self, class_id, cost):
		self.class_id			= class_id
		self.cost				= cost


# Buffalo Small: bbox=-78.8834,42.8802,-78.8158,42.9160
conn = psycopg2.connect("dbname='buffalo_routing' user='user' host='localhost' password=''")
cur = conn.cursor()

query = "select max(id) from ways_vertices_pgr;"
cur.execute(query)
row = cur.fetchall()

N_total = range(1,row[0][0]+1)

query = "select * from macro_nodes;"
cur.execute(query)
row = cur.fetchall()

macro_N = []

for i in row:
	macro_N.append(i[0])


###########MAIN CODE#############
def dijkstra(s, graph, N):

	ti = time.time()

	EA = {}
	prev_node = {}
	macro_node_encountered = {}

	for i in N:
		if i == s:
			EA.update({(s,s): 0})
			macro_node_encountered.update({(s,s): False})
		else:
			EA.update({(s,i): float('inf')})
			macro_node_encountered.update({(s,i): False})

	#print EA

	S = []
	for i in N:
		S.append(i)

	macro_entry = []

	while len(macro_entry) < 1 and len(S) > 0:
		# print count
		minimum_EA = float('inf')
		for i_min in S:
			#print s,i_min,t, EA[s,i_min,t], minimum_EA
			if EA[s,i_min] <= minimum_EA:
				minimum_EA = EA[s,i_min]
				i = i_min
		# print S
		S.remove(i)

		if_i_macro = False
		if i in macro_N:
			if_i_macro = True
			if macro_node_encountered[s,i] == False:
				macro_entry.append(i)
				#print s, i, EA[s,i]
			# print target_list
		#print S
		#print N
		for j in graph[i]:
			#print 's=',s, 'i=',i, 'j=',j, 'EA[s,j,t]=',EA[s,j,t], 'EA[s,i,t]=',EA[s,i,t], 'Aij(i,j,EA[s,i,t])=',Aij(i,j,EA[s,i,t])
			#Aij_calculation = Aij(i,j,EA[s,i,t])
			Aij_calculation = EA[s,i] + graph[i][j].cost
			if EA[s,j] >= Aij_calculation:
				EA[s,j] = Aij_calculation
				prev_node[s,j] = i
				if if_i_macro == True or macro_node_encountered[s,i] == True:
					macro_node_encountered[s,j] = True
				else:
					macro_node_encountered[s,j] = False


	tf = time.time() - ti
	print "Total time taken is %f seconds" % tf
	
	if len(macro_entry) > 0:
		if EA[s,macro_entry[0]] < float('inf'):
			return macro_entry[0], EA[s,macro_entry[0]]
		else:
			return 'nan', 'nan'
	else:
		return 'nan', 'nan'


def backward_dijkstra(t, backward_graph, N):

	ti = time.time()

	EA = {}
	next_node = {}
	macro_node_encountered = {}

	for j in N:
		if j == t:
			EA.update({(t,t): 0})
			macro_node_encountered.update({(t,t): False})
		else:
			EA.update({(j,t): float('inf')})
			macro_node_encountered.update({(j,t): False})


	#print EA

	S = []
	for j in N:
		S.append(j)

	macro_exit = []

	while len(macro_exit) < 1 and len(S) > 0:
		# print count
		minimum_EA = float('inf')
		for j_min in S:
			#print s,i_min,t, EA[s,i_min,t], minimum_EA
			if EA[j_min,t] <= minimum_EA:
				minimum_EA = EA[j_min,t]
				j = j_min
		# print S
		S.remove(j)

		if_j_macro = False
		if j in macro_N:
			if_j_macro = True
			if macro_node_encountered[j,t] == False:
				macro_exit.append(j)
				#print j, t, EA[j,t]
			# print target_list
		#print S
		#print N
		for i in backward_graph[j]:
			#print 's=',s, 'i=',i, 'j=',j, 'EA[s,j,t]=',EA[s,j,t], 'EA[s,i,t]=',EA[s,i,t], 'Aij(i,j,EA[s,i,t])=',Aij(i,j,EA[s,i,t])
			#Aij_calculation = Aij(i,j,EA[s,i,t])
			Aij_calculation = EA[j,t] + backward_graph[j][i].cost
			if EA[i,t] >= Aij_calculation:
				EA[i,t] = Aij_calculation
				next_node[i,t] = j
				if if_j_macro == True or macro_node_encountered[j,t] == True:
					macro_node_encountered[i,t] = True
				else:
					macro_node_encountered[i,t] = False


	tf = time.time() - ti
	print "Total time taken is %f seconds" % tf
	
	if len(macro_exit) > 0:
		if EA[macro_exit[0],t] < float('inf'):
			return macro_exit[0], EA[macro_exit[0],t]
		else:
			return 'nan', 'nan'
	else:
		return 'nan', 'nan'



#====================================================================================

from_macro = {}
to_macro = {}

for i in macro_N:
	from_macro[i] = [i, 0]
	to_macro[i] = [i, 0]

micro_N = list(set(N_total) - set(macro_N))
#micro_N = [28720]


count = 0
for s in micro_N:
	count += 1
	print count

	from_macro[s] = []
	to_macro[s] = []

	# 1st Quadrant:
	#query = "select source, target, class_id, cost from graph where source_lat >= (select lat from ways_vertices_pgr where id = %s) and target_lat >= (select lat from ways_vertices_pgr where id = %s) and source_lon >= (select lon from ways_vertices_pgr where id = %s) and target_lon >= (select lon from ways_vertices_pgr where id = %s);" % (s,s,s,s)
	query = "select source, target, class_id, cost from graph where source_lat >= (select lat from ways_vertices_pgr where id = %s) or target_lat >= (select lat from ways_vertices_pgr where id = %s);" % (s,s)
	cur.execute(query)
	row = cur.fetchall()

	if len(row) > 0:
		N_exec = []
		graph = defaultdict(make_dict)
		backward_graph = defaultdict(make_dict)

		for i in row:
			graph[i[0]][i[1]] = make_graph(i[2], i[3])
			backward_graph[i[0]][i[1]] = make_graph(i[2], i[3])
			N_exec.append(i[0])
			N_exec.append(i[1])

		N_exec = list(set(N_exec))

		p , q = dijkstra(s, graph, N_exec)
		from_macro[s].append(p)
		from_macro[s].append(q)

		p , q = backward_dijkstra(s, backward_graph, N_exec)
		to_macro[s].append(p)
		to_macro[s].append(q)


	else:
		from_macro[s].append('nan')
		from_macro[s].append('nan')
		to_macro[s].append('nan')
		to_macro[s].append('nan')


	# 2nd Quadrant:
	#query = "select source, target, class_id, cost from graph where source_lat >= (select lat from ways_vertices_pgr where id = %s) and target_lat >= (select lat from ways_vertices_pgr where id = %s) and source_lon <= (select lon from ways_vertices_pgr where id = %s) and target_lon <= (select lon from ways_vertices_pgr where id = %s);" % (s,s,s,s)
	query = "select source, target, class_id, cost from graph where source_lon <= (select lon from ways_vertices_pgr where id = %s) or target_lon <= (select lon from ways_vertices_pgr where id = %s);" % (s,s)
	cur.execute(query)
	row = cur.fetchall()

	if len(row) > 0:
		N_exec = []
		graph = defaultdict(make_dict)
		backward_graph = defaultdict(make_dict)

		for i in row:
			graph[i[0]][i[1]] = make_graph(i[2], i[3])
			backward_graph[i[0]][i[1]] = make_graph(i[2], i[3])
			N_exec.append(i[0])
			N_exec.append(i[1])

		N_exec = list(set(N_exec))

		p , q = dijkstra(s, graph, N_exec)
		from_macro[s].append(p)
		from_macro[s].append(q)

		p , q = backward_dijkstra(s, backward_graph, N_exec)
		to_macro[s].append(p)
		to_macro[s].append(q)


	else:
		from_macro[s].append('nan')
		from_macro[s].append('nan')
		to_macro[s].append('nan')
		to_macro[s].append('nan')


	# 3rd Quadrant:
	#query = "select source, target, class_id, cost from graph where source_lat <= (select lat from ways_vertices_pgr where id = %s) and target_lat <= (select lat from ways_vertices_pgr where id = %s) and source_lon <= (select lon from ways_vertices_pgr where id = %s) and target_lon <= (select lon from ways_vertices_pgr where id = %s);" % (s,s,s,s)
	query = "select source, target, class_id, cost from graph where source_lat <= (select lat from ways_vertices_pgr where id = %s) or target_lat <= (select lat from ways_vertices_pgr where id = %s);" % (s,s)
	cur.execute(query)
	row = cur.fetchall()

	if len(row) > 0:
		N_exec = []
		graph = defaultdict(make_dict)
		backward_graph = defaultdict(make_dict)

		for i in row:
			graph[i[0]][i[1]] = make_graph(i[2], i[3])
			backward_graph[i[0]][i[1]] = make_graph(i[2], i[3])
			N_exec.append(i[0])
			N_exec.append(i[1])

		N_exec = list(set(N_exec))

		p , q = dijkstra(s, graph, N_exec)
		from_macro[s].append(p)
		from_macro[s].append(q)

		p , q = backward_dijkstra(s, backward_graph, N_exec)
		to_macro[s].append(p)
		to_macro[s].append(q)


	else:
		from_macro[s].append('nan')
		from_macro[s].append('nan')
		to_macro[s].append('nan')
		to_macro[s].append('nan')


	# 4th Quadrant:
	#query = "select source, target, class_id, cost from graph where source_lat <= (select lat from ways_vertices_pgr where id = %s) and target_lat <= (select lat from ways_vertices_pgr where id = %s) and source_lon >= (select lon from ways_vertices_pgr where id = %s) and target_lon >= (select lon from ways_vertices_pgr where id = %s);" % (s,s,s,s)
	query = "select source, target, class_id, cost from graph where source_lon >= (select lon from ways_vertices_pgr where id = %s) or target_lon >= (select lon from ways_vertices_pgr where id = %s);" % (s,s)
	cur.execute(query)
	row = cur.fetchall()

	if len(row) > 0:
		N_exec = []
		graph = defaultdict(make_dict)
		backward_graph = defaultdict(make_dict)

		for i in row:
			graph[i[0]][i[1]] = make_graph(i[2], i[3])
			backward_graph[i[0]][i[1]] = make_graph(i[2], i[3])
			N_exec.append(i[0])
			N_exec.append(i[1])

		N_exec = list(set(N_exec))

		p , q = dijkstra(s, graph, N_exec)
		from_macro[s].append(p)
		from_macro[s].append(q)

		p , q = backward_dijkstra(s, backward_graph, N_exec)
		to_macro[s].append(p)
		to_macro[s].append(q)


	else:
		from_macro[s].append('nan')
		from_macro[s].append('nan')
		to_macro[s].append('nan')
		to_macro[s].append('nan')


conn.close()


df_from_macro = pd.DataFrame.from_dict(from_macro, orient='index', dtype=None)
df_to_macro = pd.DataFrame.from_dict(to_macro, orient='index', dtype=None)

engine = create_engine('postgresql://user:raj@localhost:5432/buffalo_routing')

df_from_macro.to_sql('start_macro_nodes', engine, if_exists = 'replace')
df_to_macro.to_sql('end_macro_nodes', engine, if_exists = 'replace')