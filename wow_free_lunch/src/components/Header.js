import { useContext } from 'react';
import {
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

import logo from '../assets/logo.png';

import { Faction, FactionContext } from '../state/FactionContext';
import { Nav, NavContext } from '../state/NavContext';
import { Profession, ProfessionContext } from '../state/ProfessionContext';
import { RealmContext } from '../state/RealmContext';


// ===========
// Nav Section
// ===========


// component for nav buttons in header
// TODO: remove hard-coded navkey prop
const NavButtons = () => {
  return (
    <ButtonGroup colorScheme="teal" spacing="2">
      <NavButton name="Home" navkey={Nav.HOME}/>
      <NavButton name="Profession" navkey={Nav.PROFESSION}/>
      <NavButton name="About" navkey={Nav.ABOUT}/>
    </ButtonGroup>
  )
}


// component for individual nav button in header
const NavButton = (props) => {
  
  const { nav, setNav } = useContext(NavContext);
  
  const variant = (nav.name === props.name ? "solid" : "ghost");
  
  return (
    
      <Button 
        variant={variant}
        onClick={() => {setNav(props.navkey)}}
      >
        {props.name}
      </Button>
    
  )
}


// ==============
// Realm Selector
// ==============


// manager displaying the Realm Selector
const RealmSelectorManager = () => {
  
  const { nav } = useContext(NavContext);
  
  return (
    <>
      {nav.display_realm && <RealmSelector />}
    </>
  )
}


// component for Realm Selector
const RealmSelector = () => {
  
  const { realm, setRealm } = useContext(RealmContext);
  const { faction, setFaction } = useContext(FactionContext);
  
  const factionColorScheme = (faction.name === Faction.HORDE ? "red" : "blue");
  
  return (
    <>
      <Menu>
        <MenuButton as={Button} colorScheme="blackAlpha">
          {realm.name}
        </MenuButton>
        <MenuList>
          <MenuItem onClick={() => {setRealm({name: "Angerforge"})}}>Angerforge</MenuItem>
          <MenuItem onClick={() => {setRealm({name: "Skyfury"})}}>Skyfury</MenuItem>
        </MenuList>
      </Menu>
      <Menu>
        <MenuButton as={Button} colorScheme={factionColorScheme}>
          {faction.name}
        </MenuButton>
        <MenuList>
          <MenuItem onClick={() => {setFaction({name: Faction.ALLIANCE})}}>Alliance</MenuItem>
          <MenuItem onClick={() => {setFaction({name: Faction.HORDE})}}>Horde</MenuItem>
        </MenuList>
      </Menu>
    </>
  )
}


// ==============
// Profession Bar
// ==============


// component for Profession buttons in Profession Bar
const ProfessionButton = (props) => {
  
  const { profession, setProfession } = useContext(ProfessionContext);
  
  const variant = (profession.name === props.profession ? "solid" : "ghost");

  return (
      <Button 
        variant={variant}
        onClick={() => {setProfession({name: props.profession})}}
      >
        {props.name}
      </Button>
  )
}

// component for Profession Bar
// TODO: change this to a map function
const ProfessionBar = () => {
  return (
    <Box display="flex" width="100%" bg="gray.200" alignItems="center" >
      <ButtonGroup width="100%" colorScheme="blue" size='sm' p={2} spacing={2} justifyContent="center" flexWrap="wrap">
        <ProfessionButton name="Alchemy" profession={Profession.ALCHEMY}/>
        <ProfessionButton name="Blacksmithing" profession={Profession.BLACKSMITHING}/>
        <ProfessionButton name="Cooking" profession={Profession.COOKING}/>
        <ProfessionButton name="Engineering" profession={Profession.ENGINEERING}/>
        <ProfessionButton name="Inscription" profession={Profession.INSCRIPTION}/>
        <ProfessionButton name="Jewelcrafting" profession={Profession.JEWELCRAFTING}/>
        <ProfessionButton name="Leatherworking" profession={Profession.LEATHERWORKING}/>
        <ProfessionButton name="Tailoring" profession={Profession.TAILORING}/>
      </ButtonGroup>
    </Box>
  )
}

// manager displaying the Realm Selector
const ProfessionBarManager = () => {
  
  const { nav } = useContext(NavContext);
  
  return (
    <>
      {nav.display_profession && <ProfessionBar />}
    </>
  )
}


// ==============
// Main Component
// ==============


// Header content
const HeaderContent = () => {
  return (
    <>
      <Box display="flex" bg="gray.300" flexWrap='wrap'>
        <Box display="flex" alignItems="flex-end">
          <Image src={logo} h="100"/>
          <NavButtons />
        </Box>
        <Spacer />
        <Box display="flex" alignItems="flex-end" justifyContent="flex-end">
          <RealmSelectorManager />
        </Box>
      </Box>    
      <ProfessionBarManager />
    </>
  )
}


// Header component
export const Header = () => {
  return (
    <HeaderContent />
  )
};
