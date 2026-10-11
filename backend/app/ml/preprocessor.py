import re
import numpy as np
import pandas as pd
from typing import Tuple, List, Dict, Any, Optional

CANONICAL_FEATURES = [
    'Destination Port',
    'Flow Duration',
    'Total Fwd Packets',
    'Total Backward Packets',
    'Total Length of Fwd Packets',
    'Total Length of Bwd Packets',
    'Fwd Packet Length Max',
    'Fwd Packet Length Min',
    'Fwd Packet Length Mean',
    'Fwd Packet Length Std'
]

ALIAS_MAP = {
    'destination port': 'Destination Port',
    'dest port': 'Destination Port',
    'dst port': 'Destination Port',
    'destination_port': 'Destination Port',
    'flow duration': 'Flow Duration',
    'flow_duration': 'Flow Duration',
    'duration': 'Flow Duration',
    'total fwd packets': 'Total Fwd Packets',
    'total fwd packet': 'Total Fwd Packets',
    'total_fwd_packets': 'Total Fwd Packets',
    'fwd packets': 'Total Fwd Packets',
    'total backward packets': 'Total Backward Packets',
    'total bwd packets': 'Total Backward Packets',
    'total_bwd_packets': 'Total Backward Packets',
    'total_backward_packets': 'Total Backward Packets',
    'total length of fwd packets': 'Total Length of Fwd Packets',
    'total_length_of_fwd_packets': 'Total Length of Fwd Packets',
    'totlen fwd pkts': 'Total Length of Fwd Packets',
    'total length of bwd packets': 'Total Length of Bwd Packets',
    'total_length_of_bwd_packets': 'Total Length of Bwd Packets',
    'totlen bwd pkts': 'Total Length of Bwd Packets',
    'fwd packet length max': 'Fwd Packet Length Max',
    'fwd_packet_length_max': 'Fwd Packet Length Max',
    'fwd pkt len max': 'Fwd Packet Length Max',
    'fwd packet length min': 'Fwd Packet Length Min',
    'fwd_packet_length_min': 'Fwd Packet Length Min',
    'fwd pkt len min': 'Fwd Packet Length Min',
    'fwd packet length mean': 'Fwd Packet Length Mean',
    'fwd_packet_length_mean': 'Fwd Packet Length Mean',
    'fwd pkt len mean': 'Fwd Packet Length Mean',
    'fwd packet length std': 'Fwd Packet Length Std',
    'fwd_packet_length_std': 'Fwd Packet Length Std',
    'fwd pkt len std': 'Fwd Packet Length Std',
    'label': 'Label',
    'class': 'Label',
    'attack': 'Label',
    'target': 'Label'
}

def clean_col_name(c: str) -> str:
    cleaned = re.sub(r'[^a-zA-Z0-9 ]', ' ', str(c)).strip().lower()
    return re.sub(r'\s+', ' ', cleaned)

def map_column_names(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, str]]:
    rename_dict = {}
    original_to_canonical = {}
    for col in df.columns:
        norm = clean_col_name(col)
        if norm in ALIAS_MAP:
            target = ALIAS_MAP[norm]
            rename_dict[col] = target
            original_to_canonical[col] = target
        else:
            for alias_key, target in ALIAS_MAP.items():
                if alias_key in norm:
                    rename_dict[col] = target
                    original_to_canonical[col] = target
                    break
            if col not in rename_dict:
                original_to_canonical[col] = col

    renamed_df = df.rename(columns=rename_dict)
    return renamed_df, original_to_canonical

def validate_features(df: pd.DataFrame) -> Tuple[bool, List[str], List[str]]:
    missing = [feat for feat in CANONICAL_FEATURES if feat not in df.columns]
    present = [feat for feat in CANONICAL_FEATURES if feat in df.columns]
    return len(missing) == 0, present, missing

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df_clean = df.copy()
    for col in df_clean.columns:
        if col in CANONICAL_FEATURES:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
            df_clean[col] = df_clean[col].replace([np.inf, -np.inf], np.nan)
            col_median = df_clean[col].median()
            if pd.isna(col_median):
                col_median = 0.0
            df_clean[col] = df_clean[col].fillna(col_median)
    return df_clean
