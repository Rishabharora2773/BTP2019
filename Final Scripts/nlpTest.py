import spacy
from spacy.symbols import nsubj, VERB
import UseCaseClass

nlp = spacy.load('en_core_web_sm')
stop_words = nlp.Defaults.stop_words
stop_words -= {'with'}

class UseCaseNLP:

    def __init__(self):
        self.bf_responsibility = {}
        self.af_responsibility = {}
        self.precondition = {}
        self.postcondition = {}


def findComponent(sentence):
    for comp in UC.components:
        if str(sentence).find(comp) != -1:
            return comp
    return ''

def getResponsibility(text):
    #print("get resp text",text)
    doc = nlp(str(text))
    '''
    doc = [word.text for word in doc if not word.is_stop]
    p_text = ''
    for word in doc:
        p_text = p_text + ' ' + word
        
    doc = nlp(unicode(p_text))
    '''
    comp = str(doc[0])
    resp = str(doc[1:])
    for chunk in doc.noun_chunks:
        if chunk.root.dep_ == 'nsubj':
            comp = chunk
        if chunk.root.dep_ == 'dobj':
            resp = str(chunk.root.head.text) + ' ' + str(chunk.text)

    #print('comp ',comp,'resp ',resp)
    return str(comp),str(resp)

def getBasicFlowResponsibility(UC,UC_1,components_map,af_lengths,comp_assigned,uc_id):
    for id in UC.basic_flow.keys():
        #print('str id ',id)
        key_id = "UC"+str(uc_id)+"_"+str(id)
        resp = UC.basic_flow[id]
        event = str(resp.event)
        if(event == ''):
            UC_1.bf_responsibility[key_id] = 'No responsibility found'
            comp_assigned[key_id] = False
            continue

        doc = nlp(resp.event)

        if event.find("Include UC")!=-1 or event.find("Extend UC")!=-1:
            UC_1.bf_responsibility[key_id] = event
            comp_assigned[key_id] = False
            continue

        fi = event.find("'")
        si = event[fi+1:].find("'")
        for possible_verb in doc:
            if str(possible_verb.pos_) == 'VERB':
                child = list(possible_verb.children)
                resp_list = []
                if fi == -1 or si == -1:
                    ans = str(possible_verb)
                    
                    if len(child)>=2:
                        if child[0].dep_ != 'dobj' and child[1].dep_ != 'nsubj':
                            continue
                        ans = ans + " " + str(child[1])                        
                        if str(child[0]) in components_map: 
                            resp_list = components_map[str(child[0])]
                        else:
                            components_map[str(child[0])] = resp_list
                        resp_list.append(key_id)
                        components_map[str(child[0])] = resp_list
                        UC_1.bf_responsibility[key_id] = ans
                        comp_assigned[key_id] = True
                        break
                else:
                    ans = str(possible_verb) + " "+ event[fi+1:fi+si+1]
                    UC_1.bf_responsibility[key_id] = ans
                    comp_assigned[key_id] = True
                    comp = str(str(event).split(" ")[0])                    
                    if comp in components_map: 
                        resp_list = components_map[comp]
                    else:
                        components_map[comp] = resp_list
                    resp_list.append(key_id)
                    components_map[comp] = resp_list
                    break  


        if key_id not in  UC_1.bf_responsibility.keys() :
            comp_resp = getResponsibility(resp.event)
            comp_assigned[key_id] = True
            UC_1.bf_responsibility[key_id] = comp_resp[1]
            resp_list = []
            if comp_resp[0] in components_map: 
                resp_list = components_map[comp_resp[0]]
            else:
                components_map[comp_resp[0]] = resp_list
            resp_list.append(key_id)
            components_map[comp_resp[0]] = resp_list            



def getAlternateFlowResponsibility(UC,UC_1,components_map,af_lengths,comp_assigned,uc_id):
    for id in UC.alternate_flow.keys():
        val = UC.alternate_flow[id]
        #print('id is ',id)
        #print('val is ',val.action)
        if(str(val.action) == ''):
            resp_id = "UC"+str(uc_id)+"_"+str(id)+"_1"
            UC_1.af_responsibility[resp_id] = 'No responsibility found'
            comp_assigned[resp_id] = False
            af_lengths["UC"+str(uc_id)+"_"+str(id)] = 1
            continue

        flow = val.action.split("#")
        itr = 1
        for resp in flow:
            key_id = "UC"+str(uc_id)+"_"+str(id)+"_"+str(itr)
            fi = resp.find("'")
            si = resp[fi+1:].find("'")

            if resp.find("Include UC") !=-1 or resp.find("Extend UC") != -1:
                UC_1.af_responsibility[key_id] = resp
                comp_assigned[key_id] = False
                itr = itr + 1
                continue

            doc = nlp(resp)
            for possible_verb in doc:
                if str(possible_verb.pos_) == 'VERB':
                    child = list(possible_verb.children)
                    if fi == -1 or si == -1:
                        ans = str(possible_verb)
                        if len(child)>=2:
                            if child[0].dep_ != 'dobj' and child[1].dep_ != 'nsubj':
                                continue
                            ans = ans + " " + str(child[1])
                            resp_list = []
                            if str(child[0]) in components_map: 
                                resp_list = components_map[str(child[0])]
                            else:
                                components_map[str(child[0])] = resp_list
                            resp_list.append(key_id)
                            components_map[str(child[0])] = resp_list
                            UC_1.af_responsibility[key_id] = ans
                            comp_assigned[key_id] = True
                            break
                    else:
                        ans = str(possible_verb) + " "+ resp[fi+1:fi+si+1]                    
                        UC_1.af_responsibility[key_id] = ans
                        comp_assigned[key_id] = True
                        comp = str(str(resp).split(" ")[0])
                        resp_list = []
                        if comp in components_map: 
                            resp_list = components_map[comp]
                        else:
                            components_map[comp] = resp_list
                        resp_list.append(key_id)
                        components_map[comp] = resp_list
                        break

            if key_id not in  UC_1.af_responsibility.keys() :
                comp_resp = getResponsibility(resp)
                comp_assigned[key_id] = True
                UC_1.af_responsibility[key_id] = comp_resp[1]
                resp_list = []
                if comp_resp[0] in components_map: 
                    resp_list = components_map[comp_resp[0]]
                else:
                    components_map[comp_resp[0]] = resp_list
                resp_list.append(key_id)
                components_map[comp_resp[0]] = resp_list   




            itr = itr + 1

        itr = itr - 1
        af_lengths["UC"+str(uc_id)+"_"+str(id)] = itr  

def getPre_Post_Condition(UC,UC_1,uc_id):
    for id in UC.pre_condition.keys():
        key_id = "UC"+str(uc_id)+"_"+str(id)
        UC_1.precondition[key_id] = UC.pre_condition[id]

    for id in UC.post_conditions.keys():
        key_id = "UC"+str(uc_id)+"_"+str(id)
        UC_1.postcondition[key_id] = UC.post_conditions[id].description       

def nlpTest_main(p_UC, uc_id):
    UC = UseCaseClass.UseCase()
    UC = p_UC
    components_map = {}
    af_lengths = {}
    comp_assigned = {}
    UC_1 = UseCaseNLP()
    getPre_Post_Condition(UC,UC_1,uc_id)
    getBasicFlowResponsibility(UC,UC_1,components_map,af_lengths,comp_assigned,uc_id)
    getAlternateFlowResponsibility(UC,UC_1,components_map,af_lengths,comp_assigned,uc_id)

    return UC_1,comp_assigned,components_map,af_lengths