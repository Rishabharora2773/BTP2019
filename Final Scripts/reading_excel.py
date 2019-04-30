import pandas as pd
import UseCaseClass

excel_file = ''
df_len = 0

def countNan(df,x,len):	
	cnt = 0
	i = x+1	
	while (i < len and str(df.loc[i][0]) == 'nan'):		
		cnt += 1
		i += 1

	return cnt	

def getPreConditions(UC,df,start,end):
	for i in range(start,end,1):
		UC.pre_condition[df.loc[i][1]] = df.loc[i][2] if str(df.loc[i][2]) != 'nan' else ''


def getBasicFlow(UC,df,start,end):
	for i in range(start,end,1):
		bf = UseCaseClass.BasicFlow()
		UC.basic_flow[df.loc[i][1]] = bf
		bf.event = df.loc[i][2] if str(df.loc[i][2]) != 'nan' else ''
		bf.condition = df.loc[i][3] if str(df.loc[i][3]) != 'nan' else ''
		bf.action = df.loc[i][4] if str(df.loc[i][4]) != 'nan' else ''
		bf.associated_sub_flow = str(df.loc[i][5]).split(",") if str(df.loc[i][5] != 'nan') else []
		bf.associated_alternate_flow_origin = str(df.loc[i][6]).split(",") if str(df.loc[i][6] != 'nan') else []

def getSubFlow(UC,df,start,end):
	for i in range(start,end,1):
		sf = UseCaseClass.SubFlow()
		UC.sub_flow[df.loc[i][1]] = sf
		sf.description = df.loc[i][2] if str(df.loc[i][2]) != 'nan' else ''
		sf.action = df.loc[i][3] if str(df.loc[i][3]) != 'nan' else ''
		sf.associated_flow = str(df.loc[i][4]).split(",") if str(df.loc[i][4] != 'nan') else []		 

def getAlternateFlow(UC,df,start,end):
	for i in range(start,end,1):
		af = UseCaseClass.AlternateFlow()
		UC.alternate_flow[df.loc[i][1]] = af
		af.description = df.loc[i][2] if str(df.loc[i][2]) != 'nan' else ''
		af.action = df.loc[i][3] if str(df.loc[i][3]) != 'nan' else ''
		af.associated_flow_join = str(df.loc[i][4]).split(",") if str(df.loc[i][4] != 'nan') else []		

def getPostConditions(UC,df,start,end):
	for i in range(start,end,1):
		pc = UseCaseClass.SubFlow()
		UC.post_conditions[df.loc[i][1]] = pc
		pc.description = df.loc[i][2] if str(df.loc[i][2]) != 'nan' else ''
		pc.action = df.loc[i][3] if str(df.loc[i][3]) != 'nan' else ''
		pc.associated_flow = str(df.loc[i][4]).split(",") if str(df.loc[i][4] != 'nan') else []		 

def getUC(UC,text):
	uc_list = text.split(",")
	for case in uc_list:
		use_case = case.split(" ")
		if use_case[0] == 'Include':
			use_case.pop(0)
			UC.include_UC.append(str(''.join(str(use_case).strip())).lower())
		else:
			use_case.pop(0)
			UC.extend_UC.append(str(''.join(str(use_case).strip())).lower())

def reading_excel_main():
	UC = UseCaseClass.UseCase()
	df = pd.read_excel(excel_file)
	df_len = df.shape[0]
	for row in df.itertuples():
	    if row[1] == 'Use case name':
	    	if(str(row[2]) == 'nan'):
	    		continue
	        UC.name = row[2]
	    elif (row[1] == 'Primary Actor' or row[1] == 'Secondary Actor'):
	    	if(str(row[2]) == 'nan'):
	    		continue
	    	UC.components.extend(row[2].split(","))	    	
	    elif (row[1] == 'Dependency'):
	    	if(str(row[2]) == 'nan'):
	    		continue
	        getUC(UC,row[2])
	    elif (row[1] == 'Pre-conditions'):
	    	pr_rows = countNan(df,row[0],df_len)        
	    	getPreConditions(UC,df,row[0]+1,row[0]+pr_rows+1)
	        #UC.pre_condition = row[2]
	    elif (row[1] == 'Basic Flow'):
	        bf_rows = countNan(df,row[0],df_len)
	        getBasicFlow(UC,df,row[0]+1,row[0]+bf_rows+1)		
	    elif (row[1] == 'Sub Flow'):
	        sf_rows = countNan(df,row[0],df_len)
	        getSubFlow(UC,df,row[0]+1,row[0]+sf_rows+1)
	    elif (row[1] == 'Alternate Flow'):
	        af_rows = countNan(df,row[0],df_len)
	        getAlternateFlow(UC,df,row[0]+1,row[0]+af_rows+1)
	    elif (row[1] == 'Post-Conditions'):
	        pc_rows = countNan(df,row[0],df_len)        
	        getPostConditions(UC,df,row[0]+1,row[0]+pc_rows+1)
	        #UC.post_conditions = row[2]
	        
	return UC