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

import Cookies from 'js-cookie'
import { FiPlusCircle, FiMinusCircle } from 'react-icons/fi'
import { firstBy } from 'thenby'


import { FactionContext } from '../state/FactionContext';
import { ProfessionContext } from '../state/ProfessionContext';
import { ReagentPricesContext } from '../state/ReagentPricesContext';
import { RealmContext } from '../state/RealmContext';

import { PriceBox } from './PriceBox'

import { getWowHeadUrl, getItemQualityColor } from '../utils';


// =======
// Filters 
// =======

// component for Reagent Price Box filters
// const ReagentFilters = () => {
  
//   // const { priceType, setPriceType } = useContext(PriceTypeContext);
  
//   return (
//     <Box display='flex' alignItems='center' flexWrap='wrap'>
//       <ButtonGroup colorScheme='pink' spacing='2'>
//         <Button>Expand All</Button>
//         <Button>Collapse All</Button>
//       </ButtonGroup>
//       <Spacer />
//       <InputGroup width='200px' p='8px'>
//         <Input type='search' placeholder='Reagent name' />
//       </InputGroup>
//     </Box>
//   )
// }


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
          <AccordionButton bg='yellow.400' color='white' _expanded={{ bg: 'yellow.300', color: 'gray.400' }} borderRadius='12px'>
            <Box flex='1' textAlign='left'>
              {props.itemClass}
            </Box>
              {isExpanded ? (
                <Icon as={FiMinusCircle} boxSize='22px' />
              ) : (
                <Icon as={FiPlusCircle} boxSize='22px' />
              )}
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
            <AccordionButton bg='purple.300' color='white' _expanded={{ bg: 'purple.200', color: 'gray.100' }} borderRadius='12px'>
              <Box flex='1' textAlign='left'>
                {props.itemSubclass}
              </Box>
                {isExpanded ? (
                  <Icon as={FiMinusCircle} boxSize='22px'/>
                ) : (
                  <Icon as={FiPlusCircle} boxSize='22px'/>
                )}
            </AccordionButton>
            <AccordionPanel paddingBottom='8px'>
              <Box display='flex' gap='8px' justifyContent='center' flexWrap='wrap'>
                  {
                    reagentPrices['by_item_class'][props.itemClass][props.itemSubclass]
                    .sort(
                      firstBy(function (a, b) { return a.level - b.level})
                      .thenBy(function (a, b) { return a.item_id - b.item_id})
                    )
                    .map(
                      reagent => {
                        return (
                          <Box key={reagent.item_id} display='block' padding='8px'>
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
    <Box display='flex' height='65px' width='250px' bg={props.price === 0 ? 'gray.100' : 'green.100'} borderRadius='12px'>
      <Box display='flex' width='65px' alignItems='center' justifyContent='center'>
         <Link href={getWowHeadUrl(props.itemId)} isExternal>
          <Image src={props.mediaUrl} height='48px' width='48px' border='2px solid white' borderRadius='10px' outline='2px solid black'/>
        </Link>
      </Box>
      <Box width='185px'>
        <Box display='flex' alignItems='flex-end' fontWeight='semibold' padding='4px 4px 0px 4px' noOfLines={1} color={getItemQualityColor(props.quality)}>
          <Tooltip label={props.name} placement='top'>
            <Link href={getWowHeadUrl(props.itemId)} isExternal>
              {props.name}
            </Link>
          </Tooltip>
        </Box>
        <Box display='flex' justifyContent='flex-end'>
          <Box p='4px 4px 4px 0px'>
            {props.price === 0 
              ? (
                <Box p='0px 8px'>No data</Box>
              ) : (
                <PriceBox price={props.price}/>
              )
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
        by_item_class: reagentPrices['by_item_class'],
        by_item_id: reagentPrices['by_item_id'],
        update_time: reagentPrices['update_time'],
      };
      setReagentPrices(loadingReagentPricesState);

      // prepare config
      const url = '/api/reagent_prices';

      const config = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': Cookies.get('csrftoken'),
        },
        body: JSON.stringify({
          profession: profession.name,
          realm: realm.name,
          faction: faction.name, 
          date: 'latest'
        })
      };
      
      // get response
      const res = await fetch(url, config)
      
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
      
      // update state
      const loadedReagentPricesState = {
        is_loading: false,
        by_item_class: data,
        by_item_id: dataItemId,
        update_time: resJson['update_time'],
      }
      setReagentPrices(loadedReagentPricesState);
    };
    
    // invoke function
    fetchData()
      .catch(console.error);
      
  }, [profession, realm, faction, setReagentPrices]);

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
                    Object.keys(reagentPrices['by_item_class'])
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