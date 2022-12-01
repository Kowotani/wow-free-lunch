import {React, useState, useContext} from 'react';
import {
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
  Box,
  Button, 
  ButtonGroup,
  Image,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  Spacer,
  VStack
} from '@chakra-ui/react';

import { Nav, NavContext, NavProvider } from '../state/NavContext';
import { RealmContext, RealmProvider } from '../state/RealmContext';
import { Faction, FactionContext, FactionProvider } from '../state/FactionContext';
import { Profession, ProfessionContext, ProfessionProvider } from '../state/ProfessionContext';
import silk from '../assets/silk.png'
import { PriceBox } from './PriceBox'


// =======
// Filters 
// =======


// ====================
// Item Class Hierarchy
// ====================


// ===========
// Reagent Box
// ===========

// component for Reagent with price
const ReagentPriceBox = (props) => {
  
  return (
    <Box display="flex" height="60px" width="225px" bg="green.200">
      <Box display="flex" width="60px" alignItems="center" justifyContent="center">
        <Image src={silk} height="48px" width="48px" border="4px solid white"/>
      </Box>
      <Box display="flex" width="165px">
        <VStack>
          <Box display="flex" width="100%" alignItems="flex-end" fontWeight="semibold" padding="4px 4px 0px 4px">
            {props.name}
          </Box>
          <Box display="flex" width="100%" justifyContent="flex-end">
            <Box p="0px 4px 4px 0px">
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
      <ReagentPriceBox name="Silk Cloth" price={123456789}/>
    </ProfessionProvider>
  )
};