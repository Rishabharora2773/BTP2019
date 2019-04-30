import nlpTest as nt
from PIL import Image
import reading_excel as re
from graphviz import Source,render


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


def precondition(UC_1,itr):
	string = ''
	for id in UC_1.precondition.keys():
		string = string + "\t%s[shape=point xlabel=\"%s\" style=filled]\n" %(id,UC_1.precondition[id])
	
	string = string + "\t%sstart[shape=point xlabel=\"%s\" style=filled]\n" %('UC'+str(itr)+'_','')

	for id in UC_1.precondition.keys():
		string = string + "\t%s -> %s;\n"%(id, 'UC'+str(itr)+'_start')
	return string

def postcondition(UC_1,itr):
	string = ''
	for id in UC_1.postcondition.keys():
		string = string + "\t%s[shape=point xlabel=\"%s\" style=filled]\n" %(id,UC_1.postcondition[id])

	return string

def createResponsibility(label,node_id,f):
	node_ep = "ep"+str(node_id)
	node_resp = str(node_id)
	resp = "\t\t%s[shape=box,style=invisible, fillcolor=white, color=blue, label=<<TABLE border=\"0\" cellborder=\"0\"><TR><TD width=\"20\" height=\"20\" fixedsize=\"true\" rowspan=\"1\"><IMG SRC=\"responsibilty.gif\" scale=\"true\"/></TD> <TD rowspan=\"1\"><BR/><BR/>%s</TD> </TR></TABLE>>]\n" %(node_resp,label)
	ep = "\t\t%s[shape=point style=unfilled fillcolor=white]\n"%(node_ep)
	f.write(ep)
	f.write(resp)

def createStaticStub(label,node_id,f):
	colon = label.find(':')
	label = label[colon+2:]
	node_ep = "ep"+str(node_id)
	ep = "\t\t%s[shape=point style=unfilled fillcolor=white]\n"%(node_ep)
	node_stub = str(node_id)
	stub = "\t\t%s[shape=diamond xlabel=\"%s\" style=unfilled fillcolor=white]\n"%(node_stub,label)
	f.write(ep)
	f.write(stub)

def createDynamicStub(label,node_id):
	colon = label.find(':')
	label = label[colon+2:]
	node_ep = "ep"+str(node_id)
	ep = "\t\t%s[shape=point style=unfilled fillcolor=white]\n"%(node_ep)
	node_stub = str(node_id)
	stub = "\t\t%s[shape=diamond xlabel=\"%s\" style=dotted fillcolor=white]\n"%(node_stub,label)
	f.write(ep)
	f.write(stub)

def createClusters(id,component,comp_map,af_nlp,bf_nlp,f):
	f.write("\tsubgraph cluster_%s {\n"%(str(id)))
	f.write("\t\tstyle=filled;\n\t\tcolor=%s;\n\t\tlabel=\"%s\";\n"%(colours[id],component))
	if(component in comp_map):
		for node_id in comp_map[component]:
			flow = str(node_id).find('_') + 1
			flow = node_id[flow]
			#print('flow',flow)
			if flow == 'A':
				if str(af_nlp[node_id]).find("Include UC") != -1:
					createStaticStub(af_nlp[node_id][0],node_id,f)
				elif str(af_nlp[node_id]).find("Exclude UC") != -1:
					createDynamicStub(af_nlp[node_id],node_id)
				else:
					createResponsibility(af_nlp[node_id],node_id,f)
			else:
				if str(bf_nlp[node_id]).find("Include UC") != -1:
					createStaticStub(bf_nlp[node_id],node_id,f)
				elif str(bf_nlp[node_id]).find("Exclude UC") != -1:
					createDynamicStub(bf_nlp[node_id],node_id)
				else:
					createResponsibility(bf_nlp[node_id],node_id,f)
	f.write("\t}\n\n")

def createBasicFlowEdges(bf_nlp,f,itr):
	prevnode = 'UC'+str(itr)+'_start'
	for node_id in sorted(bf_nlp, key=cmp_to_key(mycomp)):
		node_ep = "ep"+str(node_id)
		node_resp = str(node_id)
		f.write("\t%s -> %s;\n"%(prevnode,node_ep))
		f.write("\t%s -> %s;\n"%(node_ep,node_resp))
		prevnode = node_resp

	post_node = 'UC'+str(itr)+'_Po1'
	f.write("\t%s -> %s;\n"%(prevnode,post_node))

def createAlternateFlowEdges(af_lengths,f):
	for key_id in sorted(af_lengths):
		prevnode = "ep"+str(key_id)+"_"+str(1)
		for i in range(1,af_lengths[key_id]+1,1):
			node_id = str(key_id)+"_"+str(i)
			node_ep = "ep"+str(node_id)
			node_resp = str(node_id)
			if prevnode != node_ep:
				f.write("\t%s -> %s;\n"%(prevnode,node_ep))
			f.write("\t%s -> %s;\n"%(node_ep,node_resp))
			prevnode = node_resp			

