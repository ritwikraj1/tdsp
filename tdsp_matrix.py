import psycopg2
import pandas as pd
import sys
import time
from collections import defaultdict
import numpy as np

# start_time = time.time()

def make_dict():
	return defaultdict(make_dict)

class make_graph:
	def __init__(self, class_id, cost):
		self.class_id			= class_id
		self.cost				= cost

graph = defaultdict(make_dict)

# Buffalo Small: bbox=-78.8834,42.8802,-78.8158,42.9160
conn = psycopg2.connect("dbname='buffalo_routing' user='user' host='localhost' password=''")
cur = conn.cursor()

query = "select * from macro_graph;"
cur.execute(query)
row = cur.fetchall()

N = []

for i in row:
	graph[int(i[2])][int(i[3])] = make_graph(i[1], i[4])
	N.append(int(i[2]))
	N.append(int(i[3]))

N = list(set(N))

query = "select * from start_macro_nodes;"
cur.execute(query)
row = cur.fetchall()

macro_entries = defaultdict(make_dict)

for i in row:
	if i[1] not in (None,'nan'):
		macro_entries[int(i[0])][int(i[1])] = float(i[2])
	if i[3] not in (None,'nan'):
		macro_entries[int(i[0])][int(i[3])] = float(i[4])
	if i[5] not in (None,'nan'):
		macro_entries[int(i[0])][int(i[5])] = float(i[6])
	if i[7] not in (None,'nan'):
		macro_entries[int(i[0])][int(i[7])] = float(i[8])


query = "select * from end_macro_nodes;"
cur.execute(query)
row = cur.fetchall()

macro_exits = defaultdict(make_dict)

for i in row:
	if i[1] not in (None,'nan'):
		macro_exits[int(i[0])][int(i[1])] = float(i[2])
	if i[3] not in (None,'nan'):
		macro_exits[int(i[0])][int(i[3])] = float(i[4])
	if i[5] not in (None,'nan'):
		macro_exits[int(i[0])][int(i[5])] = float(i[6])
	if i[7] not in (None,'nan'):
		macro_exits[int(i[0])][int(i[7])] = float(i[8])


def Aij(i,j,t0):

	if i == j:
		aij = t0

	elif graph[i][j].class_id in (101,103,102,104,105,106,107,108,124,109,125):
		duration = graph[i][j].cost/3600.0

		t0_hour = t0/3600.0

		if t0_hour < 7:
			aij_hour = t0_hour + duration
		elif t0_hour < 8:
			aij_hour = t0_hour + (1 + (t0_hour-7)/float(8-7))*duration
		elif t0_hour < 9:
			aij_hour = t0_hour + 2*duration
		elif t0_hour < 11:
			aij_hour = t0_hour + (2 - 0.75*(t0_hour-9)/float(11-9))*duration
		elif t0_hour < 15:
			aij_hour = t0_hour + 1.25*duration
		elif t0_hour < 17:
			aij_hour = t0_hour + (1.25 + 0.75*(t0_hour-15)/float(17-15))*duration
		elif t0_hour < 18:
			aij_hour = t0_hour + 2*duration
		elif t0_hour < 20:
			aij_hour = t0_hour + (2 - (t0_hour-18)/float(20-18))*duration
		else:
			aij_hour = t0_hour + duration

		aij = aij_hour*3600

	else:
		aij = t0 + graph[i][j].cost

	return aij


