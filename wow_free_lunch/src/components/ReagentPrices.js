import { useContext, useEffect } from 'react';
import {
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  Box,
  Image,
  Icon,
  Link,
  Tooltip,
} from '@chakra-ui/react';

import { FiPlusCircle, FiMinusCircle } from 'react-icons/fi'
import { firstBy } from 'thenby'


import { FactionContext } from '../state/FactionContext';
import { ProfessionContext } from '../state/ProfessionContext';
import { ReagentPricesContext } from '../state/ReagentPricesContext';
import { RealmContext } from '../state/RealmContext';

import { PriceBox } from './PriceBox'

import { 
  DEV_BASE_URL, 
  getItemQualityColor, 
  getRandomInt, 
  getWowHeadUrl 
} from '../utils';


// =========
// Constants
// =========

const LOAD_TIME_LOWER = 1250    // lower bound on randomized load time
const LOAD_TIME_UPPER = 1750   // upper bound on randomized load time


// ====================
// Item Class Hierarchy
// ====================

// component for Item Class accordion
const ItemClassAccordion = (props) => {
  
  const { reagentPrices } = useContext(ReagentPricesContext);
  
  return (
    <Accordion allowMultiple>
      <AccordionItem border='0px'>
      {({ isExpanded }) => (
        <>
          <AccordionButton 
            bg='yellow.400' 
            color='white'
            _hover={{bg: 'yellow.300'}} 
            _expanded={{ bg: 'yellow.200', color: 'gray.500' }} 
            borderRadius='12px'
          >
            <Box flex='1' textAlign='left'>
              {props.itemClass}
            </Box>
              {isExpanded
                ? <Icon as={FiMinusCircle} boxSize='22px'/>
                : <Icon as={FiPlusCircle} boxSize='22px'/>
              }
          </AccordionButton>
          <AccordionPanel paddingBottom='8px'>
            <Box justifyContent='center'>
                {
                  Object.keys(reagentPrices['by_item_class'][props.itemClass])
                  .sort()
                  .map( 
                    itemSubclass => {
                      return (
                        <Box key={itemSubclass} display='block' padding='8px'>
                          <ItemSubclassAccordion 
                            itemClass={props.itemClass} 
                            itemSubclass={itemSubclass} 
                          />
                        </Box>
                      )
                    }
                  )
                }
            </Box>
          </AccordionPanel>
        </>
      )}
      </AccordionItem>
    </Accordion>
  )
}


// component for Item Subclass accordion
const ItemSubclassAccordion = (props) => {
  
  const { reagentPrices } = useContext(ReagentPricesContext);

  return (
    <Accordion allowMultiple>
      <AccordionItem border='0px'>
        {({ isExpanded }) => (
          <>
            <AccordionButton 
              bg='purple.400' 
              color='white' 
              _hover={{bg: 'purple.300'}}
              _expanded={{ bg: 'purple.200', color: 'gray.500' }} 
              borderRadius='12px'
            >
              <Box flex='1' textAlign='left'>
                {props.itemSubclass}
              </Box>
                {isExpanded 
                  ? <Icon as={FiMinusCircle} boxSize='22px'/>
                  : <Icon as={FiPlusCircle} boxSize='22px'/>
                }
            </AccordionButton>
            <AccordionPanel paddingBottom='8px'>
              <Box 
                display='flex' 
                gap='8px' 
                justifyContent='center' 
                flexWrap='wrap'
              >
                  {
                    reagentPrices['by_item_class'][props.itemClass][props.itemSubclass]
                    .sort(
                      firstBy(function (a, b) { return a.level - b.level})
                      .thenBy(function (a, b) { return a.item_id - b.item_id})
                    )
                    .map(
                      reagent => {
                        return (
                          <Box 
                            key={reagent.item_id} 
                            display='block' 
                            padding='8px'
                          >
                            <ReagentPriceBox
                              itemId={reagent.item_id}
                              name={reagent.name} 
                              price={reagent.min_price}
                              quality={reagent.quality}
                              mediaUrl={reagent.media_url}
                            />
                          </Box>
                        )
                      }
                    )
                  }
              </Box>
            </AccordionPanel>
          </>
        )}
      </AccordionItem>
    </Accordion>
  )
}


// =================
// Reagent Price Box
// =================

