import React from 'react'
import clsx from 'clsx'

interface CellProps {
  value: number
  isBold?: boolean
}

export const Cell = ({ value, isBold = false }: CellProps) => {
  return (
    <td
      className={`${clsx({
        ['text-white']: isBold,
        ['bg-black']: isBold,
      })} border-4 border-gray-600 flex-1 p-1 text-center`}
    >
      {value}
    </td>
  )
}
