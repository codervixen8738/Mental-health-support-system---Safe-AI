import pandas as pd

df = pd.read_csv("real_data.csv", skiprows=3, header=None, names=['PTSD', 'Age', 'Ethnicity', 'Marital status', 'Religion', 'Education', 'IMC'])

# Convert numeric columns
df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
df['IMC'] = pd.to_numeric(df['IMC'], errors='coerce')
df['PTSD'] = pd.to_numeric(df['PTSD'], errors='coerce')

# Drop IDs if present
df = df.drop(columns=["participant_id"], errors="ignore")

# Drop rows with NaN in key columns
df = df.dropna(subset=['Age', 'IMC', 'PTSD'])

def assign_risk(row):
    score = row['Age'] + row['IMC']
    
    if score < 40:
        return 0  # Low
    elif score < 50:
        return 1  # Medium
    else:
        return 2  # High

df['risk_level'] = df.apply(assign_risk, axis=1)

from imblearn.over_sampling import SMOTE

X = df[['Age', 'IMC']]
y = df["risk_level"]

smote = SMOTE(
    sampling_strategy={0:1500, 1:1700, 2:1800},
    random_state=42
)

X_smote, y_smote = smote.fit_resample(X, y)

df_smote = pd.DataFrame(X_smote, columns=X.columns)
df_smote["risk_level"] = y_smote

import numpy as np

noise_df = df.sample(500, replace=True).copy()

clinical_cols = [
    'Age', 'IMC'
]

for col in clinical_cols:
    noise_df[col] += np.random.normal(
        loc=0,
        scale=noise_df[col].std() * 0.05,
        size=len(noise_df)
    )

final_df = pd.concat([df_smote, noise_df], axis=0)
final_df = final_df.sample(frac=1, random_state=42).reset_index(drop=True)

print(final_df.shape)

final_df.to_csv("processed_real_data.csv", index=False)