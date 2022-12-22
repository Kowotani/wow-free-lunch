import { useContext, useEffect, useState } from 'react';
import {
  Box,
  Button, 
  ButtonGroup,
  Image,
  Input,
  InputGroup,
  Link,
  Progress, 
  Spacer,
} from '@chakra-ui/react';

import { createColumnHelper } from "@tanstack/react-table";

import Cookies from 'js-cookie'
import { Data } from 'dataclass';

import { DataTable } from './DataTable';
import { PriceBox } from './PriceBox';

import { ProfessionContext } from '../state/ProfessionContext';
import { ReagentPricesContext } from '../state/ReagentPricesContext';


// =======
// Classes 
// =======

class Reagent extends Data {
  
  // metadata
  name = '';
  item_id = 0;
  media_url = '';
  quantity = 0;
  price = 0;
  
}

// Free Lunch data class
class FreeLunch extends Data {
  
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


// return WoWHead url formatted with item_id
function getWowHeadeUrl(item_id) {
  return `https://www.wowhead.com/wotlk/item=${item_id}/`
}


// return text color for an item given the input quality
function getItemQualityColor(quality) {
  switch (quality) {
    
    case 'COMMON':
      return 'black'
      
    case 'UNCOMMON':
      return '#1eff00'
      
    case 'RARE':
      return '#0070dd'
      
    case 'EPIC': 
      return '#a335ee'
    
    default:
      return 'black'
  }
}


// DataTable component
const FreeLunchTable = (props) => {
  
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
          <Link href={getWowHeadeUrl(props.row.getValue('item_id'))} isExternal>
            <Image src={props.getValue()} height='48px' width='48px' border='4px solid cyan' />
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
            href={getWowHeadeUrl(props.row.getValue('item_id'))} 
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
                <PriceBox price={props.getValue()}/>
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
                  <PriceBox price={props.getValue()}/>
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
                {(props.getValue() * 100).toFixed(2)}%
              </Box>
            }
          </>
        )
      },
      header: 'Percent Profit',
      meta: {
        isNumeric: true
      },
      sortingFn: 'basic'
    })
  ];

  // hide certain columns by default
  const hiddenColumns = ['item_id', 'insufficient_data', 'quality'];
  
  
  // ----------------
  // filtered columns
  // ----------------
  
  // // default to only profitable crafted items
  // const defaultColumnFilters = [
  //   {
  //     id: 'unit_profit', 
  //     value: [1, 999999]
  //   }
  // ]
  
  return (
    <DataTable 
      columns={columns} 
      data={props.data} 
      hiddenColumns={hiddenColumns}
      inputColumnFilters={props.columnFilters}
    />
  )
}


// ==============
// Main Component
// ==============


// Free Lunches content
const FreeLunchesContent = () => {
  
  const { reagentPrices } = useContext(ReagentPricesContext);
  const { profession } = useContext(ProfessionContext);
  
  const [ craftedItemRecipes, setCraftedItemRecipes] = useState({});
  const [ freeLunchData, setFreeLunchData] = useState({});
  const [ columnFilters, setColumnFilters] = useState([]);
  
  const [ isLoading, setIsLoading ] = useState(true);
  
  useEffect(() => {
  
    // query recipe data

    // async data fetch
    const fetchData = async() => {
      
      setIsLoading(true);
      
      console.log('fetching /api/crafted_item_recipes ...', profession);
      
      // prepare config
      const url = '/api/crafted_item_recipes';

      const config = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': Cookies.get('csrftoken'),
        },
        body: JSON.stringify({
          profession: profession.name
        })
      };
      
      // get response
      const res = await fetch(url, config)
      
      // convert to json
      const data = await res.json();
      console.log('retrieved /api/crafted_item_recipes: ', data);
      
      // update state
      setCraftedItemRecipes(data['data']);
      setIsLoading(false);
    };
    
    // invoke function
    fetchData()
      .catch(console.error);

  }, [profession]);
  
  
  useEffect(() => {
    
    // calculate Free Lunch data

    const data = (Object.keys(craftedItemRecipes).length > 0
        && Object.keys(reagentPrices['by_item_id']).length > 0) 
      ? craftedItemRecipes.map((item) => {
      
      // identify cases where there is not enough price data
      let insufficientData = false;
      
      // construct Reagents param
      const reagents = item.reagents.map((reagent) => {
        
        if (reagentPrices['by_item_id'][reagent.item_id] === 0) {
          insufficientData = true;
        }
        
        return Reagent.create({
          name: reagent.name,
          item_id: reagent.item_id,
          media_url: reagent.media_url,
          quantity: reagent.quantity,
          price: reagentPrices['by_item_id'][reagent.item_id]
        })
      })
      
      
      const cost = insufficientData ? 0 : reagents.reduce(
        (total, item) => total + item.quantity * item.price, 0
      );
      
      // construct FreeLunch
      const freeLunch = FreeLunch.create({
        name: item.name,
        item_id: item.item_id,
        quality: item.quality,
        media_url: item.media_url,
        reagents: reagents,
        vendor_price: item.vendor_price,
        cost: cost,
        unit_profit: insufficientData ? 0 : item.vendor_price - cost,
        percent_profit: insufficientData ? 0 : item.vendor_price / cost - 1,
        insufficient_data: insufficientData
      })
      
      return freeLunch
    }) : {}
    
    console.log('data: ', data)
    
    // update state
    setFreeLunchData(data);
  }, [craftedItemRecipes, reagentPrices])


  // manage updating the FreeLunch table filters
  // filterColumn === null -> remove all filters
  // filterValue === null -> remove that filterColumn
  function updateColumnFilters(filterColumn = null, filterValue = null) {
    
    const newColumnFilters = [];
    
    // modify a single column filter, otherwise reset all filters
    if (filterColumn !== null) {
    
      // update 
      for (const obj of columnFilters) {
        if (obj.id !== filterColumn) {
          newColumnFilters.push(obj)
        }
      }
      if (filterValue !== null) {
        newColumnFilters.push({
          id: filterColumn, 
          value: filterValue
        });
      }
    }
    
    // update state
    console.log('new filters: ', newColumnFilters)
    setColumnFilters(newColumnFilters);
  }


  // handler for Item Name search input
  function handleItemNameSearchChange(e) {
    if (e.target.value.length >= 3) {
      updateColumnFilters('name', e.target.value);
    } else if (e.target.value.length === 0) {
      updateColumnFilters('name', null);
    }
  }
  
  return (
    <>
      <Box display='block' bg='cyan.300' p='10px 14px'>
        Free Lunches
      </Box>
      <Box display='flex' alignItems='center' flexWrap='wrap'>
          <ButtonGroup colorScheme='pink' p='14px' spacing='2'>
            <Button onClick={() => {updateColumnFilters()}}>
              Show All
            </Button>
            <Button 
              onClick={() => {updateColumnFilters('unit_profit', [1, 999999])}}
            >
              Show Profitable
            </Button>
          </ButtonGroup>
          <Spacer />
          <InputGroup width='200px' p='14px'>
            <Input 
              type='search' 
              placeholder='Item name'
              onChange={(e) => handleItemNameSearchChange(e)}
            />
          </InputGroup>
        </Box>
      {isLoading && 
        <Box display='block' alignItems='center' flexWrap='wrap'>
          <Progress isIndeterminate />
        </Box>
      }
      {!isLoading && 
        <Box display='block'>
          <FreeLunchTable 
            data={freeLunchData} 
            columnFilters={columnFilters}
          />
        </Box>
      }
    </>
  )
}


// Free Lunches component
export const FreeLunches = () => {
  
  return (
    <FreeLunchesContent />
  )
}
