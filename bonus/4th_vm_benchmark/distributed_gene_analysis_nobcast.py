from mpi4py import MPI
import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

possible_paths = [
    "leukemia_expression.csv",
    "bioinfo_data/leukemia_expression.csv",
    "/tmp/hpc/leukemia_expression.csv",
    "/home/abdo/spark_job/leukemia_expression.csv"
]

data_path = None
for path in possible_paths:
    if os.path.exists(path):
        data_path = path
        break

if data_path is None:
    raise FileNotFoundError("leukemia_expression.csv was not found.")

data = pd.read_csv(data_path)

X = data.iloc[:, :-1].values
y = data.iloc[:, -1].astype(int).values

chunks_X = np.array_split(X, size)
chunks_y = np.array_split(y, size)

local_X = chunks_X[rank]
local_y = chunks_y[rank]

X_train, X_test, y_train, y_test = train_test_split(
    local_X, local_y, test_size=0.3, random_state=42
)

model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X_train, y_train)

local_score = model.score(X_test, y_test)
scores = comm.gather(local_score, root=0)

if rank == 0:
    print("Bioinformatics scores from all nodes:", scores)
    print("Average score:", sum(scores) / len(scores))
