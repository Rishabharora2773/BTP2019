import automate_UCM as au

def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0  
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K


def mycomp(x,y):
    if len(x) != len(y):
        return len(x)-len(y)
    if x < y :
        return -1
    elif x > y:
        return 1
    return 0

def preConditions(sys_nt_obj,f):
	itr = 1
	string = ''
	for nt_obj in sys_nt_obj:
		string = string + au.precondition(nt_obj,itr)
		itr = itr + 1

	return string

def postConditions(sys_nt_obj,f):
	itr = 1
	string = ''
	for nt_obj in sys_nt_obj:
		string = string + au.postcondition(nt_obj,itr)
		itr = itr + 1

	return string

def createClusters(id,component,sys_comp_map,sys_resp_map,f,bindings,uc_name_map):
	#af nlp and bf nlp create
	f.write("\tsubgraph cluster_%s {\n"%(str(id)))
	f.write("\t\tstyle=filled;\n\t\tcolor=%s;\n\t\tlabel=\"%s\";\n"%(colours[id],component))
	if(component in sys_comp_map):
		for node_id in sys_comp_map[component]:
			if str(sys_resp_map[node_id]).find("Include UC") != -1 or str(sys_resp_map[node_id]).find("Exclude UC") != -1:
				uc_name = sys_resp_map[sys_resp_map.find(':')+2:]
				if uc_name in uc_name_map:
					bindings[node_id] = uc_name_map[uc_name]
				else:
					print("NO such use case mentioned in above use cases.")
					node_ep = "ep"+str(node_id)
					ep = "\t\t%s[shape=point style=unfilled fillcolor=white]\n"%(node_ep)
					node_stub = str(node_id)
					stub = "\t\t%s[shape=diamond xlabel=\"%s\" style=unfilled fillcolor=white]\n"%(node_stub,uc_name)
					f.write(ep)
					f.write(stub)
			else:
				au.createResponsibility(sys_resp_map[node_id],node_id,f)
	
	f.write("\t}\n\n")

def createUnassignedNodes(comp_assigned,sys_resp_map,f,bindings,uc_name_map):
	id_list = []
	for id in comp_assigned.keys():
		if comp_assigned[id] == False:
			id_list.append(id)
	for id in id_list:
		if str(sys_resp_map[id]).find("Include UC") != -1 or str(sys_resp_map[id]).find("Exclude UC") != -1:
			uc_name = str(sys_resp_map[id])[str(sys_resp_map[id]).find(':')+2:]
			if uc_name in uc_name_map:
				bindings[id] = uc_name_map[uc_name]
				node_ep = "ep"+str(id)
				ep = "\t\t%s[shape=point style=unfilled fillcolor=white]\n"%(node_ep)
				f.write(ep)
			else:
				print("NO %s usecase mentioned in above use cases." %uc_name)
				print('uc map ',uc_name_map)
				node_ep = "ep"+str(id)
				ep = "\t\t%s[shape=point style=unfilled fillcolor=white]\n"%(node_ep)
				node_stub = str(id)
				stub = "\t\t%s[shape=diamond xlabel=\"%s\" style=unfilled fillcolor=white]\n"%(node_stub,uc_name)
				f.write(ep)
				f.write(stub)
		else:
			au.createResponsibility(sys_resp_map[id],id,f)

def createBasicFlowEdges(sys_nt_obj,f,bindings):
	itr = 1
	for val in sys_nt_obj:
		bf_nlp = val.bf_responsibility
		prevnode = 'UC'+str(itr)+'_start'
		for node_id in sorted(bf_nlp, key=cmp_to_key(mycomp)):
			node_ep = "ep"+str(node_id)
			node_resp = str(node_id)
			if node_id in bindings.keys():
				node_resp = 'UC'+str(bindings[node_id])+'_start'
			f.write("\t%s -> %s;\n"%(prevnode,node_ep))
			f.write("\t%s -> %s;\n"%(node_ep,node_resp))
			prevnode = node_resp
			if node_id in bindings.keys():
				prevnode = 'UC'+str(bindings[node_id])+'_Po1'

		post_node = 'UC'+str(itr)+'_Po1'
		f.write("\t%s -> %s;\n"%(prevnode,post_node))
		itr = itr + 1

