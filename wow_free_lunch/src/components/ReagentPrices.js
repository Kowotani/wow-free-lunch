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


// ==============
// Main Component
// ==============


// Header component
export const ReagentPrices = () => {
  return (
    <ProfessionProvider>
      <p>Reagent Prices</p>
    </ProfessionProvider>
  )
};