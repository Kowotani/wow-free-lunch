import { useContext, useEffect, useRef, useState } from "react"
import { 
  Box,
  ScaleFade,
  Table, 
  Thead, 
  Tbody, 
  Tr, 
  Th, 
  Td, 
  chakra 
} from "@chakra-ui/react"
// import { TriangleDownIcon, TriangleUpIcon } from "@chakra-ui/icons"
import {
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getSortedRowModel
} from "@tanstack/react-table"
import { createTable } from '@tanstack/table-core';

import { CraftedItemRecipesContext } from '../state/CraftedItemRecipesContext';
import { FreeLunchesContext } from '../state/FreeLunchesContext';
import { ReagentPricesContext } from '../state/ReagentPricesContext';


// ===========
// React Table
// ===========

function GetReactTable(options) {
  
  // Compose in the generic options to the user options
  const resolvedOptions = {
    state: {}, // Dummy state
    onStateChange: () => {}, // noop
    renderFallbackValue: null,
    ...options
  }

  // Create a new table and store it in state
  const [tableRef] = useState(() => ({
    current: createTable(resolvedOptions)
  }))

  // By default, manage table state here using the table's initial state
  const [state, setState] = useState(() => tableRef.current.initialState)

  // Compose the default state above with any user state. This will allow the user
  // to only control a subset of the state if desired.
  tableRef.current.setOptions(prev => ({
    ...prev,
    ...options,
    state: {
      ...state,
      ...options.state
    },
    // Similarly, we'll maintain both our internal state and any user-provided
    // state.
    onStateChange: updater => {
      setState(updater)
      options.onStateChange?.(updater)
    }
  }))

  return tableRef.current
}


// ==========
// Data Table
// ==========

export const DataTable = ({ data, columns, hiddenColumns, inputColumnFilters }) => {
  
  const [sorting, setSorting] = useState([]);
  const [columnFilters, setColumnFilters] = useState(inputColumnFilters);
  
  const { craftedItemRecipes } = useContext(CraftedItemRecipesContext);
  const { freeLunches } = useContext(FreeLunchesContext);
  const { reagentPrices } = useContext(ReagentPricesContext);  
  
  // set default column visibility
  const [columnVisibility, setColumnVisibility] = useState(
    Object.fromEntries(hiddenColumns.map(x => [x, false])));
  
  // ref for no Free Lunch message 
  const noFreeLunchRef = useRef(null);
  
  const table = GetReactTable({
    columns,
    data,
    getCoreRowModel: getCoreRowModel(),
    onSortingChange: setSorting,
    getSortedRowModel: getSortedRowModel(),
    onColumnVisibilityChange: setColumnVisibility,
    getFilteredRowModel: getFilteredRowModel(),
    state: {
      sorting,
      columnVisibility,
      columnFilters
    }
  });

  useEffect(() => {
    setColumnFilters(inputColumnFilters)
  }, [inputColumnFilters]);  

  // console.log('data: ', table.getCoreRowModel().rows.length, 'filtered: ', table.getFilteredRowModel().rows.length)
  console.log('freeLunches is loading: ', freeLunches['is_loading'])

  return (
    <>
    <Table>
      <Thead>
        {table.getHeaderGroups().map(headerGroup => (
          <Tr key={headerGroup.id}>
            {headerGroup.headers.map(header => {
              // see https://tanstack.com/table/v8/docs/api/core/column-def#meta to type this correctly
              const meta = header.column.columnDef.meta
              return (
                <Th
                  key={header.id}
                  onClick={header.column.getToggleSortingHandler()}
                  isNumeric={meta?.isNumeric}
                >
                  <chakra.span>
                    {header.column.getIsSorted() && meta?.isNumeric ? (
                        header.column.getIsSorted() === "asc" ? '🔼' :'🔽'
                      ) : null
                    }
                  </chakra.span>                
                  {flexRender(
                    header.column.columnDef.header,
                    header.getContext()
                  )}
                  <chakra.span>
                    {header.column.getIsSorted() && !meta?.isNumeric ? (
                        header.column.getIsSorted() === "asc" ? '🔼' :'🔽'
                      ) : null
                    }
                  </chakra.span>
                </Th>
              )
            })}
          </Tr>
        ))}
      </Thead>
      <Tbody>
        {table.getRowModel().rows.map(
            row => (
              <Tr key={row.id}>
                {row.getVisibleCells().map(cell => {
                  // see https://tanstack.com/table/v8/docs/api/core/column-def#meta to type this correctly
                  const meta = cell.column.columnDef.meta
                  return (
                    <Td key={cell.id} isNumeric={meta?.isNumeric}>
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </Td>
                  )
                })}
              </Tr> 
            )
          )
        }
      </Tbody>
    </Table>
    {table.getFilteredRowModel().rows.length === 0 
      && (
        <ScaleFade 
          initialScale={0.8} 
          in={true} 
          delay={0.3}
          transition={{
            enter: { duration: 0.5 }
          }}
        >
          <Box 
            display='flex' 
            alignItems='center' 
            justifyContent='center' 
            textAlign='center' 
            p='10px' 
            background='gray.200'
          >
            No free lunches found <br/>
            Click the Show All button to view all craftable items
          </Box>
        </ScaleFade>
      )
    }
    </>
  )
}