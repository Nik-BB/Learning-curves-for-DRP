# Learning-curves-for-DRP

This repository contains the source code needed to reproduce the results and figures for the paper 'Comparison of multiple modalities for drug response prediction with learning curves using neural networks and XGBoost'. 

The paper uses learning curves for the comparison of multiple modalities performance at anti-cancer drug response prediction (DRP) with both neural networks and XGBoost.
Three modalities are compared here: RNA-seq, proteomics and phosphoproteomics.

Due to the significantly smaller number of cell lines with phosphoproteomics profiles, the analysis is split into two parts. The first part uses the 38 cell lines with phosphoproteomics protoeomics and RNA-seq profiles (CLS38). The second part uses the 877 cell lines with  protoeomics and RNA-seq proflies (CL877). For code relating to CLS38 see CLS38_phos_prot_RNA. For code relating to CLS38 see CLS38_phos_prot_RNA. 

The two yml files give the conda environments that were used for kears TensorFlow and XGBoost. 


### Using the repository 

#### Reproducing the paper figures.

The data and the source code needed to reproduce the figures are given in this repository.
Within both the CLS38_phos_prot_RNA and CLS877_RNA_prot folders there is a notebook  to analyses the results and create the plots used in the paper. 
For CLS38 this notebook is called UCL_plotting_phos_ect.ipynb. For CLS877 this notebook is called UCL_plotting_clean.ipynb. These files give the source code needed to reproduce the figures in the paper. The raw data used for these figures is in the folder LC_metric-results.



#### Re-training and testing the models 
Both folders also contain the code used to train all of the models that are then used to create the learning curves with both Neural networks and XGBoost. The code needed for this is contained within Python modules that I have created. The implementation of modules scripts for each modality is given within notebooks. For example, phos_LTTfs_main_run_lc.ipynb implemnts these scripts to train the models used to plot the phosphoproteomics learning curve. Therefore, following this notebook will take you through the steps used in traning the models for the phosphoproteomics learning curve. 

See the [code usage tutorial](https://github.com/Nik-BB/Learning-curves-for-DRP/blob/main/code-usage-tutorial.pdf) in this GitHub repo for a pdf walkthrough of the code.

### Datasets
The datasets need to re-train the models are publically available. 

#### Omics datasetes

* RNA-seq data from the Genomics of drug sensitivity in cancer database https://www.cancerrxgene.org/

* Proteomics data from the paper 'Pan-cancer proteomic map of 949 human cell lines https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9387775/

* Phosphoproteomics data from 'Drug ranking using machine learning systematically predicts the efficacy of anti-cancer drugs' paper https://www.nature.com/articles/s41467-021-22170-8

#### Truth values / Target data

* IC50 values from GDSC1 https://www.cancerrxgene.org/

#### Databases used for feature selection 

* Landmark genes from  the paper 'A Next Generation Connectivity Map: L1000 Platform and the First 1,000,000 Profiles' https://pubmed.ncbi.nlm.nih.gov/29195078/

* Protein targets from https://omnipathdb.org/

Once downloaded the path to these datasets needs to be set in the Data_imports.py files. The path to the databases used for feature selection needs to be set in the main notebooks that run the learning curves e.g. phos_LTTfs_main_run_lc.ipynb. 
