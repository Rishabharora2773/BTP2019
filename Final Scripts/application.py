from flask import Flask,render_template,request,send_from_directory
from werkzeug import secure_filename
import automate_UCM as au
import nlpTest as nt
import os, shutil
import reading_excel as re
import system_overview as so
from PIL import Image
from graphviz import Source,render

application = app = Flask(__name__,static_url_path='/static')

def moveFiles(image_names):
	src = app.root_path +'/'
	dest = src + "static/"
	print("src",src,"dest",dest)
	for image in image_names:
		shutil.move(src+image,dest+image) 

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    #print("in headre")
    r.headers["Cache-Control"] = "no-store"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.cache_control.max_age = 300
    r.cache_control.public = True
    dir_name = app.root_path
    test = os.listdir(dir_name)
    for item in test:
        if(item.endswith(".xlsx") or item.endswith(".dot")):
            os.remove(os.path.join(dir_name,item))
    return r


@app.route('/index')
def index():
	return 'index page'

@app.route('/uploaded' , methods = ['GET','POST'])
def uploader():
	itr = 1
	UC_name_map = {}
	System_UC_obj = []
	System_nt_obj = []
	System_comp_assigned = {}
	System_components_map = {}
	System_af_lengths = {}
	System_resp_map = {}
	image_names = []

	if request.method == 'POST':
		f = request.files.getlist("file[]")
		for file in f:
			file.save(secure_filename(file.filename))
			file_name = file.filename
			re.excel_file = file.filename
			uc_name = file_name[:file_name.find('.')]
			image_names.append(uc_name+".dot.png")
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
		"""
		img = Image.open("system_overview.dot.png")
		img.show()
		"""
		
	image_names.append("system_overview.dot.png")
	moveFiles(image_names)
	return render_template("gallery2.html",image_names=image_names)
	#print(app.root_path)
	#return send_from_directory(app.root_path,"Apply_For_Financing.dot.png",as_attachment = True)	
	#return 'File Uploaded Successfully!'

@app.route('/')
def upload():
	return render_template('index.html')

if __name__ == '__main__':
	#app.run(host='0.0.0.0',port=80)
	app.run(debug = True)