###########MAIN CODE#############
def tdsp(s,t,target_list):
	# if len(sys.argv) == 3:
	# 	s = int(sys.argv[1])
	# 	t = float(sys.argv[2])
	# else:
	# 	print "ERROR: You have provided %d input parameters" % (len(sys.argv) - 1)
	# 	quit()

	#print target_list

	target_list_copy = []
	for tlc in target_list:
		target_list_copy.append(tlc)

	#print A

	EA = {}
	prev_node = {}

	for i in N:
		if i == s:
			EA.update({(s,s,t): t})
		else:
			EA.update({(s,i,t): float('inf')})

	#print EA

	S = np.array(N)
	S_cost = float('inf')*np.ones(len(N))
	start_index, = np.where(S == s)
	S_cost[start_index[0]] = t

	count = 0

	while len(target_list_copy) != 0:
		count += 1
		#print S_cost
		min_loc = np.argmin(S_cost)
		i = S[min_loc]

		S_cost = np.delete(S_cost, min_loc)
		S = np.delete(S, min_loc)


		if i in target_list_copy:
			target_list_copy.remove(i)
			# print target_list
		#print S
		#print N
		for j in graph[i]:
			#print 's=',s, 'i=',i, 'j=',j, 'EA[s,j,t]=',EA[s,j,t], 'EA[s,i,t]=',EA[s,i,t], 'Aij(i,j,EA[s,i,t])=',Aij(i,j,EA[s,i,t])
			Aij_calculation = Aij(i,j,EA[s,i,t])
			#Aij_calculation = graph[i][j].cost
			if EA[s,j,t] > Aij_calculation:
				EA[s,j,t] = Aij_calculation
				prev_node[s,j,t] = i
				j_index, = np.where(S == j)
				#print j
				S_cost[j_index[0]] = Aij_calculation

	# route = {}

	# for i in target_list:
	# 	route[s,i,t] = []

	# for i in target_list:
	# 	print s,i,t
	# 	if i != s:
	# 		j = i
	# 		while j != s:
	# 			print prev_node[s,j,t]
	# 			route[s,i,t].append(prev_node[s,j,t])
	# 			j = prev_node[s,j,t]

	# # for i in N:
	# # 	route[s,i,t].reverse()
	# # 	if len(route[s,i,t]) > 0:
	# # 		del route[s,i,t][0]

	# for i in target_list:
	# 	route[s,i,t].reverse()
	# 	if len(route[s,i,t]) > 0:
	# 		route[s,i,t].append(i)
	# 	else:
	# 		route[s,i,t].append(s)
	# 		route[s,i,t].append(i)

	# #print EA
	# #print prev_node
	# print route

	final_EA = {}

	for i in target_list:
		final_EA[s,i,t] = EA[s,i,t]

	#print final_EA

	return final_EA


#####Main Query#####
def tdsp_data(sources, targets, start_time):

	# print 'sources = %s' % sources
	ti = time.time()
	print 'sources =', sources
	print 'targets =', targets
	print 'start hour =', start_time
	exits_near_targets = []
	for i in targets:
		for j in macro_exits[i]:
			exits_near_targets.append(j)

	exits_near_targets = list(set(exits_near_targets))

	cost_matrix = {}
	for i in sources:
		for j in macro_entries[i]:
			macro_start_time = start_time + macro_entries[i][j]
			cost_matrix.update(tdsp(j, macro_start_time, exits_near_targets))

		# print cost_matrix

	final_cost = {}

	string = "SELECT b.id AS source, c.id AS target, ST_Intersects(ST_GeomFromEWKT(CONCAT('SRID=4326;LINESTRING(',b.lon,' ',b.lat,', ',c.lon,' ',c.lat,')')),poly_map) from (select ST_Collect(the_geom) AS poly_map from macro_ways) a, (select * from ways_vertices_pgr where id in (%s)) b, (select * from ways_vertices_pgr where id in (%s)) c;" % (str(sources)[1:-1],str(targets)[1:-1])
	cur.execute(string)
	intersection_row = cur.fetchall()

	for k in intersection_row:
		i = int(k[0])
		j = int(k[1])
		intersection = bool(k[2])

		if intersection == True:
			final_cost[i,j,start_time] = float('inf')
			for p in macro_entries[i]:
				for q in macro_exits[j]:
					curr_cost = cost_matrix[p,q,start_time + macro_entries[i][p]] + macro_exits[j][q]

					if final_cost[i,j,start_time] > curr_cost:
						final_cost[i,j,start_time] = curr_cost

		else:
			cur.execute("""select * from pgr_dijkstracost('select gid as id, source, target, cost_s as cost, reverse_cost_s as reverse_cost from ways', %s, %s, directed := true)""",(i,j))
			row = cur.fetchone()
			if row is None:
				final_cost[i,j,start_time] = float('inf')
			else:
				final_cost[i,j,start_time] = float(row[2])


	tf = time.time() - ti
	print "Total time taken is %f seconds" % tf

	return final_cost
	# print cost_matrix

# conn.close()


source_nodes = input("List of source nodes:")
print source_nodes
target_nodes = input("List of target nodes:")
print target_nodes
depart_at = input("Depart at [in seconds]:")

x = tdsp_data(source_nodes,target_nodes,depart_at)

print x

#sources = [12, 524, 1351, 63, 435, 345, 366, 757, 673, 2]
#targets = [13, 525, 1352, 64, 436, 346, 367, 758, 674, 1]
#start hour = 36300