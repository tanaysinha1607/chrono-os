import pandas as pd
import numpy as np
import json

LOG_FILE = 'app_usage_log.csv' 
SESSION_TIMEOUT_MINUTES = 15
SEQUENCE_LENGTH = 5 

df = pd.read_csv(LOG_FILE)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.dropna().sort_values('timestamp')

IGNORE_APPS = ['explorer.exe', 'Finder', 'Window Manager', 'TextInputHost.exe']
df = df[~df['app_name'].isin(IGNORE_APPS)]

df['time_diff'] = df['timestamp'].diff().dt.total_seconds() / 60
df['session_id'] = (df['time_diff'] > SESSION_TIMEOUT_MINUTES).cumsum()

unique_apps = df['app_name'].unique().tolist()
app_to_int = {app: i for i, app in enumerate(unique_apps)}
int_to_app = {i: app for i, app in enumerate(unique_apps)}
vocab_size = len(unique_apps)

with open('app_vocab.json', 'w') as f:
    json.dump(app_to_int, f)

print(f"Vocabulary created with {vocab_size} unique apps.")

df['app_int'] = df['app_name'].map(app_to_int)

sequences = []
for session_id, group in df.groupby('session_id'):
    app_ints = group['app_int'].tolist()
    if len(app_ints) > SEQUENCE_LENGTH:
        for i in range(len(app_ints) - SEQUENCE_LENGTH):
            seq = app_ints[i:i + SEQUENCE_LENGTH + 1]
            sequences.append(seq)

print(f"Generated {len(sequences)} sequences.")

sequences = np.array(sequences)
X = sequences[:, :-1] 
y = sequences[:, -1]  

print("Data shape (X):", X.shape) 
print("Data shape (y):", y.shape) 

np.savez('processed_data.npz', X=X, y=y, vocab_size=np.array([vocab_size]))
print("Preprocessing complete. Data saved to processed_data.npz")