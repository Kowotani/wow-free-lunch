import { useContext, useEffect, useMemo, useState, } from 'react';
import {
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  Box,
  Icon,
  Progress, 
} from '@chakra-ui/react';

import { FiPlusCircle, FiMinusCircle } from 'react-icons/fi'

import { CalendarPopover } from './CalendarPopover';
import { FreeLunch, FreeLunchTable } from './FreeLunchTable';

import { AllFreeLunchesContext } from '../state/AllFreeLunchesContext';
import { FactionContext } from '../state/FactionContext';
import { RealmContext } from '../state/RealmContext';
import { DEV_BASE_URL, getFormattedDate } from '../utils';


// ====================
// Profession Accordion
// ====================


// component for Item Subclass accordion
const ProfessionAccordion = (props) => {
  
  const { allFreeLunches } = useContext(AllFreeLunchesContext);
  
  const data = allFreeLunches['free_lunches'][props.profession];

  return (
    <Accordion 
      allowToggle={true} 
      defaultIndex={data.length > 0 ? 0 : null} 
      p='10px'
    >
      <AccordionItem border='0px'>
        {({ isExpanded }) => (
          <>
            <AccordionButton bg='gray.200' color='gray.500' _hover={{bg: 'gray.300'}} _expanded={{bg: 'green.400', color: 'white'}} borderRadius='12px'>
              <Box flex='1' textAlign='left'>
                {props.profession}
              </Box>
              {isExpanded ? (
                <Icon as={FiMinusCircle} boxSize='22px' />
              ) : (
                <Icon as={FiPlusCircle} boxSize='22px' />
              )}
            </AccordionButton>
            <AccordionPanel p={0}>
              <FreeLunchTable
                data={data}
                enableShowAllMessage={false}
              />
            </AccordionPanel>
          </>
        )}
      </AccordionItem>
    </Accordion>
  )
}


// ==============
// Main Component
// ==============


// All Free Lunches
export const AllFreeLunches = () => {
  
  const { allFreeLunches, setAllFreeLunches} = useContext(AllFreeLunchesContext);
  const { faction } = useContext(FactionContext);
  const { realm } = useContext(RealmContext);
  
  const [isLoading, setIsLoading] = useState(false);
  
  useEffect(() => {
  
    // query Free Lunches

    // async data fetch
    const fetchData = async() => {
      
      // update state
      setIsLoading(true);
      
      // prepare config
      const base_url = (window.location.origin === DEV_BASE_URL 
        ? DEV_BASE_URL
        : window.location.origin
      )
      const params = new URLSearchParams({
        realm: realm.name,
        faction: faction.name,
        date: 'latest',
      }).toString();
      const url = base_url + '/api/all_free_lunches?' + params;
      
      // get response
      const res = await fetch(url)
      
      // convert to json
      const resJson = await res.json();
      const data = resJson['data']
      
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
      setIsLoading(false);
      setAllFreeLunches({
        free_lunches: free_lunches,
        update_time: resJson['update_time'],
      });      
    };
    
    // invoke function
    fetchData()
      .catch(console.error);

  }, [realm.name, faction, setAllFreeLunches]);


  // prevent re-render of table when user is entering search input
  const freeLunchAccordions = useMemo(() => (
    <>
      {Object.keys(allFreeLunches.free_lunches).map((profession) => {
        return <ProfessionAccordion key={profession} profession={profession} />
      })}  
    </>
  ), [allFreeLunches.free_lunches])

  
  return (
    <>
      <Box display='flex' alignItems='center' justifyContent='space-between' bg='teal.500' color='white' fontWeight='medium' p='8px 14px' m='10px 0px 6px 0px'>
        <Box>
          Free Lunches
        </Box>
        <CalendarPopover 
          color='gray.600' 
          label={'As of ' + getFormattedDate(new Date(allFreeLunches.update_time))}
          isDisabled={isLoading}
        />
      </Box>
      {isLoading && 
        <Box display='block' alignItems='center'>
          <Progress isIndeterminate />
        </Box>
      }
      {!isLoading &&
        <Box display='block'>
          {freeLunchAccordions}
        </Box>
      }
    </>
  )
}