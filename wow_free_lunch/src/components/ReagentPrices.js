import { useContext, useEffect } from 'react';
import {
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
  Button,
  ButtonGroup,
  Box,
  // HStack,
  Image,
  Input,
  InputGroup,
  // InputLeftElement,
  // Radio,
  // RadioGroup,
  Spacer,
} from '@chakra-ui/react';
// import { SearchIcon } from '@chakra-ui/icons'

import Cookies from 'js-cookie'
import { firstBy } from 'thenby'

import { FactionContext } from '../state/FactionContext';
// import { PriceType, PriceTypeContext, PriceTypeProvider } from '../state/PriceTypeContext';
import { ProfessionContext } from '../state/ProfessionContext';
import { ReagentPricesContext, ReagentPricesProvider } from '../state/ReagentPricesContext';
import { RealmContext } from '../state/RealmContext';

import { PriceBox } from './PriceBox'


// =======
// Filters 
// =======

// component for Reagent Price Box filters
const ReagentFilters = () => {
  
  // const { priceType, setPriceType } = useContext(PriceTypeContext);
  
  return (
    <Box display='flex' alignItems='center'>
      <ButtonGroup colorScheme='pink' spacing='2'>
        <Button>Expand All</Button>
        <Button>Collapse All</Button>
      </ButtonGroup>
      <Spacer />
      <InputGroup width='200px' p='8px'>
        <Input type='search' placeholder='Reagent name' />
      </InputGroup>
    </Box>
  )
}


function CollapseAccordionItems(accordion) {
  
}

// ====================
// Item Class Hierarchy
// ====================

// component for Item Class accordion
const ItemClassAccordion = (props) => {
  
  const { reagentPrices } = useContext(ReagentPricesContext);
  
  return (
    <Accordion allowMultiple>
      <AccordionItem>
        <AccordionButton bg='orange.200' _expanded={{ bg: 'orange.100', color: 'gray.400' }}>
          <Box flex='1' textAlign='left'>
            {props.itemClass}
          </Box>
          <AccordionIcon />
        </AccordionButton>
        <AccordionPanel>
          <Box justifyContent='center'>
              {
                Object.keys(reagentPrices[props.itemClass])
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
      </AccordionItem>
    </Accordion>
  )
}


// component for Item Subclass accordion
const ItemSubclassAccordion = (props) => {
  
  const { reagentPrices } = useContext(ReagentPricesContext);
  // const { priceType } = useContext(PriceTypeContext);

  return (
    <Accordion allowMultiple>
      <AccordionItem>
        <AccordionButton bg='blue.200' _expanded={{ bg: 'blue.100', color: 'gray.400' }}>
          <Box flex='1' textAlign='left'>
            {props.itemSubclass}
          </Box>
          <AccordionIcon />
        </AccordionButton>
        <AccordionPanel>
          <Box display='flex' gap='8px' justifyContent='flex-start' flexWrap='wrap'>
              {
                Object.entries(reagentPrices[props.itemClass][props.itemSubclass])
                .sort(
                  firstBy(function (a, b) { return a[1].level - b[1].level})
                  .thenBy(function (a, b) { return a[1].item_id - b[1].item_id})
                )
                .map(
                  reagent => {
                    return (
                      <Box key={reagent[1].item_id} display='block' padding='8px'>
                        <ReagentPriceBox 
                          name={reagent[0]} 
                          price={reagent[1].min_price}
                          quality={reagent[1].quality}
                          mediaUrl={reagent[1].media_url}
                          isDisabled={reagent[1].quantity === 0}
                        />
                      </Box>
                    )
                  }
                )
              }
          </Box>
        </AccordionPanel>
      </AccordionItem>
    </Accordion>
  )
}


// ===========
// Reagent Box
// ===========

// component for Reagent with price
const ReagentPriceBox = (props) => {
  
  return (
    <Box display='flex' height='60px' width='225px' bg='green.200'>
      <Box display='flex' width='60px' alignItems='center' justifyContent='center'>
        <Image src={props.mediaUrl} height='48px' width='48px' border='4px solid white'/>
      </Box>
      <Box width='165px'>
        <Box display='block' width='100%' alignItems='flex-end' fontWeight='semibold' padding='4px 4px 0px 4px'>
          {props.name}
        </Box>
        <Box display='flex' justifyContent='flex-end'>
          <Box p='4px 4px 4px 0px'>
            <PriceBox price={props.price}/>
          </Box>
        </Box>
      </Box>
    </Box>
  )
  
}


// ==============
// Main Component
// ==============

// Reagent Prices content
const ReagentPricesContent = () => {
  
  const { faction } = useContext(FactionContext);
  const { profession } = useContext(ProfessionContext);
  const { reagentPrices, setReagentPrices } = useContext(ReagentPricesContext);
  const { realm } = useContext(RealmContext);
  
  useEffect(() => {
    
    // async data fetch
    const fetchData = async() => {
      
      console.log('fetching data...', profession, realm, faction);
      
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
      const data = await res.json();
      console.log(data);
      
      // update state
      setReagentPrices(data);
    };
    
    // invoke function
    fetchData()
      .catch(console.error);
      
  }, [profession, realm, faction, setReagentPrices]);

  return (
    <>
      <Box display='block' p='10px 0px 10px 0px'>
        <Accordion allowMultiple>
          <AccordionItem>
            <AccordionButton bg='purple.200' _expanded={{ bg: 'purple.100', color: 'gray.400' }}>
              <Box flex='1' textAlign='left'>
                Reagent Prices
              </Box>
              <AccordionIcon />
            </AccordionButton>
            <AccordionPanel>
              <ReagentFilters />
                {
                  Object.keys(reagentPrices)
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
          </AccordionItem>
        </Accordion>
      </Box>
    </>
  )
  
}


// Reagent Prices component
export const ReagentPrices = () => {
  
  return (
    <ReagentPricesProvider>
      <ReagentPricesContent />
    </ReagentPricesProvider>
  )
};