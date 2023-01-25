import { useCallback, useContext, useEffect, useMemo, useState } from 'react';
import {
  Box,
  Button, 
  ButtonGroup,
  Icon,
  Input,
  InputGroup,
  InputLeftElement,
  Progress, 
} from '@chakra-ui/react';

import Cookies from 'js-cookie'

import { FaSearch } from 'react-icons/fa'

import { CalendarPopover } from './CalendarPopover';
import { FreeLunch, FreeLunchTable, Reagent } from './FreeLunchTable';

import { useWindowDimensions } from '../hooks/WindowDimensions';

import { CraftedItemRecipesContext } from '../state/CraftedItemRecipesContext';
import { FreeLunchesContext } from '../state/FreeLunchesContext';
import { ProfessionContext } from '../state/ProfessionContext';
import { ReagentPricesContext } from '../state/ReagentPricesContext';
import { getFormattedDate } from '../utils';


// =========
// Constants
// =========

const FREE_LUNCHES_FILTER_BREAKPOINT = 525   // Vertical or horizontal filters


// ==============
// Main Component
// ==============


// Profession Free Lunches
export const ProfessionFreeLunches = () => {
  
  const { craftedItemRecipes, setCraftedItemRecipes} = useContext(CraftedItemRecipesContext);
  const { freeLunches, setFreeLunches} = useContext(FreeLunchesContext);
  const { profession } = useContext(ProfessionContext);
  const { reagentPrices } = useContext(ReagentPricesContext);
  
  const [ columnFilters, setColumnFilters ] = useState([]);
  const [ searchValue, setSearchValue ] = useState('');
  const [ isLoadingRecipes, setIsLoadingRecipes ] = useState(false);
  const [ isLoadingFreeLunches, setIsLoadingFreeLunches ] = useState(false);
  
  const { width } = useWindowDimensions();
  
  useEffect(() => {
  
    // query recipe data

    // async data fetch
    const fetchData = async() => {
      
      // update state
      setIsLoadingRecipes(true);

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
      const data = await res.json()

      // update state
      setIsLoadingRecipes(false);
      setCraftedItemRecipes({recipes: data['data']});
    };
    
    // invoke function
    fetchData()
      .catch(console.error);

  }, [profession, setCraftedItemRecipes]);
  
  
  useEffect(() => {
    
    // calculate Free Lunch data

    // update state
    setIsLoadingFreeLunches(true);

    const freeLunchData = (craftedItemRecipes.recipes.length > 0
        && Object.keys(reagentPrices.by_item_id).length > 0) 
      ? craftedItemRecipes.recipes.map((item) => {
      
      // identify cases where there is not enough price data
      let insufficientData = false;
      
      // construct Reagents param
      const reagents = item.reagents.map((reagent) => {
        
        if (reagentPrices.by_item_id[reagent.item_id] === 0) {
          insufficientData = true;
        }
        
        return Reagent.create({
          name: reagent.name,
          item_id: reagent.item_id,
          media_url: null,
          quantity: reagent.quantity,
          price: reagentPrices.by_item_id[reagent.item_id]
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
        reagents: null,
        vendor_price: item.vendor_price,
        cost: cost,
        unit_profit: insufficientData ? 0 : item.vendor_price - cost,
        percent_profit: insufficientData ? 0 : item.vendor_price / cost - 1,
        insufficient_data: insufficientData
      })
      
      return freeLunch
    }) : []

    // update state
    setIsLoadingFreeLunches(false);
    setFreeLunches({
      free_lunches: freeLunchData,
      update_time: reagentPrices.update_time,
    });      

  }, [craftedItemRecipes, reagentPrices, setFreeLunches])


  // function to update the FreeLunch table filters
  // filterColumn === null -> remove all filters
  // filterValue === null -> remove that filterColumn
  // NOTE: wrapped in useCallback to prevent infinite re-render with useEffect
  const updateColumnFilters = useCallback( (filterColumn = null, filterValue = null) => {
    
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
    setColumnFilters(newColumnFilters);
  }, [])


  useEffect(() => {
    
    // debounce search value

    const updateSearchValue = setTimeout(() => {
      updateColumnFilters('name', searchValue)
    }, 500)
    
    return () => clearTimeout(updateSearchValue)
  }, [searchValue, updateColumnFilters])


  // function to show all Free Lunches (eg. remove all filters)
  function showAllFreeLunches() {
    setSearchValue('');
    updateColumnFilters();
  }
  
  // prevent re-render of table when user is entering search input
  const freeLunchTable = useMemo(() => (
    <FreeLunchTable 
      data={freeLunches.free_lunches} 
      columnFilters={columnFilters}
      enableShowAllMessage={true}
    />    
  ), [freeLunches.free_lunches, columnFilters])
  

  return (
    <>
      <Box display='flex' alignItems='center' justifyContent='space-between' bg='teal.500' color='white' fontWeight='medium' p='8px 14px'>
        <Box>
          Free Lunches
        </Box>
        <CalendarPopover 
          color='gray.600' 
          label={'As of ' + getFormattedDate(new Date(freeLunches['update_time']))}
          isDisabled={reagentPrices['is_loading'] || isLoadingFreeLunches}
        />
      </Box>
      <Box display='flex' alignItems='center' justifyContent={width < FREE_LUNCHES_FILTER_BREAKPOINT ? 'center' : 'space-between'} flexWrap='wrap' p='14px'>
        <ButtonGroup colorScheme='pink' spacing='8px'>
          <Button onClick={() => {showAllFreeLunches()}}>
            Show All
          </Button>
          <Button 
            onClick={() => {updateColumnFilters('unit_profit', [1, 999999])}}
          >
            Show Profitable
          </Button>
        </ButtonGroup>
        <InputGroup 
          display='flex' 
          width={width < FREE_LUNCHES_FILTER_BREAKPOINT ? '250px'  : '215px'} 
          alignItems='center'
          m={width < FREE_LUNCHES_FILTER_BREAKPOINT ? '10px 0px 0px' : '0px'}
        >
          <InputLeftElement 
            pointerEvents='none'
            children={<Icon as={FaSearch} color='gray.500' boxSize='18px'/>}
          />
          <Input 
            value={searchValue}
            type='search' 
            placeholder='Item name'
            onChange={(e) => setSearchValue(e.target.value)}
          />
        </InputGroup>
      </Box>
      {(reagentPrices['is_loading'] || isLoadingRecipes || isLoadingFreeLunches) && 
        <Box display='block' alignItems='center' flexWrap='wrap'>
          <Progress isIndeterminate />
        </Box>
      }
      {!(reagentPrices['is_loading'] || isLoadingRecipes || isLoadingFreeLunches) &&
        <Box display='block'>
          {freeLunchTable}
        </Box>
      }
    </>
  )
}