import * as React from 'react'
import { Cell } from './Cell'

interface MatrixProps {
  data: number[][]
  onClick?(): void
  tableClass?: string
  solution?: boolean[][]
}

export const Matrix = ({
  data,
  tableClass = '',
  onClick = () => {},
  solution = data.map((row) => new Array(row.length).fill(true)),
}: MatrixProps) => {
  return (
    <table
      className={`my-4 cursor-pointer hover:bg-gray-200 ${tableClass}`}
      onClick={onClick}
    >
      {data.map((row, i) => (
        <tr key={i}>
          {row.map((item, j) => (
            <Cell
              key={`row-${i}-col-${j}`}
              value={item}
              isBold={!solution[i][j]}
            />
          ))}
        </tr>
      ))}
    </table>
  )
}
