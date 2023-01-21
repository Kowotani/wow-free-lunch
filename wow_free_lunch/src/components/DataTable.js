import { useEffect, useState } from "react"
import { 
  Box,
  Icon,
  ScaleFade,
  Table, 
  Thead, 
  Tbody, 
  Tr, 
  Th, 
  Td, 
  VStack
} from "@chakra-ui/react"

import {
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getSortedRowModel
} from "@tanstack/react-table"
import { createTable } from '@tanstack/table-core';

import { TiArrowSortedDown, TiArrowSortedUp } from 'react-icons/ti'

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

export const DataTable = (
  { data, columns, hiddenColumns, inputColumnFilters, 
    enableShowAllMessage
  }) => {
  
  const [sorting, setSorting] = useState([]);
  const [columnFilters, setColumnFilters] = useState(inputColumnFilters);

  // set default column visibility
  const [columnVisibility, setColumnVisibility] = useState(
    Object.fromEntries(hiddenColumns.map(x => [x, false])));
  
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

  useEffect(() => {
    setColumnVisibility(
      Object.fromEntries(hiddenColumns.map(x => [x, false])));
  }, [hiddenColumns])

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
                  p='14px'
                >
                  <Box display='flex' alignItems='center' justifyContent={meta?.isNumeric ? 'flex-end': 'flex-begin'}>
                    <Box height='16px'>
                      {header.column.getIsSorted() && meta?.isNumeric ? (
                          header.column.getIsSorted() === "asc" 
                            ? <Icon as={TiArrowSortedUp} boxSize='16px' color='gray.500'/> 
                            : <Icon as={TiArrowSortedDown} boxSize='16px' color='gray.500'/> 
                        ) : null
                      }
                    </Box>
                    <Box>
                    {
                      header.column.columnDef.header
                    /*{flexRender(
                      header.column.columnDef.header,
                      header.getContext()
                    )}*/
                    }
                    </Box>
                    <Box height='16px'>
                      {header.column.getIsSorted() && !meta?.isNumeric ? (
                          header.column.getIsSorted() === "asc" 
                            ? <Icon as={TiArrowSortedUp} boxSize='16px' color='gray.500'/>
                            : <Icon as={TiArrowSortedDown} boxSize='16px' color='gray.500'/>
                        ) : null
                      }
                    </Box>
                  </Box>
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
                    <Td key={cell.id} isNumeric={meta?.isNumeric} p='14px'>
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
          delay={0.4}
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
            <VStack>
              <Box>No free lunches found</Box>
              {enableShowAllMessage && (
                <Box>Click the 
                  <Box 
                    display='inline' 
                    background='pink.500' 
                    color='white' 
                    borderRadius='md'
                    p='2px 6px'
                    m='6px'
                  >
                  Show All
                  </Box> 
                  button above to view all craftable items
                </Box>
              )}
            </VStack>
          </Box>
        </ScaleFade>
      )
    }
    </>
  )
}