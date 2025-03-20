import pandas as pd
import numpy as np
import sys; sys.path.insert(0, '/root/similarity_activity_predictor/jcompoundmapper_pywrapper')
from jCompoundMapper_pywrapper import JCompoundMapper
from rdkit import DataStructs
from rdkit import Chem
from rdkit.DataStructs.cDataStructs import SparseBitVect
from rdkit.Chem.Fingerprints import FingerprintMols
from rdkit.DataStructs.cDataStructs import CreateFromBitString
from rdkit.DataStructs import ConvertToExplicit



def fingerprint_generator_rdkit(df):
    df["ROMol"] = df.loc[:,"smiles"].apply(Chem.MolFromSmiles)
    df["fps"] = df.loc[:,"ROMol"].apply(FingerprintMols.FingerprintMol)
    return df

def fingerprint_generator_ASP(df): 
    jcm = JCompoundMapper("ASP")
    df["ROMol"] = df.loc[:,"smiles"].apply(Chem.MolFromSmiles)
    fingerprints = jcm.calculate(df.loc[:,"ROMol"])
    df["fps"] = None  
    df["fps"] = df["fps"].astype(object)
    for idx in fingerprints.index:
        df.loc[idx,"fps"] = list_to_explicit_bit_vect(fingerprints.loc[idx,:])
    return df

def fingerprint_generator_LSTAR(df): 
    jcm = JCompoundMapper("LSTAR")
    df["ROMol"] = df.loc[:,"smiles"].apply(Chem.MolFromSmiles)
    fingerprints = jcm.calculate(df.loc[:,"ROMol"])
    df["fps"] = None  
    df["fps"] = df["fps"].astype(object)
    for idx in fingerprints.index:
        df.loc[idx,"fps"] = list_to_explicit_bit_vect(fingerprints.loc[idx,:])
    return df

def fingerprint_generator_RAD2D(df): 
    jcm = JCompoundMapper("RAD2D")
    df["ROMol"] = df.loc[:,"smiles"].apply(Chem.MolFromSmiles)
    fingerprints = jcm.calculate(df.loc[:,"ROMol"])
    df["fps"] = None  
    df["fps"] = df["fps"].astype(object)
    for idx in fingerprints.index:
        df.loc[idx,"fps"] = list_to_explicit_bit_vect(fingerprints.loc[idx,:])
    return df


def list_to_explicit_bit_vect(fp_list):
    """Convierte una lista de 0s y 1s en un ExplicitBitVect de RDKit."""
    bit_string = "".join(map(str, fp_list))
    return CreateFromBitString(bit_string)