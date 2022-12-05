import {React, useState, useContext} from 'react';
import {
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
  Box,
  Image,
  Spacer,
  VStack
} from '@chakra-ui/react';

import { Profession, ProfessionContext, ProfessionProvider } from '../state/ProfessionContext';
import { PriceBox } from './PriceBox'


function GenRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min))
}


// =======
// Filters 
// =======


// ====================
// Item Class Hierarchy
// ====================

// component for Item Class accordion
const ItemClassAccordion = (props) => {
  
  const [itemSubclasses, setItemSubClasses] = useState();
  
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
  
  const [reagents, setReagents] = useState();
  
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
      <Box display='flex' width='165px'>
        <VStack>
          <Box display='flex' width='100%' alignItems='flex-end' fontWeight='semibold' padding='4px 4px 0px 4px'>
            {props.name}
          </Box>
          <Box display='flex' width='100%' justifyContent='flex-end'>
            <Box p='0px 4px 4px 0px'>
              <PriceBox price={props.price}/>
            </Box>
          </Box>
        </VStack>
      </Box>
    </Box>
  )
  
}


// ==============
// Main Component
// ==============


// Header component
export const ReagentPrices = () => {
  return (
    <ProfessionProvider>
      <ItemClassAccordion name='Item Class 1'/>
    </ProfessionProvider>
  )
};