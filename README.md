# Learning-curves-for-DRP

Using learning curves for the comparison of multiple modalities performance at anti-cancer drug response prediction (DRP) with both neural networks and XGBoost.
Three modalities are compared here: RNA-seq, proteomics and phosphoproteomics.

Due to the significantly smaller number of cell lines with phosphoproteomics profiles, the analysis is split into two parts. The first part uses the 38 cell lines with phosphoproteomics protoeomics and RNA-seq profiles (CLS38). The second part uses the 877 cell lines with  protoeomics and RNA-seq proflies (CL877). For code relating to CLS38 see CLS38_phos_prot_RNA. For code relating to CLS38 see CLS38_phos_prot_RNA. 

The two yml files give the conda environments that I used for kears TensorFlow and XGBoost. 


### Using the repository 
Within both the CLS38_phos_prot_RNA and CLS877_RNA_prot folders there is a notebook that was used to analyses the results and create the plots used in the paper. 

Both folders also contain the code used to create the learning curves with both Neural networks and XGBoost. The majority of the code needed for this is contained within Python scripts. The implementation of these scripts for each modality is given within notebooks. For example, phos_LTTfs_main_run_lc.ipynb implemnts these scripts to find the results needed to plot the phosphoproteomics learning curve. Therefore, following this notebook will take you through the steps I used in creating the phosphoproteomics learning curve. 
