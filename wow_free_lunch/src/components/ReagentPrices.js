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
} from '@chakra-ui/react';

import { Nav, NavContext, NavProvider } from '../state/NavContext';
import { RealmContext, RealmProvider } from '../state/RealmContext';
import { Faction, FactionContext, FactionProvider } from '../state/FactionContext';
import { Profession, ProfessionContext, ProfessionProvider } from '../state/ProfessionContext';


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
    <>
      <p>Reagent PriceBox</p>
    </>
  )
  
}


// ==============
// Main Component
// ==============


// Header component
export const ReagentPrices = () => {
  return (
    <ProfessionProvider>
      <ReagentPriceBox />
    </ProfessionProvider>
  )
};