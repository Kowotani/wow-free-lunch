import { useContext, useEffect, useState } from 'react';
import {
  Box,
  Button, 
  ButtonGroup,
  Image,
  Input,
  InputGroup,
  Link,
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
    
    // // calculate estimated cost
    // getCost() {
    //   return 123;
    // }
    
    // // calculate estimated unit profit
    // getUnitProfit() {
    //   return this.vendor_price - this.getCost();
    // }
    
    // // calculate estimated percent profit
    // getPercentProfit() {
    //   return Math.Round(this.getUnitProfit() / this.getCost(), 4);
    // }

}


// =======
// Filters 
// =======

// component for Free Lunches filters
const FreeLunchesFilters = () => {
  
  // const { priceType, setPriceType } = useContext(PriceTypeContext);
  
  return (
    <Box display='flex' alignItems='center' flexWrap='wrap'>
      <ButtonGroup colorScheme='pink' p='14px' spacing='2'>
        <Button>Show All</Button>
        <Button>Show Profitable Only</Button>
      </ButtonGroup>
      <Spacer />
      <InputGroup width='200px' p='14px'>
        <Input type='search' placeholder='Crafted item name' />
      </InputGroup>
    </Box>
  )
}


// ================
// Free Lunch Table
// ================


// return WoWHead url formatted with item_id
function getWowHeadeUrl(item_id) {
  return `https://www.wowhead.com/wotlk/item=${item_id}/`
}


// DataTable component
const FreeLunchTable = (props) => {
  
  // Define columns
  const columnHelper = createColumnHelper();
  const columns = [
    
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
    
    // item name
    columnHelper.accessor('name', {
      cell: (props) => {
        return (
          <Link href={getWowHeadeUrl(props.row.getValue('item_id'))} isExternal>
            {props.getValue()}
          </Link>
        )
      },
      header: 'Item'
    }),
    
    // estimated cost
    columnHelper.accessor('cost', {
      cell: (props) => {
        return (
          <Box display='flex' justifyContent='flex-end'>
            <PriceBox price={props.getValue()}/>
          </Box>
        )
      },
      header: 'Cost',
      meta: {
        isNumeric: true
      }
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
    
    // unit profit
    columnHelper.accessor('unit_profit', {
      cell: (props) => {
        return (
          <Box display='flex' justifyContent='flex-end'>
            <PriceBox price={props.getValue()}/>
          </Box>
        )
      },
      header: 'Unit Profit',
      meta: {
        isNumeric: true
      },
      sortingFn: 'basic'
    }),
    
    // percent profit
    columnHelper.accessor('percent_profit', {
      cell: (props) => {
        return (
          <Box color={props.getValue() < 0 ? 'red' : 'black'}>
            {(props.getValue() * 100).toFixed(2)}%
          </Box>
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
  const hiddenColumns = ['item_id'];
  
  return (
    <DataTable 
      columns={columns} 
      data={props.data} 
      hiddenColumns={hiddenColumns}
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
  
  useEffect(() => {
  
    // query recipe data

    // async data fetch
    const fetchData = async() => {
      
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
      
      // construct Reagents param
      const reagents = item.reagents.map((reagent) => {
        return Reagent.create({
          name: reagent.name,
          item_id: reagent.item_id,
          media_url: reagent.media_url,
          quantity: reagent.quantity,
          price: reagentPrices['by_item_id'][reagent.item_id]
        })
      })
      
      const cost = reagents.reduce(
        (total, item) => total + item.quantity * item.price, 
        0
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
        unit_profit: item.vendor_price - cost,
        percent_profit: item.vendor_price / cost - 1
      })
      
      return freeLunch
    }) : {}
    
    console.log('data: ', data)
    
    // update state
    setFreeLunchData(data);
  }, [craftedItemRecipes, reagentPrices])

  return (
    <>
      <Box display='block' bg='cyan.300' p='10px 14px'>
        Free Lunches
      </Box>
      <FreeLunchesFilters />
      <Box display='block'>
        <FreeLunchTable data={freeLunchData} />
      </Box>
    </>
  )
  
}


// Free Lunches component
export const FreeLunches = () => {
  
  return (
    <FreeLunchesContent />
  )
}