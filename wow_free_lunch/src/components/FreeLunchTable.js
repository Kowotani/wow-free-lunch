import {
  Box,
  Image,
  Link,
  Spinner,
} from '@chakra-ui/react';

import { createColumnHelper } from "@tanstack/react-table";

import { Data } from 'dataclass';

import { DataTable } from './DataTable';
import { PriceBox } from './PriceBox';

import { getWowHeadUrl, getItemQualityColor } from '../utils';


// =======
// Classes 
// =======


export class Reagent extends Data {
  
  // metadata
  name = '';
  item_id = 0;
  media_url = '';
  quantity = 0;
  price = 0;
  
}


// Free Lunch data class
export class FreeLunch extends Data {
  
    // metadata
    name = '';
    item_id = 0;
    quality = '';
    media_url = '';
    reagents = [];  // list of Reagent objects
    vendor_price = 0;
    cost = 0;
    unit_profit = 0;
    percent_profit = 0;
    insufficient_data = false;
    
}


// ================
// Free Lunch Table
// ================


// spinner component
const TableSpinner = () => {
  return (
    <Spinner
      thickness='4px'
      size='lg'
      speed='1s'
      emptyColor='gray.200'
      color='blue.500'
    />
  )
}


// DataTable component
export const FreeLunchTable = (props) => {
  
  // Define columns
  const columnHelper = createColumnHelper();
  const columns = [


    // --------------
    // hidden columns
    // --------------

    // item id
    columnHelper.accessor('item_id', {
      id: 'item_id',
      cell: (props) => props.getValue(),
      header: 'Item ID',
      enableHiding: true,
      meta: {
        isNumeric: true
      }
    }),

    // insufficient data
    columnHelper.accessor('insufficient_data', {
      id: 'insufficient_data',
      cell: (props) => {
        return (
          <Box>
            {props.getValue() ? 'True': 'False'}
          </Box>
        )
      },
      header: 'Insufficient Data',
      enableHiding: true,
    }),
    
    // quality
    columnHelper.accessor('quality', {
      id: 'quality',
      cell: (props) => {
        return (
          <Box>
            {props.getValue()}
          </Box>
        )
      },
      header: 'Quality',
      enableHiding: true,
    }),
    
    
    // ---------------
    // visible columns
    // ---------------
    
    // item icon
    columnHelper.accessor('media_url', {
      cell: (props) => {
        return (
          <Link href={getWowHeadUrl(props.row.getValue('item_id'))} isExternal>
            <Image src={props.getValue()} height='48px' width='48px' border='4px solid cyan' minWidth='48px'/>
          </Link>
        )
      },
      header: 'Icon',
      enableSorting: false
    }),
    
    // item name
    columnHelper.accessor('name', {
      id: 'name',
      cell: (props) => {
        return (
          <Link
            color={getItemQualityColor(props.row.getValue('quality'))}
            href={getWowHeadUrl(props.row.getValue('item_id'))} 
            isExternal
          >
            {props.getValue()}
          </Link>
        )
      },
      header: 'Item'
    }),
    
    // vendor price
    columnHelper.accessor('vendor_price', {
      cell: (props) => {
        return (
          <Box display='flex' justifyContent='flex-end'>
            <PriceBox price={props.getValue()}/>
          </Box>
        )
      },
      header: 'Vendor Price',
      meta: {
        isNumeric: true
      }
    }),    
    
    // estimated cost
    columnHelper.accessor('cost', {
      cell: (props) => {
        return (
          <>
            {!props.row.getValue('insufficient_data') &&
              <Box display='flex' justifyContent='flex-end'>
                {isNaN(props.getValue())
                  ? null
                  : <PriceBox price={props.getValue()}/>
                }
              </Box>
            }
          </>
        )
      },
      header: 'Cost',
      meta: {
        isNumeric: true
      }
    }),
    
    // unit profit
    columnHelper.accessor('unit_profit', {
      id: 'unit_profit',
      cell: (props) => {
        return (
          <>
            {props.row.getValue('insufficient_data')
              ? (
                  <Box display='flex' justifyContent='flex-end'>
                    Insufficient Data
                  </Box>
              ) : (
                <Box display='flex' justifyContent='flex-end'>
                  {isNaN(props.getValue())
                    ? <TableSpinner />
                    : <PriceBox price={props.getValue()}/>
                  }
                </Box>
              )
            }
          </>
        )
      },
      header: 'Unit Profit',
      meta: {
        isNumeric: true
      },
      sortingFn: 'basic',
      filterFn: 'inNumberRange',
      enableColumnFilter: true
    }),
    
    // percent profit
    columnHelper.accessor('percent_profit', {
      cell: (props) => {
        return (
          <>
            {!props.row.getValue('insufficient_data') &&
              <Box color={props.getValue() < 0 ? 'red' : 'black'}>
                {isNaN(props.getValue()) 
                  ? null 
                  : (props.getValue() * 100).toFixed(2) + '%'
                }
              </Box>
            }
          </>
        )
      },
      header: 'Profit Margin',
      meta: {
        isNumeric: true
      },
      sortingFn: 'basic'
    })
  ];

  // hide certain columns by default
  const hiddenColumns = ['item_id', 'insufficient_data', 'quality'];
  
  
  return (
    <DataTable 
      columns={columns} 
      data={props.data} 
      hiddenColumns={hiddenColumns}
      inputColumnFilters={props.columnFilters}
      enableShowAllMessage={props.enableShowAllMessage}
    />
  )
}