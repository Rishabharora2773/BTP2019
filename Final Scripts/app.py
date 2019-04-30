from flask import Flask,render_template,request
from werkzeug import secure_filename
import automate_UCM as au
import nlpTest as nt
import reading_excel as re
import system_overview as so
from PIL import Image
from graphviz import Source,render

app = Flask(__name__,static_url_path='/static')

@app.route('/index')
def index():
	return 'index page'

@app.route('/uploader' , methods = ['GET','POST'])
def uploader():
	itr = 1
	UC_name_map = {}
	System_UC_obj = []
	System_nt_obj = []
	System_comp_assigned = {}
	System_components_map = {}
	System_af_lengths = {}
	System_resp_map = {}

	if request.method == 'POST':
		f = request.files.getlist("file[]")
		for file in f:
			file.save(secure_filename(file.filename))
			file_name = file.filename
			re.excel_file = file.filename
			uc_name = file_name[:file_name.find('.')]

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

			for comp in components_map.keys():
				resp_list = []
				if comp in System_components_map.keys():
					resp_list = System_components_map[comp]
				resp_list.extend(components_map[comp])
				System_components_map[comp] = resp_list
			
			itr = itr + 1
		
		so.system_overview_main(System_nt_obj,System_components_map,System_resp_map,System_comp_assigned,System_UC_obj,System_af_lengths,UC_name_map)
		render('dot','png',"system_overview.dot")
		img = Image.open("system_overview.dot.png")
		img.show()
		
	return 'File Uploaded Successfully!'

@app.route('/upload')
def upload():
	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True)