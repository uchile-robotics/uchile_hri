#!/usr/bin/env python

from MBSP import parse
from MBSP import split
from ConfigParser import SafeConfigParser
from rospkg import RosPack

rospack=RosPack()

config_path = rospack.get_path('bender_nlp')+ '/config/'
config_path = './config/'

class GenerateOrder:
    cparser = SafeConfigParser()

    #Init
    def __init__(self, sentence):
        self.verbs = []
        self.people = []
        self.objects = []
        self.places = []
        self.information = []        
        self.filter_sentences(sentence)
            
        
    #add_order
    def add_order(self,verb,info,data):
        sameMove = False
        if verb == 'go' and len(self.verbs) > 0:
            indices = [i for i,x in enumerate(self.verbs) if x == verb]
            for ii in indices:
                if self.places[ii] == info:
                    sameMove = True
        if not sameMove:
            self.verbs.append(verb)
            s_info = ' '.join([w.string for w in info])
            if data == 'person':
                self.people.append(s_info)
                self.objects.append('')
                self.places.append('')
                self.information.append('')
            if data == 'object':
                self.people.append('')
                self.objects.append(s_info)
                self.places.append('')
                self.information.append('')
            if data == 'place':
                self.people.append('')
                self.objects.append('')
                self.places.append(s_info)
                self.information.append('')
            if data == 'information':
                self.people.append('')
                self.objects.append('')
                self.places.append('')
                self.information.append(s_info)


    #parse_sentence
    def parse_sentence(self,sentence):
        sentence = sentence.replace('hand it ','bring it ')
        sentence = sentence.replace('put ','place ')
        sen = sentence.split(' and ')
        ws = sen[0].split(' ')
        ss = []
        for i in range(len(ws)):
            add_sen = True
            ww = ws[i:]
            if len(ww) < 2:
                break
            s = ' '.join(ww)
            s = parse(s)
            s = split(s)
            t = s[0].words[0].type
            if (t == 'VB' or t == 'VBP') and s[0].words[0].chunk.type != 'INTJ':
                if len(ss) > 0:
                    aux = ss[len(ss)-1].replace(' '+s.string,'')
                    s_aux = aux.split(' ')
                    if len(s_aux) == 2 and s_aux[1] == 'the':
                        add_sen = False
                    else:
                        ss[len(ss)-1] = aux
                        add_sen = True
                if add_sen:
                    ss.append(s.string)
        if len(sen) == 2:
            ss.append(sen[1])
        ss_aux = []
        isJoin = False
        for i in range(len(ss)):
            if ss[i].find('pick') == 0 and ss[i].find('from') < 0:
                if ss[i+1].find('from') >= 0:
                    ss_aux.append(' '.join([ ss[i],ss[i+1] ]))
                    isJoin = True
            else:
                if not isJoin:
                    ss_aux.append(ss[i])
                else:
                    isJoin = False
        return ss_aux

    #obtain_information
    def obtain_information(self,chunk):
        isTO = False
        isIN = False
        aux = []
        sv_aux = []
        sto_aux = []
        sin_aux = []
        verb = chunk[0].words[0]
        if len(chunk[0].words) > 1:
            for w in chunk[0].words[1:]:
                sv_aux.append(w)
        
        for c in chunk[1:]:
            if len(c.words) == 1 and c.words[0].tag == 'TO':
                isTO = True
            elif len(c.words) == 1 and c.words[0].tag == 'IN' and c.words[0].string != 'of':
                    isIN = True
            elif len(c.words) == 1 and c.words[0].tag == 'WB':
                isTO = False
                isIN = False
            else:
                if not isTO and not isIN:
                    for w in c.words:
                        if w.tag != 'RP':
                            sv_aux.append(w)
                if isTO:
                    for w in c.words: 
                        if w.tag != 'RP':
                            sto_aux.append(w)
                    isTO = False
                if isIN:
                    if sin_aux != [] and sto_aux ==[]:
                        for w in sin_aux:
                            sto_aux.append(w)
                        sin_aux = []
                    for w in c.words: 
                        if w.tag != 'RP':
                            sin_aux.append(w)
                    isIN = False
        #Limpieza de DT, RB y PRP$
        while(len(sv_aux) >= 2):
            if sv_aux[0].tag == 'DT' or sv_aux[0].tag == 'RB' or sv_aux[0].tag == 'PRP$':
                del sv_aux[0]
            elif sv_aux[-1].tag == 'RB':
                del sv_aux[-1]
            else:
                break
        while(len(sto_aux) >= 2):
            if sto_aux[0].tag == 'DT' or sto_aux[0].tag == 'RB' or sto_aux[0].tag == 'PRP$':
                del sto_aux[0]
            elif sto_aux[-1].tag == 'RB':
                del sto_aux[-1]
            else:
                break
        while(len(sin_aux) >= 2):
            if sin_aux[0].tag == 'DT' or sin_aux[0].tag == 'RB' or sin_aux[0].tag == 'PRP$':
                del sin_aux[0]
            elif sin_aux[-1].tag == 'RB':
                del sin_aux[-1]
            else:
                break
        #Retorno de datos
        if len(sv_aux) >= 3:
            if sv_aux[-2].tag == 'WP' and sv_aux[-1].tag == 'VBZ':
                return (verb, sv_aux[:-2], sto_aux, sin_aux)
        return (verb, sv_aux, sto_aux, sin_aux)

        #generate_list
    def generate_list(self, verb, oi):
        for name,value in self.cparser.items(verb):
            verb,data1,pos = value.split(',')
            self.add_order(verb,oi[int(pos)],data1)
        
    #filter_sentences
    def filter_sentences(self,sentences):
        self.cparser.read(''.join([config_path,'verb_list.conf']))
        ss = self.parse_sentence(sentences)
        is_To = False
        is_In = False
        for s in ss:
            data = []
            sen = parse(s)
            sen = split(sen)
            #print 'split: {}'.format(sen)
            chunk = sen[0].chunk
            oi = self.obtain_information(chunk)
            #print 'oi: {}'.format(oi)
            v = chunk[0]
            aux = []
            if v.string == 'go' or v.string=='move' or v.string == 'navigate': #Go #Move #Navigate
                self.generate_list('go_1',oi)
            elif v.string == 'leave': #Leave
                self.generate_list('leave_1',oi)
            elif v.string == 'answer': #Answer
                self.generate_list('answer_1',oi)
            elif v.string == 'carry': #Carry
                self.generate_list('carry_1',oi)
            elif v.string == 'introduce': #Introduce
                self.generate_list('introduce_1',oi)
            elif v.string == 'ask': #Ask
                self.generate_list('ask_1',oi)
            elif v.string == 'tell' or v.string == 'say': #Tell #Say
                if oi[2] == []:
                    tag = 'tell_1'
                elif oi[2][0].tag == 'PRP':
                    tag = 'tell_3'
                else:
                    tag = 'tell_2'
                self.generate_list(tag,oi)
            elif v.string == 'find' or v.string == 'locate': #Find #Locate
                aux = [w.string for w in oi[1]]
                if ('me' in aux or aux[0] != aux[0].lower() or 'person' in aux) and oi[3] == []:
                    tag = 'find_1'
                elif aux[0] == aux[0].lower() and oi[3] == []:
                    tag = 'find_2'
                elif ('me' in aux or aux[0] != aux[0].lower() or 'person' in aux) and oi[3] != []:
                    tag = 'find_3'
                elif aux[0] == aux[0].lower() and oi[3] != []:
                    tag = 'find_4'
                self.generate_list(tag,oi)
            elif v.string == 'follow': #Follow
                if oi[3] == []:
                    tag = 'follow_1'
                else:
                    tag = 'follow_2'
                self.generate_list(tag,oi)
            elif v.string == 'look': #Look
                if oi[2] == []:
                    aux = [w.string for w in oi[3]]
                else:
                    aux = [w.string for w in oi[2]]

                if oi[2] == []:
                    if aux[0] == 'me' or aux[0].lower() != aux[0] or 'person' in aux:
                        tag = 'look_1'
                    else:
                        tag = 'look_2'
                else:
                    if aux[0] == 'me' or aux[0].lower() != aux[0] or 'person' in aux:
                        tag = 'look_3'
                    else:
                        tag = 'look_4'
                self.generate_list(tag,oi)
            elif v.string == 'grasp' or v.string == 'take': #Grasp #Take
                if oi[2] == [] and oi[3] == []:
                    tag = 'take_1'
                elif oi[2] == [] and oi[3] != []:
                    tag = 'take_3'
                elif oi[2] != [] and oi[3] == []:
                    if oi[1][0].string == 'her' or oi[1][0].string == 'him':
                        tag = 'take_2'
                    else:
                        tag = 'take_4'
                self.generate_list(tag,oi)
            elif v.string == 'bring': #Bring
                if oi[3] != []:
                    if oi[1][0].tag == 'PRP':
                        if oi[1][0].string == 'me':
                            ll = oi[1]
                            aux_list = [[ll[:ll.index(elem)],ll[ll.index(elem)+1:]] for elem in ll if elem.tag == 'DT'][0]
                            oi = (oi[0],aux_list[0],aux_list[1],oi[3])
                            tag = 'bring_6'
                        else:
                            tag = 'bring_2'
                    else:
                        tag = 'bring_1'
                else:
                    if len(oi[1]) == 1 and oi[1][0].tag == 'PRP':
                        if oi[2][0].tag == 'PRP':
                            tag = 'bring_3'
                        elif oi[2][0].tag == 'NNP':
                            tag = 'bring_5'
                        else:
                            tag = 'bring_4'
                self.generate_list(tag,oi)
            elif v.string == 'place': #Place 
                self.generate_list('place_1',oi)
            elif v.string == 'give': #Give
                if oi[3] != []:
                    if len(oi[1]) == 1 and oi[1][0].tag == 'PRP':
                        tag = 'give_2'
                    else:
                        tag = 'give_4'
                else:
                    if len(oi[1]) == 1 and oi[1][0].tag == 'PRP':
                        tag = 'give_1'
                    else:
                        tag = 'give_3'
                self.generate_list(tag,oi)
            elif v.string == 'guide': #Guide
                if len(oi[1]) == 1 and oi[1][0].tag == 'PRP':
                    tag = 'guide_1'
                else:
                    tag = 'guide_2'
                self.generate_list(tag,oi)
            elif v.string == 'get' or v.string == 'pick': #Get #Pick
                if oi[3] != []:
                    tag = 'get_2'
                else:
                    tag = 'get_1'
                self.generate_list(tag,oi)
            elif v.string == 'deliver': #Deliver
                if oi[2] != [] and oi[3] == []:
                    if oi[2][0].tag == 'NNP':
                        tag = 'deliver_1'
                    elif oi[2][0].tag == 'PRP':
                        tag = 'deliver_3'
                elif oi[2] == [] and oi[3] != []:
                    tag = 'deliver_2'
                self.generate_list(tag,oi)
            elif v.words[0].string == 'escort': #Escort
                if oi[3] != []:
                    tag = 'escort_1'
                else:
                    tag = 'escort_2'
                self.generate_list(tag,oi)
            else:
                print 'Verb {} not found'.format(v.string)
        self.replacePRP()

    # replacePRP
    def replacePRP(self):
            while u'it' in self.objects or u'them' in self.objects:
                if u'it' in self.objects:
                    i = self.objects.index(u'it')
                elif u'them' in self.objects:
                    i = self.objects.index(u'them')
                self.objects[i] = [item for item in self.objects[i-1::-1] if item!=''][0]
            while u'her' in self.people or u'him' in self.people:
                if u'her' in self.people:
                    i = self.people.index(u'her')
                elif u'him' in self.people:
                    i = self.people.index(u'him')
                self.people[i] = [item for item in self.people[i-1::-1] if item!=''][0]
                    

if __name__=='__main__':
    # Sentence to analize
    sens = "go to the bedroom find Mia and follow her"
    # Analize sentence and obtain orders
    s = GenerateOrder(sens)
        
    # Uncomment for view results
    print sens
    print '==========================='
    print 'Verbs  : {}'.format(s.verbs)
    print 'People : {}'.format(s.people)
    print 'Objects: {}'.format(s.objects)
    print 'Places : {}'.format(s.places)
    print 'Info   : {}'.format(s.information)
