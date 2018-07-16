import sys

def extractDrugCost(item_line):
    """
    Returns id, drug_name and drug_cost fields from a string item_line of format 'id,last_name,first_name,drug_name,cost'.
    last_name, first_name and drug_name may or may not contain '"' or ','
    Works under assumption that id has 10 digits.
    """
    id=item_line[:10]
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
    
def collectInfo(fin):
    """
    fin - file object for input file
    Returns a dictionary, that will contain information in the following form:
    {drug_name: [total_cost,prescribers_ids_set],...},
    where prescribers_ids_set is a set of id fields of people who prescribed particular drug.
    """
    drugs={}
    item_line=fin.readline()
    item_line=fin.readline()
    while item_line!='':
        id,drug_name,drug_cost=extractDrugCost(item_line)        
        try:
            drugs[drug_name][0]+=drug_cost
            drugs[drug_name][1].add(id)
        except KeyError:
            drugs[drug_name]=[drug_cost,set([id])]      
        item_line=fin.readline()
    return drugs
             

if __name__ == "__main__":
    if len(sys.argv)!=3:
        sys.stderr("Usage: pharmacy-counting.py <input_file> <output_file> \n")
        sys.exit(-1)
    input_file, output_file=sys.argv[1:3]
    fin=open(input_file,'r')
    drugs=collectInfo(fin)
    fin.close()
    fout=open(output_file,'r')
    fout.write('drug_name,num_prescriber,total_cost\n')
    for drug in sorted(drugs.keys(),key=lambda x:drugs[x][0],reverse=True):
        fout.write(drug+','+str(len(drugs[drug][1]))+','+str(drugs[drug][0])+'\n')
    fout.close()