// component for Reagent with price
const ReagentPriceBox = (props) => {

  return (
    <Box 
      display='flex' 
      height='65px' 
      width='250px' 
      bg={props.price === 0 ? 'gray.100' : 'green.100'} 
      borderRadius='12px'
    >
      <Box 
        display='flex' 
        width='65px' 
        alignItems='center' 
        justifyContent='center'
      >
         <Link href={getWowHeadUrl(props.itemId)} isExternal>
          <Image 
            src={props.mediaUrl} 
            height='48px' 
            width='48px' 
            border='2px solid white' 
            borderRadius='10px' 
            outline='2px solid black'
          />
        </Link>
      </Box>
      <Box width='185px'>
        <Box 
          display='flex' 
          alignItems='flex-end' 
          fontWeight='semibold' 
          padding='4px 4px 0px 4px' 
          noOfLines={1} 
          color={getItemQualityColor(props.quality)}
        >
          <Tooltip label={props.name} placement='top'>
            <Link href={getWowHeadUrl(props.itemId)} isExternal>
              {props.name}
            </Link>
          </Tooltip>
        </Box>
        <Box display='flex' justifyContent='flex-end'>
          <Box p='4px 4px 4px 0px'>
            {props.price === 0 
              ? <Box p='0px 8px'>No data</Box>
              : <PriceBox price={props.price}/>  
            }
          </Box>
        </Box>
      </Box>
    </Box>
  )
  
}


// ==============
// Main Component
// ==============

// Reagent Prices
export const ReagentPrices = () => {

  const { faction } = useContext(FactionContext);
  const { profession } = useContext(ProfessionContext);
  const { reagentPrices, setReagentPrices } = useContext(ReagentPricesContext);
  const { realm } = useContext(RealmContext);
  
  useEffect(() => {
    
    // async data fetch
    const fetchData = async() => {
      
      const loadingReagentPricesState = {
        is_loading: true,
        by_item_class: {},
        by_item_id: {},
        update_time: null,
      };
      setReagentPrices(loadingReagentPricesState);
      const startTime = new Date();

      // prepare config
      const base_url = (window.location.origin === DEV_BASE_URL 
        ? DEV_BASE_URL
        : window.location.origin
      )
      const params = new URLSearchParams({
        profession: profession.name,
        realm: realm.name,
        faction: faction.name,
        date: 'latest',
      }).toString();
      const url = base_url + '/api/reagent_prices?' + params;
      
      // get response
      const res = await fetch(url)
      
      // convert to json
      const resJson = await res.json();
      const data = resJson['data']
      
      // create item_id indexed price dict
      const dataItemId = {};
      for (const itemClass of Object.keys(data)) {
        for (const itemSubclass of Object.keys(data[itemClass])) {
          for (const reagent of data[itemClass][itemSubclass]) {
            dataItemId[reagent.item_id] = reagent.min_price
          }
        }
      }
      
      // update state after min time has elapsed
      const minLoadingTime = getRandomInt(LOAD_TIME_LOWER, LOAD_TIME_UPPER);
      const endTime = new Date();
      const delay = Math.max(minLoadingTime - (endTime - startTime), 0);
      const loadedReagentPricesState = {
        is_loading: false,
        by_item_class: data,
        by_item_id: dataItemId,
        update_time: resJson['update_time'],
      }
      setTimeout(() => {
        setReagentPrices(loadedReagentPricesState);
      }, delay);
    };
    
    // invoke function
    fetchData()
      .catch(console.error);
      
  }, [faction, profession, realm.name, setReagentPrices]);

  return (
    <>
      <Box display='block' p='10px 0px 10px 0px'>
        <Accordion allowMultiple>
          <AccordionItem border='0px'>
          {({ isExpanded }) => (
            <>
              <AccordionButton 
                bg='blue.500' 
                color='white'
                _hover={{bg: 'blue.400'}}
                _expanded={{ bg: 'blue.300', color: 'gray.100' }} 
                height='48px'
              >
                <Box flex='1' textAlign='left' fontWeight='medium'>
                  Reagent Prices
                </Box>
                {isExpanded ? (
                  <Icon as={FiMinusCircle} boxSize='22px' m='0px 2px'/>
                ) : (
                  <Icon as={FiPlusCircle} boxSize='22px' m='0px 2px'/>
                )}
              </AccordionButton>
              <AccordionPanel paddingBottom='8px'>
                  {
                    Object.keys(reagentPrices.by_item_class)
                    .sort()
                    .map( 
                      itemClass => {
                        return (
                          <Box key={itemClass} display='block' padding='8px'>
                            <ItemClassAccordion itemClass={itemClass} />
                          </Box>
                        )
                      }
                    )
                  }
              </AccordionPanel>   
              </>
            )}
          </AccordionItem>
        </Accordion>
      </Box>
    </>
  )
  
}