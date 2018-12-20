#!/usr/bin/env python
import spacy
from spacy.symbols import advcl,conj,CCONJ,cc,dobj,pobj

print("Cargando modelo...")
nlp = spacy.load('en_coref_lg')

def getActions(doc):
    actions=[]
    #root = [token for token in doc if token.head == token][1]
    roots = [token for token in doc if token.head == token]
    print(roots)
    for root in roots:
        print("raiz:",root)
        follow=root.n_rights > 0
        i=root.i
        j=root.i
        main_root=root
            
        while follow:
            follow=False
            for token in root.rights:
                print(token)
                if token.dep==advcl or token.dep==conj:
                    follow=True
                    j=token.i
                    prev=doc[j-1]
                    if prev.pos==CCONJ:
                        j-=1
                    actions.append(doc[i:j])
                    i=token.i
                    root=token
        follow=root.n_lefts > 0

        if (j+1)<len(doc):
            actions.append(doc[i:len(doc)])
    return actions

def getMain(nSpan):
    if nSpan._.is_coref:
        main=nSpan._.coref_cluster
        return main.main
    else:
        return nSpan

def parseActions(actions):
    verbs=[]
    dObj=[]
    pObj=[]
    aux=[]
    for action in actions:
        dCount=0
        pCount=0
        verbs.append(action.root)
        for chunk in action.noun_chunks:
            if chunk.root.dep==dobj:
                dObj.append(getMain(chunk))
                dCount+=1
            elif chunk.root.dep==pobj:
                pObj.append(getMain(chunk))
                aux.append(chunk.root.head.text)
                pCount+=1

        if dCount<1:
            dObj.append(None)
        if pCount<1:
            pObj.append(None)
    return verbs,dObj,pObj,aux

def main():
    while True:
        p=raw_input("Inserte frase: ")
        u = unicode(p, "utf-8")
        doc=nlp(u)
        for token in doc:
            print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,token.shape_,
                token.is_alpha, token.is_stop)
        actions = getActions(doc)
        print("acciones:",actions)
        verbs,dObj,pObj,aux = parseActions(actions)
        print("verbos",verbs)
        print("Objeto directo",dObj)
        print("Preposicion",pObj)
        print("aux:",aux)
        
if __name__ == '__main__':
    main()