def createAlternateFlowOrigin(bf_obj,af_obj,itr,f):
	sorted_list = sorted(bf_obj.keys())
	for key in sorted_list:
		temp_key = ''
		fromnode = ''
		if sorted_list.index(key) != (len(sorted_list) - 1):
			ind = int(key[1]) + 1
			temp_key = key[0] + str(ind)
			fromnode = "epUC"+str(itr)+'_'+str(temp_key)
		else :
			temp_key = 'Po1'
			fromnode = "UC"+str(itr)+'_'+str(temp_key)
		#print('key',key,'temp key ',temp_key)
		fromnode = "epUC"+str(itr)+'_'+str(temp_key)

		for val in bf_obj[key].associated_alternate_flow_origin:
			if val == 'nan':
				break
			to = "epUC"+str(itr)+'_'+str(val)+"_1"
			label = af_obj[val].description
			#print('fromnode',fromnode,'to',to)
			f.write("\t%s->%s[label=\"[%s]\"]\n"%(fromnode,to,label))

def createUnassignedNodes(comp_assigned,af_nlp,bf_nlp,f):
	id_list = []
	for id in comp_assigned.keys():
		if comp_assigned[id] == False:
			id_list.append(id)
	for id in id_list:
		if id in af_nlp.keys():
			print("af resp",af_nlp[id])
			if str(af_nlp[id]).find("Include UC") != -1:
				createStaticStub(af_nlp[id],id,f)
			elif str(af_nlp[id]).find("Exclude UC") != -1:
				createDynamicStub(af_nlp[id],id)
			else:
				createResponsibility(af_nlp[id],id,f)
		else:
			if str(bf_nlp[id]).find("Include UC") != -1:
				createStaticStub(bf_nlp[id],id,f)
			elif str(bf_nlp[id]).find("Exclude UC") != -1:
				createDynamicStub(bf_nlp[id],id)
			else:
				createResponsibility(bf_nlp[id],id,f)

def createPostConditionEdges(af_lengths,UC,UC_1,itr,f):
	for map_id in UC.post_conditions.keys():
		val = UC.post_conditions[map_id]
		to_id = 'UC'+str(itr)+'_'+str(map_id)
		for id in val.associated_flow:
			from_id = 'UC'+str(itr)+'_'+str(id)
			if(str(id)[0] == 'A'):
				len = af_lengths[from_id]
				from_id = from_id + '_' + str(len)
			f.write("\t%s -> %s;\n"%(from_id,to_id))


def createAlternateFlowJoin(af_obj,itr,af_lengths,f):
	for id in af_obj.keys():
		from_id = 'UC'+str(itr)+'_'+str(id)+'_'+str(af_lengths['UC'+str(itr)+'_'+str(id)])
		to_id = 'UC'+str(itr)+'_'+str(af_obj[id].associated_flow_join[0])
		if (str(af_obj[id].associated_flow_join[0])[0] == 'M' or str(af_obj[id].associated_flow_join[0])[0] == 'A'):
			to_id = 'ep' + to_id
		f.write("\t%s -> %s;\n"%(from_id,to_id))

total_components = 0
pre = ''
colours = ['cadetblue1','chartreuse2','yellow','lightpink','mediumorchid1','crimson','firebrick2','greenyellow']

def automate_UCM_main(UC,UC_1,comp_assigned_p,components_map_p,af_lengths_p,name,itr):	
	bf_obj = UC.basic_flow
	af_obj = UC.alternate_flow 
	comp_map = components_map_p
	comp_assigned = comp_assigned_p
	af_lengths = af_lengths_p
	total_components = len(UC.components)
	af_nlp = UC_1.af_responsibility
	bf_nlp = UC_1.bf_responsibility

	f = open(name+".dot","w")

	f.write("digraph G{\n")
	f.write("\tlabel="+name+"\n")
	f.write("\tforcelabels=true\n\tedge[headclip=false, tailclip=false]\n\trankdir=LR\n")
	f.write(precondition(UC_1,itr))
	f.write(postcondition(UC_1,itr))
	cluster_itr = 0
	for ids in comp_map.keys():
		createClusters(cluster_itr,ids,comp_map,af_nlp,bf_nlp,f)
		cluster_itr = cluster_itr+1

	createUnassignedNodes(comp_assigned,af_nlp,bf_nlp,f)
	createBasicFlowEdges(bf_nlp,f,itr)
	createAlternateFlowEdges(af_lengths,f)
	createAlternateFlowOrigin(bf_obj,af_obj,itr,f)
	createAlternateFlowJoin(af_obj,itr,af_lengths,f)
	#createPostConditionEdges(af_lengths,UC,UC_1,itr,f)

	f.write("}")
	f.close()
	render('dot','png',name+".dot")
	img = Image.open(name+".dot.png")
	img.show()