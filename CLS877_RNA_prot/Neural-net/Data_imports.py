import numpy as np
import pandas as pd
import sys
codebase_path = '/data/home/wpw035/Codebase'
import DRP_utils.data_preprocessing as dp_nb
sys.path.insert(0, codebase_path) #add path to my codebase models

#read and format target values

def read_targets():
    df_ic50 = pd.read_csv(f'{codebase_path}/downloaded_data_small/GDSC1_ic50.csv')
    frame = {}
    for d in np.unique(df_ic50['CELL_LINE_NAME']):
        cellDf = df_ic50[df_ic50['CELL_LINE_NAME'] == d]
        cellDf.index = cellDf['DRUG_NAME']
        frame[d] = cellDf['LN_IC50']


    def remove_repeats_mean_gdsc1(frame, df_ic50): 
        new_frame = {}
        for cell_line in np.unique(df_ic50['CELL_LINE_NAME']):
            temp_subset = frame[cell_line].groupby(frame[cell_line].index).mean()
            new_frame[cell_line] = temp_subset
        return new_frame  

    new_frame = remove_repeats_mean_gdsc1(frame, df_ic50)
    ic50_df1 = pd.DataFrame(new_frame).T
    
    return ic50_df1



def read_input_data():
    
    ic50_df1 = read_targets()
    _all_drugs = ic50_df1.columns
    
    #drug one hot encoding
    frame = {}
    for i,d in enumerate(_all_drugs):
        hot_vec = np.zeros(len(_all_drugs))
        hot_vec[i] = 1
        frame[d] = hot_vec
    one_hot_drugs = pd.DataFrame(frame)

    #read in protmics data
    uniprot_ids = pd.read_csv(
        f'{codebase_path}/downloaded_data_small/Proteinomics_large.tsv',
        sep = '\t', skipfooter = 951).columns[2 :] #keep ids of col names

    prot_raw = pd.read_csv(
        f'{codebase_path}/downloaded_data_small/Proteinomics_large.tsv',
        sep = '\t', header=1
    )
    prot_raw.drop(index=0, inplace=True)

    prot_raw.index = prot_raw['symbol']
    prot_raw.drop(columns=['symbol', 'Unnamed: 1'], inplace=True)
    
    #replace missing protomics values
    p_miss = prot_raw.isna().sum().sum() / (len(prot_raw) * len(prot_raw.columns))
    print(f'Number of missing prot values {p_miss}')
    #close to 40% of the dataframe is missing valuse
    #replace nan with zero (as done in the paper)
    prot = prot_raw.replace(np.nan, 0)

    #check for duplications and missing value in cols and index
    assert sum(prot.index.duplicated()) == 0
    assert sum(prot.columns.duplicated()) == 0
    assert sum(prot.index.isna()) == 0
    assert sum(prot.columns.isna()) == 0

    #only keep interserciton of cl's and truth values
    ic50_df1, prot = dp_nb.keep_overlapping(ic50_df1, prot)
    print(f'num non overlapping prot and target cls: {len(prot_raw) - len(prot)}')

    #read in rna-seq data
    gdsc_path = '/data/home/wpw035/GDSC'
    rna_raw = pd.read_csv(f'{gdsc_path}/downloaded_data/gdsc_expresstion_dat.csv')
    rna_raw.index = rna_raw['GENE_SYMBOLS']
    rna_raw.drop(columns=['GENE_SYMBOLS','GENE_title'], inplace=True)
    cell_names_raw = pd.read_csv(f'{gdsc_path}/downloaded_data/gdsc_cell_names.csv', skiprows=1, skipfooter=1)
    cell_names_raw.drop(index=0, inplace=True)

    #chagne ids to cell names
    id_to_cl = {}
    for _, row in cell_names_raw.iterrows():
        cell_line = row['Sample Name']
        ident = int(row['COSMIC identifier'])
        id_to_cl[ident] = cell_line

    ids = rna_raw.columns
    ids = [int(iden.split('.')[1]) for iden in ids] 

    #ids that are in rna_raw but don't have an assocated cl name 
    #from cell_names_raw (not sure why we have these)
    missing_ids = []
    for iden in ids:
        if iden not in id_to_cl.keys():
            missing_ids.append(iden)
    missing_ids = [f'DATA.{iden}' for iden in missing_ids]      
    rna_raw.drop(columns=missing_ids, inplace=True)

    cell_lines = []
    for iden in ids:
        try:
            cell_lines.append(id_to_cl[iden])
        except KeyError:
            pass
    rna_raw.columns = cell_lines
    rna_raw = rna_raw.T

    #take out duplicated cell line
    rna_raw = rna_raw[~rna_raw.index.duplicated()] 
    #take out nan cols
    rna_raw = rna_raw[rna_raw.columns.dropna()]
    #take out duplciated cols
    rna_raw = rna_raw.T[~rna_raw.columns.duplicated()].T

    #check for duplications and missing value in cols and index
    assert sum(rna_raw.index.duplicated()) == 0
    assert sum(rna_raw.columns.duplicated()) == 0
    assert sum(rna_raw.index.isna()) == 0
    assert sum(rna_raw.columns.isna()) == 0
    
    #only keep intersect of rna and prot cl's
    prot, rna = dp_nb.keep_overlapping(prot, rna_raw)
    _all_cls = prot.index
    print(f'num non overlapping rna prot and target cls: {len(rna_raw) - len(rna)}')
    prot.shape, rna.shape
    
    #one hot input data (instead of omic)
    one_hot_cls = []
    for i, cl in enumerate(_all_cls):
        hot_cl = np.zeros(len(_all_cls))
        hot_cl[i] = 1
        one_hot_cls.append(hot_cl)
    one_hot_cls = pd.DataFrame(one_hot_cls)  
    one_hot_cls.index = _all_cls

    
    return prot, rna, one_hot_cls, one_hot_drugs, ic50_df1