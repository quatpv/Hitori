import * as React from 'react'
import type { NextPage } from 'next'
import { Matrix } from '../components/pages/home/Matrix/Matrix'
import axios from 'axios'
import { useMutation } from 'react-query'
import { samples } from '../components/pages/home/Matrix/samples'

interface Payload {
  rows: number
  cols: number
  data: MatrixData
  method: 'CC' | 'CE'
}

type Solution = boolean[][]

interface Response {
  ok: boolean
  result: Solution
  running_time: number
  number_of_clauses: number
  number_of_variables: number
}

const solveHitoriProblem = async (payload: Payload) => {
  const response = await axios.post<Response>(
    'http://localhost:8000/hitori-solver',
    payload,
  )
  return response.data
}

type MatrixData = number[][]

const Home: NextPage = () => {
  const [payload, setPayload] = React.useState<Payload | null>(null)
  const [response, setResponse] = React.useState<Response>({
    ok: false,
    result: [],
    running_time: 0,
    number_of_clauses: 0,
    number_of_variables: 0,
  })

  const solverMutation = useMutation(solveHitoriProblem)

  return (
    <main className="h-screen w-full flex">
      <aside className="h-full flex-1 border-4 justify-center p-4 overflow-y-scroll">
        <p className="text-2xl font-bold p-2 text-center">Sample Matrix</p>
        {samples.map((sample, index) => (
          <>
            <p className="text-center text-xl bg-gray-300 border-2 rounded-md p-2">{`${sample.length} x ${sample.length}`}</p>
            <Matrix
              tableClass="w-full"
              data={sample}
              key={index}
              onClick={() => {
                setPayload({
                  data: sample,
                  rows: sample.length,
                  cols: sample[0].length,
                  method: 'CC',
                })
                setResponse({
                  ok: false,
                  running_time: 0,
                  number_of_clauses: 0,
                  number_of_variables: 0,
                  result: new Array(sample.length)
                    .fill(true)
                    .map(() => new Array(sample[0].length).fill(true)),
                })
              }}
            />
          </>
        ))}
      </aside>
      <div className="h-full flex-3 border-4 flex flex-col items-center p-4">
        <p className="text-2xl font-bold p-2 text-center">Hitori Solver</p>
        {payload && (
          <>
            <div className="w-full flex justify-center h-3/5 overflow-y-scroll">
              <Matrix
                data={payload.data}
                solution={response.result}
                tableClass="w-3/5"
              />
            </div>
            <div className="flex w-full h-60 border-t-2">
              <div className="flex-1 py-8 px-24">
                <p className="text-2xl font-bold text-center mb-4">
                  Payload Information
                </p>
                <p className="text-xl">
                  Rows -{' '}
                  <span className="font-bold leading-8">{payload.rows}</span>
                </p>
                <p className="text-xl">
                  Columns -{' '}
                  <span className="font-bold leading-8">{payload.cols}</span>
                </p>
                <p className="text-xl leading-8">Method: </p>
                <select
                  className="h-10 text-lg border-2 rounded-sm my-2"
                  value={payload.method}
                  onChange={(e) => {
                    setPayload(
                      (prevPayload) =>
                        ({
                          ...prevPayload,
                          method: e.target.value,
                        } as Payload),
                    )
                  }}
                >
                  <option value="CC">Chains and Cycles</option>
                  <option value="CE">Connectivity Encoding</option>
                </select>
                <button
                  className="block text-xl text-center w-40 p-2 rounded-md bg-green-500 text-white font-bold"
                  disabled={solverMutation.isLoading}
                  onClick={async () => {
                    const res = await solverMutation.mutateAsync(payload)
                    if (res.ok) {
                      setResponse(res)
                    }
                  }}
                >
                  {solverMutation.isLoading ? 'Solving...' : 'Solve'}
                </button>
              </div>
              <div className="flex-1 py-8 px-24 border-l-2">
                <p className="text-2xl font-bold text-center mb-4">
                  Statistic Results
                </p>
                <p className="text-xl">
                  Running time:{' '}
                  <span className="font-bold leading-8">
                    {response.running_time}
                  </span>
                  {' (ms)'}
                </p>
                <p className="text-xl">
                  Number of clauses:{' '}
                  <span className="font-bold leading-8">
                    {response.number_of_clauses}
                  </span>
                </p>
                <p className="text-xl">
                  Number of variables:{' '}
                  <span className="font-bold leading-8">
                    {response.number_of_variables}
                  </span>
                </p>
              </div>
            </div>
          </>
        )}
      </div>
    </main>
  )
}

export default Home
