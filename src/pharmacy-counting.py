import sys

def checkCostNumType(input_file):
    """
    input_file - a string, a path to the input file
    Returns True, if file contains float values of cost.  
    """
    with open(input_file,'r') as fin:
        line=fin.readline()
        line=fin.readline()
    i=line.rfind(',')
    drug_cost=line[i+1:]
    if '.' in drug_cost:
        return True
    else:
        return False    

def extractDrugCost(item_line,isFloat):
    """
    item_line - a string  of format 'id,last_name,first_name,drug_name,cost'
    isFloat - a boolean value, (True if drug_cost value is float)
    Returns id, drug_name and drug_cost fields from item_line.
    last_name, first_name and drug_name may or may not contain '"' or ','
    """
    l=item_line.find(',')
    id=item_line[:l]
    i=item_line.rfind(',')
    if isFloat:
        drug_cost=float(item_line[i+1:])
    else:
        drug_cost=int(item_line[i+1:])
    j=item_line[:i].rfind(',')
    k=item_line[:i].rfind('"')
    if k<j:
        drug_name=item_line[j+1:i]
    else:
        l=item_line[:k].rfind('"')
        drug_name=item_line[l:k+1]
    return id,drug_name,drug_cost
    
def collectInfo(fin,isFloat):
    """
    fin - file object for input file
    isFloat - a boolean value, (True if drug_cost value is float)
    Returns a dictionary, that will contain information in the following form:
    {drug_name: [total_cost,prescribers_ids_set],...},
    where prescribers_ids_set is a set of id fields of people who prescribed particular drug.
    """
    drugs={}
    item_line=fin.readline()
    item_line=fin.readline()
    while item_line!='':
        id,drug_name,drug_cost=extractDrugCost(item_line,isFloat)        
        try:
            drugs[drug_name][0]+=drug_cost
            drugs[drug_name][1].add(id)
        except KeyError:
            drugs[drug_name]=[drug_cost,set([id])]      
        item_line=fin.readline()
    return drugs
    
def writeInfo(drugs,fout,isFloat):
    """
    fout - file object for output file
    isFloat - a boolean value, (True if drug_cost value is float)
    drugs - dictionary, that contains information in the following form:
    {drug_name: [total_cost,prescribers_ids_set],...},
    where prescribers_ids_set is a set of id fields of people who prescribed particular drug.
    This function writes the output data into the file.
    """
    fout.write('drug_name,num_prescriber,total_cost\n')
    if isFloat:
        for drug in sorted(drugs.keys(),key=lambda x:(-drugs[x][0],x.strip('"'))):
            fout.write('{0},{1},{2:.2f}\n'.format(drug,len(drugs[drug][1]),drugs[drug][0]))
    else:
        for drug in sorted(drugs.keys(),key=lambda x:(-drugs[x][0],x.strip('"'))):
            fout.write('{0},{1},{2}\n'.format(drug,len(drugs[drug][1]),drugs[drug][0]))             

if __name__ == "__main__":
    if len(sys.argv)!=3:
        sys.stderr("Usage: pharmacy-counting.py <input_file> <output_file> \n")
        sys.exit(-1)
    input_file,output_file=sys.argv[1:3]
    isFloat=checkCostNumType(input_file)
    with open(input_file,'r') as fin:
        drugs=collectInfo(fin,isFloat)
    with open(output_file,'w') as fout:
        writeInfo(drugs,fout,isFloat)
