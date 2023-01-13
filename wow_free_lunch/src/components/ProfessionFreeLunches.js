import { useContext, useEffect, useMemo, useState } from 'react';
import {
  Box,
  Button, 
  ButtonGroup,
  Icon,
  Input,
  InputGroup,
  InputLeftElement,
  Progress, 
  Spacer,
} from '@chakra-ui/react';

import Cookies from 'js-cookie'

import { FaSearch } from 'react-icons/fa'

import { FreeLunch, FreeLunchTable, Reagent } from './FreeLunchTable';

import { CraftedItemRecipesContext } from '../state/CraftedItemRecipesContext';
import { FreeLunchesContext } from '../state/FreeLunchesContext';
import { ProfessionContext } from '../state/ProfessionContext';
import { ReagentPricesContext } from '../state/ReagentPricesContext';


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
  
  
  useEffect(() => {
  
    // query recipe data

    // async data fetch
    const fetchData = async() => {
      
      const loadingCraftedItemRecipesState = {
        is_loading: true,
        recipes: craftedItemRecipes['recipes']
      };
      setCraftedItemRecipes(loadingCraftedItemRecipesState);

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

    // update state
    const loadedFreeLunchesState = {
      is_loading: false,
      free_lunches: freeLunchData
    };
    setFreeLunches(loadedFreeLunchesState);      

  }, [craftedItemRecipes['recipes'], reagentPrices])


  useEffect(() => {
    
    // debounce search value

    const updateSearchValue = setTimeout(() => {
      updateColumnFilters('name', searchValue)
    }, 500)
    
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
    setColumnFilters(newColumnFilters);
  }


  // function to show all Free Lunches (eg. remove all filters)
  function showAllFreeLunches() {
    setSearchValue('');
    updateColumnFilters();
  }
  
  // prevent re-render of table when user is entering search input
  const freeLunchTable = useMemo(() => (
    <FreeLunchTable 
      data={freeLunches['free_lunches']} 
      columnFilters={columnFilters}
      enableShowAllMessage={true}
    />    
  ), [freeLunches['free_lunches'], columnFilters])
  
  
  return (
    <>
      <Box display='block' bg='teal.500' color='white' fontWeight='medium' p='10px 14px'>
        Free Lunches
      </Box>
      <Box display='flex' alignItems='center' flexWrap='wrap'>
        <ButtonGroup colorScheme='pink' p='14px' spacing='8px'>
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
        <InputGroup display='flex' width='250px' p='14px 14px' alignItems='center'>
          <InputLeftElement display='flex' alignItems='flex-end' justifyContent='flex-end'
            pointerEvents='none'
            children={<Icon as={FaSearch} color='gray.500'/>}
          />
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