import sys,os
import json
import heapq

def extractDrugCost(item_line):
    """
    Returns id, drug_name and drug_cost fields from a string item_line of format 'id,last_name,first_name,drug_name,cost'.
    last_name, first_name and drug_name may or may not contain '"' or ','
    """
    l=item_line.find(',')
    id=item_line[:l]
    i=item_line.rfind(',')
    drug_cost=float(item_line[i+1:])
    j=item_line[:i].rfind(',')
    k=item_line[:i].rfind('"')
    if k<j:
        drug_name=item_line[j+1:i]
    else:
        l=item_line[:k].rfind('"')
        drug_name=item_line[l:k+1]
    return id,drug_name,drug_cost
    
def divideInput(fin):
    """
    fin - file object for input file
    Reads input file line by line, extracts id, drug_name and drug_cost fields from each data entry and groups them (as tuples) by the first letter in the drug_name (or '"').
    Writes each group into file <letter>.json (or quotes.json for names with '"')
    Returns list of filenames created.
    """
    drug_groups={}
    item_line=fin.readline()
    item_line=fin.readline()
    while item_line!='':
        id,drug_name,drug_cost=extractDrugCost(item_line)    
        try:
            drug_groups[drug_name[0]].append((id,drug_name,drug_cost))
        except KeyError:
            drug_groups[drug_name[0]]=[(id,drug_name,drug_cost)]    
        item_line=fin.readline()
    for letter in drug_groups.keys():
        if letter=='"':
            name='quotes'
        else:
            name=letter
        with open(os.path.join(os.getcwd(), name+'.json')) as fout:
            json.dump(drug_groups[letter],fout)
    filenames=drug_groups.keys()[:]
    if '"' in filenames:
        filenames.remove('"')
        filenames.append('quotes')
    return filenames

def collectInfoByGroup(filename):    
    """
    filename - string, filename.json contains list of tuples (id,drug_name,drug_cost)
    Returns a sorted (by cost, and name if there is a tie) list, each element of which is a tuple (-total_cost,drug_name_without_quotes,num_prescribers, drug_name). This particular format is chosen for sorting purposes. This list contains statistics obtained from 1 .json file.
    """
    output_list=[]
    drugs={}
    with open(os.path.join(os.getcwd(), name+'.json')) as fin:
        input_list=json.load(fin)
    for entry in input_list:
        try:
            drugs[entry[1]][0]+=entry[2]
            drugs[entry[1]][1].add(entry[0])
        except KeyError:
            drugs[entry[1]]=[entry[2],set([entry[0]])]
    for drug in sorted(drugs.keys(),key=lambda x:(-drugs[x][0],x.strip('"'))):
        output_list.append((-float(drugs[drug][0]),str(drug.strip('"')),int(len(drugs[drug][1])),str(drug)))
    os.remove(os.path.join(os.getcwd(), name+".json"))
    return output_list
    
def collectGroups(filenames):
    """
    filenames - list of .json files filenames, that contain input data (list of strings)
    Returns a list of sorted lists, each list contains statistics obtained from each .json file.
    """
    list_of_lists=[]
    for name in filenames:
        list_of_lists.append(collectInfoByGroup(name))
    return list_of_lists
    
def collectTotalInfo(list_of_lists):
    """
    list_of_lists - list of sorted lists, each list contains statistics obtained from each .json file
    Returns a sorted (by cost, and name if there is a tie) list, each element of which is a tuple (drug_name,num_prescribers,total_cost). This list contains statistics obtained from whole dataset.
    """
    sorted_list=heapq.merge(*list_of_lists)
    output_list=[]
    for item in sorted_list:
        output_list.append((item[3],item[2],-item[0]))
    return output_list
    
def writeInfo(sorted_list,fout):
    """
    fout - file object for output file
    sorted_list - a list of tuples (drug_name,num_prescribers,total_cost)
    This function writes the output data into the file.
    """
    fout.write('drug_name,num_prescriber,total_cost\n')
    for entry in sorted_list:
        fout.write('{0},{1},{2:.2f}\n'.format(entry[0],entry[1],entry[2]))
    
if __name__ == "__main__":    
    if len(sys.argv)!=3:
        sys.stderr("Usage: pharmacy-counting.py <input_file> <output_file> \n")
        sys.exit(-1)
    input_file,output_file=sys.argv[1:3]
    with open(input_file,'r') as fin:
        filenames=divideInput(fin)
    list_of_lists=collectGroups(filenames)
    sorted_list=collectTotalInfo(list_of_lists)
    with open(output_file,'w') as fout:
        writeInfo(sorted_list,fout)