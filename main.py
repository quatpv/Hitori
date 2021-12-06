from solver.hitory import HirotySAT
import json
import time
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

configs = json.load(open('configs.json', 'r'))


def hitory_solver(n, value, configs, method):
    rows = n
    columns = n
    start_time = time.time()
    alg = HirotySAT(rows, columns, value, configs, method=method)
    alg.encode()
    alg.decode()
    end_time = time.time()
    running_time = end_time - start_time

    if alg.satisfiable:
        print("running time: ", running_time)
        print("number_of_clauses: ", alg.number_of_clauses)
        print("number_of_variables: ", alg.number_of_variables)
        print(alg.result)
    else:
        print("No solution")

    return {
        "ok": alg.satisfiable,
        "running_time": running_time,
        "number_of_clauses": alg.number_of_clauses,
        "number_of_variables": alg.number_of_variables,
        "result": alg.result.tolist(),
    }


class Payload(BaseModel):
    rows: int
    cols: int
    method: str
    data: List[List[int]]


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/hitori-solver")
def get_solution(payload: Payload):
    return hitory_solver(payload.rows, payload.data, configs, payload.method)
