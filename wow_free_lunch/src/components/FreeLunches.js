import { useContext, useEffect, useMemo, useState } from 'react';
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
  Spinner,
} from '@chakra-ui/react';

import { createColumnHelper } from "@tanstack/react-table";

import Cookies from 'js-cookie'
import { Data } from 'dataclass';

import { DataTable } from './DataTable';
import { PriceBox } from './PriceBox';

import { CraftedItemRecipesContext } from '../state/CraftedItemRecipesContext';
import { FreeLunchesContext } from '../state/FreeLunchesContext';
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
  
  const { craftedItemRecipes, setCraftedItemRecipes} = useContext(CraftedItemRecipesContext);
  const { freeLunches, setFreeLunches} = useContext(FreeLunchesContext);
  const { profession } = useContext(ProfessionContext);
  const { reagentPrices } = useContext(ReagentPricesContext);
  
  const [ columnFilters, setColumnFilters ] = useState([]);
  const [ searchValue, setSearchValue ] = useState('');
  
  
  useEffect(() => {
  
    // query recipe data

    // async data fetch
    const fetchData = async() => {
      
      const loadingCraftedItemRecipesState = {
        is_loading: true,
        recipes: craftedItemRecipes['recipes']
      };
      setCraftedItemRecipes(loadingCraftedItemRecipesState);
      
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
      const loadedCraftedItemRecipesState = {
        is_loading: false,
        recipes: data['data']
      };
      setCraftedItemRecipes(loadedCraftedItemRecipesState);      
    };
    
    // invoke function
    fetchData()
      .catch(console.error);

  }, [profession]);
  
  
  useEffect(() => {
    
    // calculate Free Lunch data

    const loadingFreeLunchesState = {
      is_loading: true,
      free_lunches: freeLunches['free_lunches']
    };
    setFreeLunches(loadingFreeLunchesState);

    const freeLunchData = (craftedItemRecipes['recipes'].length > 0
        && Object.keys(reagentPrices['by_item_id']).length > 0) 
      ? craftedItemRecipes['recipes'].map((item) => {
      
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
    }) : []
    
    console.log('FreeLunch data: ', freeLunchData)
    
    // update state
    const loadedFreeLunchesState = {
      is_loading: false,
      free_lunches: freeLunchData
    };
    setFreeLunches(loadedFreeLunchesState);      

  }, [craftedItemRecipes['recipes'], reagentPrices])


  useEffect(() => {
    
    // debounce search value
    
    const timeout = searchValue.length === 0 ? 0 : 1000;
    console.log('debouncing by: ', timeout)
    const updateSearchValue = setTimeout(() => {
      updateColumnFilters('name', searchValue)
    }, timeout)
    
    return () => clearTimeout(updateSearchValue)
  }, [searchValue])


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


  // function to show all Free Lunches (eg. remove all filters)
  function showAllFreeLunches() {
    setSearchValue('');
    updateColumnFilters();
  }
  
  const freeLunchTable = useMemo(() => (
    <FreeLunchTable 
      data={freeLunches['free_lunches']} 
      columnFilters={columnFilters}
    />    
  ), [freeLunches['free_lunches'], columnFilters])
  
  
  return (
    <>
      <Box display='block' bg='cyan.300' p='10px 14px'>
        Free Lunches
      </Box>
      <Box display='flex' alignItems='center' flexWrap='wrap'>
        <ButtonGroup colorScheme='pink' p='14px' spacing='2'>
          <Button onClick={() => {showAllFreeLunches()}}>
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
            value={searchValue}
            type='search' 
            placeholder='Item name'
            onChange={(e) => setSearchValue(e.target.value)}
          />
        </InputGroup>
      </Box>
      {(reagentPrices['is_loading'] || craftedItemRecipes['is_loading'] || freeLunches['is_loading']) && 
        <Box display='block' alignItems='center' flexWrap='wrap'>
          <Progress isIndeterminate />
        </Box>
      }
      {!(reagentPrices['is_loading'] || craftedItemRecipes['is_loading'] || freeLunches['is_loading']) &&
        <Box display='block'>
          {freeLunchTable}
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
