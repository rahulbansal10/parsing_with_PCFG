
# coding: utf-8

# In[1]:


import nltk
import sys
nltk.download('treebank')
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import treebank
from nltk.grammar import ProbabilisticProduction
from nltk.grammar import PCFG
from nltk import Nonterminal
from nltk.grammar import CFG


# In[2]:


#print(treebank.fileids())
#print(treebank.sents(treebank.fileids()))
#print(type(treebank.parsed_sents(treebank.fileids()[0])[0]))


# In[3]:


from nltk import induce_pcfg
# extract productions from three trees and induce the PCFG
#print("Induce PCFG grammar from treebank data:")

productions = []
for item in treebank.fileids()[:200]:
  for tree in treebank.parsed_sents(item):
    # perform optional tree transformations, e.g.:
    tree.collapse_unary(collapsePOS = False)# Remove branches A-B-C into A-B+C
    tree.chomsky_normal_form(horzMarkov = 2)# Remove A->(B,C,D) into A->B,C+D->D
    #print(tree.productions())
    productions += tree.productions()


# In[4]:


S = Nonterminal('S')
gm = CFG(S, productions)


# In[21]:


sent = sys.argv[1]
#sent = ' '.join((treebank.sents(treebank.fileids()[113])[0]))
print(sent)
#sent = 'After years of struggling , the Los Angeles Herald Examiner will publish its last edition today .'


# In[22]:


tokens = sent.split()
rptokens = sent.split()
missing = [tok for tok in tokens if not gm._lexical_index.get(tok)]
for i in range(len(tokens)):
  if tokens[i] in missing:
    #print('Hi')
    tp=nltk.tag.pos_tag([tokens[i]])
    print(tp)
    tokens[i]='UNK'
    prd= ProbabilisticProduction(Nonterminal(tp[0][1]), ('UNK',), prob=0.01)
    productions.append(prd)


# In[23]:


from nltk.grammar import induce_pcfg
S = Nonterminal('S')
grammar = induce_pcfg(S, productions)


# In[24]:


from nltk import tokenize
from nltk.parse import ViterbiParser

#demos = [(' '.join((treebank.sents(treebank.fileids()[113])[0])), grammar)]
#sent, grammar = demos[0]
#print(sent)

parser = ViterbiParser(grammar)


# In[25]:


try:
  parses = parser.parse_all(tokens)
  #print(parses[0])
except:
  print("Some words not covered")


# In[26]:


import re

a=str(parses[0])
print(a)
ind=[m.start() for m in re.finditer('UNK', a)]
k=0
prev=0
for i in range(len(tokens)):
  if(tokens[i]=='UNK'):
    t=ind[k]+prev
    #print(a[t:t+3],t)
    a=a.replace(a[t:t+3],rptokens[i],1)
    k=k+1
    if(k< len(ind)):
       prev=len(rptokens[i])-3


# In[27]:


t = a.rfind('(')
#print(t)
a = a[:t]
print(a)


# In[29]:


#from nltk import Tree
#tree = Tree.fromstring(a)
#print(tree)

