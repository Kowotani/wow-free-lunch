import { useContext, useEffect, useState} from 'react';
import {
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
  Box,
  Button,
  HStack,
  Image,
  Input,
  InputGroup,
  // InputLeftElement,
  Radio,
  RadioGroup,
  Spacer,
} from '@chakra-ui/react';
// import { SearchIcon } from '@chakra-ui/icons'

import Cookies from 'js-cookie'

import { FactionContext } from '../state/FactionContext';
import { PriceType, PriceTypeContext, PriceTypeProvider } from '../state/PriceTypeContext';
import { Profession, ProfessionContext } from '../state/ProfessionContext';
import { ReagentPricesContext, ReagentPricesProvider } from '../state/ReagentPricesContext';
import { RealmContext } from '../state/RealmContext';

import { PriceBox } from './PriceBox'


function GenRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min))
}


// =======
// Filters 
// =======

// component for Reagent Price Box filters
const ReagentFilters = () => {
  
  const { priceType, setPriceType } = useContext(PriceTypeContext);
  
  return (
    <Box display='flex' alignItems='center'>
      <Box fontWeight='semibold' p='8px'>Price Type </Box>
      <RadioGroup onChange={setPriceType} value={priceType} defaultValue={PriceType.VWAP} p='8px'>
        <HStack>
          <Radio value={PriceType.VWAP}>VWAP</Radio>
          <Radio value={PriceType.MIN}>Min</Radio>
        </HStack>
      </RadioGroup>
      <Spacer />
      <InputGroup width='200px' p='8px'>
        <Input type='search' placeholder='Reagent name' />
      </InputGroup>
    </Box>
  )
}


// ====================
// Item Class Hierarchy
// ====================

// component for Item Class accordion
const ItemClassAccordion = (props) => {
  
  // const [itemSubclasses, setItemSubClasses] = useState();
  
  return (
    <Accordion allowMultiple>
      <AccordionItem>
        <AccordionButton bg='orange.200' _expanded={{ bg: 'orange.100', color: 'gray.400' }}>
          <Box flex='1' textAlign='left'>
            {props.name}
          </Box>
          <AccordionIcon />
        </AccordionButton>
        <AccordionPanel>
          <Box justifyContent='center'>
            <Box display='block' padding='10px'>
              <ItemSubclassAccordion name='Item Subclass 1'/>
            </Box>
            <Box display='block' padding='10px'>
              <ItemSubclassAccordion name='Item Subclass 2'/>
            </Box>
          </Box>
        </AccordionPanel>
      </AccordionItem>
    </Accordion>
  )
}


// component for Item Subclass accordion
const ItemSubclassAccordion = (props) => {
  
  // const [reagents, setReagents] = useState();
  
  return (
    <Accordion allowMultiple>
      <AccordionItem>
        <AccordionButton bg='blue.200' _expanded={{ bg: 'blue.100', color: 'gray.400' }}>
          <Box flex='1' textAlign='left'>
            {props.name}
          </Box>
          <AccordionIcon />
        </AccordionButton>
        <AccordionPanel>
          <Box display='flex' gap='10px' justifyContent='flex-start' flexWrap='wrap'>
            <ReagentPriceBox name='Reagent 1' price={123}/>
            <ReagentPriceBox name='Reagent 2' price={GenRandomInt(0, 100000)}/>
            <ReagentPriceBox name='Reagent 4' price={GenRandomInt(0, 100000)}/>
            <ReagentPriceBox name='Reagent 5' price={GenRandomInt(0, 100000)}/>
            <ReagentPriceBox name='Reagent 6' price={GenRandomInt(0, 100000)}/>
            <ReagentPriceBox name='Reagent 7' price={GenRandomInt(0, 100000)}/>
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
  
  const images = [
      'https://render.worldofwarcraft.com/classic-us/icons/56/inv_fabric_linen_01.jpg',
      'https://render.worldofwarcraft.com/classic-us/icons/56/inv_fabric_wool_01.jpg',
      'https://render.worldofwarcraft.com/classic-us/icons/56/inv_fabric_silk_01.jpg',
      'https://render.worldofwarcraft.com/classic-us/icons/56/inv_fabric_mageweave_01.jpg',
      'https://render.worldofwarcraft.com/classic-us/icons/56/inv_fabric_purplefire_01.jpg',
      'https://render.worldofwarcraft.com/classic-us/icons/56/inv_fabric_moonrag_01.jpg',
      'https://render.worldofwarcraft.com/classic-us/icons/56/inv_fabric_netherweave.jpg',
      'https://render.worldofwarcraft.com/classic-us/icons/56/inv_fabric_soulcloth.jpg',
    ]
  
  return (
    <Box display='flex' height='60px' width='225px' bg='green.200'>
      <Box display='flex' width='60px' alignItems='center' justifyContent='center'>
        <Image src={images[GenRandomInt(0, images.length)]} height='48px' width='48px' border='4px solid white'/>
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
  const { setReagentPrices } = useContext(ReagentPricesContext);
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
      
      // update state
      setReagentPrices(data);
    };
    
    // invoke function
    fetchData()
      .catch(console.error);
      
  }, [profession, realm, faction]);
  
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
              <ItemClassAccordion name='Item Class 1'/>
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