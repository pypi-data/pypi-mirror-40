import tempfile
import subprocess

def load_conll (filename):
    fo = open(filename, "r", encoding='utf8')
    lines = fo.read().splitlines()
    fo.close()
    sentences = []
    offsets = []
    sent=None
    cpt=0
    next_sent_linenum=0
    for l in lines:
        if l != '':
            if sent == None:
                sent = [l]
                next_sent_linenum=cpt
            else:
                sent = sent+[l]
        else: # empty line
            if sent != None and (not all(l[0] == "#" for l in sent)): # end
                sentences=sentences+[sent]
                offsets = offsets+[next_sent_linenum]
                sent = None
        cpt += 1

    # needed in the is no newline at the end of the conll file
    if sent != None and (not all(l[0] == "#" for l in sent)): # end
        sentences=sentences+[sent]
        offsets = offsets+[next_sent_linenum]

    return (sentences, offsets)

cpt = 0
def reset():
    global cpt
    cpt=0

def new_id():
    global cpt
    cpt+=1
    return ("%05d" % cpt)

def get_sentid(sentence):
    try:
        sent_id_line = next(l for l in sentence if l[0]=="#" and "# sent_id =" in l)
        return (sent_id_line.split (" = "))[1]
    except StopIteration:
        return new_id()

def get_text(sentence):
    try:
        sent_id_line = next(l for l in sentence if l[0]=="#" and "# text =" in l)
        return (sent_id_line.split (" = "))[1]
    except StopIteration:
        return None

def to_svg(sentence):
    with tempfile.NamedTemporaryFile('w', suffix=".conllu", encoding='utf8') as temp:
        conllu=temp.name
        svg=conllu.replace('conllu', 'svg')
        for l in sentence:
            temp.write(l+"\n")
        temp.flush()
        err= ""
        sub=subprocess.run (["dep2pict","--batch",conllu,svg], stderr=subprocess.PIPE)
        if sub.returncode != 0:
            return sub.stderr.decode("utf-8")
    return svg
