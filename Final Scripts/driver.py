import automate_UCM as au
import nlpTest as nt
import reading_excel as re
import system_overview as so


names = ['Shopping_Cart.xlsx']

itr = 1
UC_name_map = {}
System_UC_obj = []
System_nt_obj = []
System_comp_assigned = {}
System_components_map = {}
System_af_lengths = {}
System_resp_map = {}
'''
temp = nt.getResponsibility(u'User select the option Human speed detection from Recorded video')
print('comp',temp[0])
print('resp',temp[1])
'''

for n in names:
	re.excel_file = n
	uc_name = n[:n.find('.')]
	print('name',uc_name)
	UC_name_map[uc_name] = itr
	UC_obj = re.reading_excel_main()

	nt_obj,comp_assigned,components_map,af_lengths = nt.nlpTest_main(UC_obj,itr)
	#print(comp_assigned,"\n",components_map,'\n',af_lengths,'\n',nt_obj.af_responsibility,'\n',nt_obj.bf_responsibility)
	au.automate_UCM_main(UC_obj,nt_obj,comp_assigned,components_map,af_lengths,uc_name,itr)
	
	System_UC_obj.append(UC_obj)
	System_nt_obj.append(nt_obj)
	System_af_lengths.update(af_lengths)
	System_comp_assigned.update(comp_assigned)
	System_resp_map.update(nt_obj.af_responsibility)
	System_resp_map.update(nt_obj.bf_responsibility)

	#print("system",System_components_map)
	#print("uc",components_map)
	for comp in components_map.keys():
		resp_list = []
		print('driver comp',comp)
		if comp in System_components_map.keys():
			#print("Adasd")
			#print('driver system map',System_components_map[comp])
			resp_list = System_components_map[comp]
		resp_list.extend(components_map[comp])
		System_components_map[comp] = resp_list
		#print("system compoent map",System_components_map)

	itr = itr + 1


'''
print(System_af_lengths)
print(System_components_map)
print(System_comp_assigned)
print(System_resp_map)
'''
#so.system_overview_main(System_nt_obj,System_components_map,System_resp_map,System_comp_assigned,System_UC_obj,System_af_lengths,UC_name_map)
