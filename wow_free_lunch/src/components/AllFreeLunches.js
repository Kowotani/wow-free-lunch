import { useContext, useEffect, useMemo, useState } from 'react';
import {
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,  
  Box,
  Progress, 
} from '@chakra-ui/react';

import Cookies from 'js-cookie'

import { FreeLunch, FreeLunchTable } from './FreeLunchTable';

import { AllFreeLunchesContext } from '../state/AllFreeLunchesContext';
import { FactionContext } from '../state/FactionContext';
import { RealmContext } from '../state/RealmContext';


// ====================
// Profession Accordion
// ====================


// component for Item Subclass accordion
const ProfessionAccordion = (props) => {
  
  const { allFreeLunches } = useContext(AllFreeLunchesContext);

  return (
    <Accordion allowMultiple p='10px'>
      <AccordionItem>
        <AccordionButton bg='green.200' _expanded={{ bg: 'green.100', color: 'gray.400' }}>
          <AccordionIcon />
          <Box flex='1' textAlign='left'>
            {props.profession}
          </Box>
        </AccordionButton>
        <AccordionPanel>
          <FreeLunchTable
            data={allFreeLunches['free_lunches'][props.profession]}
          />
        </AccordionPanel>
      </AccordionItem>
    </Accordion>
  )
}


// ==============
// Main Component
// ==============


// All Free Lunches
export const AllFreeLunches = () => {
  
  // const { craftedItemRecipes, setCraftedItemRecipes} = useContext(CraftedItemRecipesContext);
  const { allFreeLunches, setAllFreeLunches} = useContext(AllFreeLunchesContext);
  const { faction } = useContext(FactionContext);
  const { realm } = useContext(RealmContext);
  
  // const { profession } = useContext(ProfessionContext);
  // const { reagentPrices } = useContext(ReagentPricesContext);
  
  // const [ columnFilters, setColumnFilters ] = useState([]);
  // const [ searchValue, setSearchValue ] = useState('');
  
  
  useEffect(() => {
  
    // query Free Lunches

    // async data fetch
    const fetchData = async() => {
      
      const loadingState = {
        is_loading: true,
        free_lunches: allFreeLunches['free_lunches']
      };
      setAllFreeLunches(loadingState);
      
      console.log('fetching /api/all_free_lunches ...', realm, faction);
      
      // prepare config
      const url = '/api/all_free_lunches';

      const config = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': Cookies.get('csrftoken'),
        },
        body: JSON.stringify({
          realm: realm.name,
          faction: faction.name, 
          date: 'latest'          
        })
      };
      
      // get response
      const res = await fetch(url, config)
      
      // convert to json
      const data = await res.json();
      console.log('retrieved /api/all_free_lunches: ', data);
      
      // format data
      const free_lunches = {}
      for (const profession of Object.keys(data)) {
        free_lunches[profession] = data[profession].map((item) => {
          
          const freeLunch = FreeLunch.create({
            name: item.name,
            item_id: item.item_id,
            quality: item.quality,
            media_url: item.media_url,
            reagents: [],
            vendor_price: item.vendor_price,
            cost: item.cost,
            unit_profit: item.vendor_price - item.cost,
            percent_profit: item.vendor_price / item.cost - 1,
            insufficient_data: false
          }) 
          
          return freeLunch
        })
      }

      // update state
      const loadedState = {
        is_loading: false,
        free_lunches: free_lunches
      };
      setAllFreeLunches(loadedState);      
    };
    
    // invoke function
    fetchData()
      .catch(console.error);

  }, [realm, faction]);
  


  // useEffect(() => {
    
  //   // debounce search value

  //   const updateSearchValue = setTimeout(() => {
  //     updateColumnFilters('name', searchValue)
  //   }, 500)
    
  //   return () => clearTimeout(updateSearchValue)
  // }, [searchValue])


  // manage updating the FreeLunch table filters
  // filterColumn === null -> remove all filters
  // filterValue === null -> remove that filterColumn
  // function updateColumnFilters(filterColumn = null, filterValue = null) {
    
  //   const newColumnFilters = [];
    
  //   // modify a single column filter, otherwise reset all filters
  //   if (filterColumn !== null) {
    
  //     // update 
  //     for (const obj of columnFilters) {
  //       if (obj.id !== filterColumn) {
  //         newColumnFilters.push(obj)
  //       }
  //     }
  //     if (filterValue !== null) {
  //       newColumnFilters.push({
  //         id: filterColumn, 
  //         value: filterValue
  //       });
  //     }
  //   }
    
  //   // update state
  //   console.log('new filters: ', newColumnFilters)
  //   setColumnFilters(newColumnFilters);
  // }


  // // function to show all Free Lunches (eg. remove all filters)
  // function showAllFreeLunches() {
  //   setSearchValue('');
  //   updateColumnFilters();
  // }
  
  // // prevent re-render of table when user is entering search input
  // const freeLunchTable = useMemo(() => (
  //   <FreeLunchTable 
  //     data={freeLunches['free_lunches']} 
  //     columnFilters={columnFilters}
  //   />    
  // ), [freeLunches['free_lunches'], columnFilters])

  // prevent re-render of table when user is entering search input
  const freeLunchAccordions = useMemo(() => (
    <>
      {Object.keys(allFreeLunches['free_lunches']).map((profession) => {
        return <ProfessionAccordion profession={profession} />
      })}  
    </>
  ), [allFreeLunches['free_lunches']])

  
  return (
    <>
      <Box display='block' bg='cyan.300' p='10px 14px' m='10px 0px'>
        Free Lunches
      </Box>
      {allFreeLunches['is_loading'] && 
        <Box display='block' alignItems='center'>
          <Progress isIndeterminate />
        </Box>
      }
      {!allFreeLunches['is_loading'] &&
        <Box display='block'>
          {freeLunchAccordions}
        </Box>
      }
    </>
  )
}