def createAlternateFlowEdges(sys_nt_obj,f,bindings,sys_af_lengths):
	itr = 1
	for val in sys_nt_obj:
		af_nlp = val.af_responsibility
		af_lengths = {}
		for key in sys_af_lengths:
			if key.startswith('UC'+str(itr)):
				af_lengths[key] = sys_af_lengths[key]

		for key_id in sorted(af_lengths):
			prevnode = "ep"+str(key_id)+'_1'
			for i in range(1,af_lengths[key_id]+1,1):
				node_id = str(key_id)+"_"+str(i)
				node_ep = "ep"+str(node_id)
				node_resp = str(node_id)
				if node_id in bindings.keys():
					node_resp = 'UC'+str(bindings[node_id])+'_start'

				if prevnode != node_ep:
					f.write("\t%s -> %s;\n"%(prevnode,node_ep))
				f.write("\t%s -> %s;\n"%(node_ep,node_resp))
				prevnode = node_resp
				if node_id in bindings.keys():
					prevnode = 'UC'+str(bindings[node_id])+'_Po1'
		itr = itr + 1 

def createAlternateFlowOrigin(sys_UC_obj,f):
	itr = 1
	for val in sys_UC_obj:
		bf_obj = val.basic_flow
		af_obj = val.alternate_flow
		au.createAlternateFlowOrigin(bf_obj,af_obj,itr,f)
		'''
		for key in bf_obj:
			fromnode = "epUC"+str(itr)+'_'+str(key)
			print("system from node",fromnode)
			for val in bf_obj[key].associated_alternate_flow_origin:
				if val == 'nan':
					break
				to = "epUC"+str(itr)+'_'+str(val)+"_1"
				label = af_obj[val].description
				f.write("\t%s->%s[label=\"[%s]\"]\n"%(fromnode,to,label))
		'''
		itr = itr + 1

def createAlternateFlowJoin(sys_UC_obj,sys_af_lengths,f):
	itr = 1
	for val in sys_UC_obj:
		af_obj = val.alternate_flow
		for id in af_obj.keys():
			from_id = 'UC'+str(itr)+'_'+str(id)+'_'+str(sys_af_lengths['UC'+str(itr)+'_'+str(id)])
			to_id = 'UC'+str(itr)+'_'+str(af_obj[id].associated_flow_join[0])
			if (str(af_obj[id].associated_flow_join[0])[0] == 'M' or str(af_obj[id].associated_flow_join[0])[0] == 'A'):
				to_id = 'ep' + to_id
			f.write("\t%s -> %s;\n"%(from_id,to_id))
		itr = itr + 1


colours = ['cadetblue1','chartreuse2','yellow','lightpink','mediumorchid1','crimson','firebrick2','greenyellow','lawngreen','olivedrab','hotpink','indigo']


def system_overview_main(sys_nt_obj,sys_comp_map,sys_resp_map,sys_comp_assigned,sys_UC_obj,sys_af_lengths,uc_name_map):
	f = open("system_overview.dot","w")
	f.write("digraph G{\n")
	f.write("\tlabel=system_overview\n")
	f.write("\tforcelabels=true\n\tedge[headclip=false, tailclip=false]\n\trankdir=LR\n")
	f.write(preConditions(sys_nt_obj,f))
	f.write(postConditions(sys_nt_obj,f))
	bindings = {}
	cluster_itr = 0
	for ids in sys_comp_map.keys():
		createClusters(cluster_itr,ids,sys_comp_map,sys_resp_map,f,bindings,uc_name_map)
		cluster_itr = cluster_itr+1

	createUnassignedNodes(sys_comp_assigned,sys_resp_map,f,bindings,uc_name_map)
	createBasicFlowEdges(sys_nt_obj,f,bindings)
	createAlternateFlowEdges(sys_nt_obj,f,bindings,sys_af_lengths)
	createAlternateFlowOrigin(sys_UC_obj,f)
	createAlternateFlowJoin(sys_UC_obj,sys_af_lengths,f)

	f.write("}")
	f.close()