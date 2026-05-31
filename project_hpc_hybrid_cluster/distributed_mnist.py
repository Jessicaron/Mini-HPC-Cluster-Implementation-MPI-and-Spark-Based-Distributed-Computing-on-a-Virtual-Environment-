from mpi4py import MPI
from sklearn.datasets import load_digits
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
    digits = load_digits()
    X = digits.data
    y = digits.target
else:
    X = None
    y = None

X = comm.bcast(X, root=0)
y = comm.bcast(y, root=0)

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
    print("Scores from all nodes:", scores)
    print("Average score:", sum(scores) / len(scores))
