import { useContext, useState } from 'react';
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

import { 
  createColumnHelper, 
  useReactTable,
  flexRender,
  getCoreRowModel,
  getSortedRowModel
} from "@tanstack/react-table";


import { Data } from 'dataclass';
import { DataTable } from './DataTable';
import { PriceBox } from './PriceBox';

import { ReagentPricesContext, ReagentPricesProvider } from '../state/ReagentPricesContext';
// import { Faction, FactionContext } from '../state/FactionContext';
// import { Nav, NavContext } from '../state/NavContext';
// import { Profession, ProfessionContext } from '../state/ProfessionContext';
// import { RealmContext } from '../state/RealmContext';


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
  
//   const { reagentPrices } = useContext(ReagentPricesContext);
//   const [ freeLunches, setFreeLunches] = useState({});

  // query recipe data
  
  // calculate Free Lunch data
  const data = [
    FreeLunch.create({
      name: 'Azure Silk Vest',
      item_id: 4324,
      quality: 'UNCOMMON',
      media_url: 'https://render.worldofwarcraft.com/classic-us/icons/56/inv_chest_cloth_37.jpg',
      reagents: [
        Reagent.create({
          name: 'Bolt of Silk Cloth',
          item_id: 4305,
          media_url: 'https://render.worldofwarcraft.com/classic-us/icons/56/inv_fabric_silk_03.jpg',
          quantity: 5,
          price: 350
        }),
        Reagent.create({
          name: 'Blue Dye',
          item_id: 6260,
          media_url: 'https://render.worldofwarcraft.com/classic-us/icons/56/inv_potion_15.jpg',
          quantity: 4,
          price: 50
        }),
      ],
      vendor_price: 1874,
      cost: 1950,
      unit_profit: -76,
      percent_profit: -0.0389
    }),
    FreeLunch.create({
      name: 'Gloves of the Dawn',
      item_id: 19057,
      quality: 'RARE',
      media_url: 'https://render.worldofwarcraft.com/classic-us/icons/56/inv_gauntlets_29.jpg',
      reagents: [
        Reagent.create({
          name: 'Arcanite Bar',
          item_id: 12360,
          media_url: 'https://render.worldofwarcraft.com/classic-us/icons/56/inv_misc_stonetablet_05.jpg',
          quantity: 2,
          price: 4250
        }),
        Reagent.create({
          name: 'Truesilver Bar',
          item_id: 6037,
          media_url: 'https://render.worldofwarcraft.com/classic-us/icons/56/inv_ingot_08.jpg',
          quantity: 10,
          price: 750
        }),
        Reagent.create({
          name: 'Righteous Orb',
          item_id: 12811,
          media_url: 'https://render.worldofwarcraft.com/classic-us/icons/56/inv_misc_gem_pearl_03.jpg',
          quantity: 1,
          price: 20000
        }),
      ],
      vendor_price: 17744,
      cost: 36000,
      unit_profit: -10256,
      percent_profit: -0.5071
    }),
    FreeLunch.create({
      name: 'Nightscape Tunic',
      item_id: 8175,
      quality: 'UNCOMMON',
      media_url: 'https://render.worldofwarcraft.com/classic-us/icons/56/inv_chest_leather_03.jpg',
      reagents: [
        Reagent.create({
          name: 'Thick Leather',
          item_id: 4304,
          media_url: 'https://render.worldofwarcraft.com/classic-us/icons/56/inv_misc_leatherscrap_08.jpg',
          quantity: 7,
          price: 575
        }),
        Reagent.create({
          name: 'Silken Thread',
          item_id: 4291,
          media_url: 'https://render.worldofwarcraft.com/classic-us/icons/56/inv_fabric_silk_02.jpg',
          quantity: 2,
          price: 500
        }),
      ],
      vendor_price: 5971,
      cost: 5025,
      unit_profit: 946,
      percent_profit: 0.1893
    })
  ];
  
  

  return (
    <>
      <Box display='block' bg='cyan.300' p='10px 14px'>
        Free Lunches
      </Box>
      <FreeLunchesFilters />
      <Box display='block'>
        <FreeLunchTable data={data} />
      </Box>
    </>
  )
  
}


// Free Lunches component
export const FreeLunches = () => {
  
  return (
    <ReagentPricesProvider>
      <FreeLunchesContent />
    </ReagentPricesProvider>
  )
}