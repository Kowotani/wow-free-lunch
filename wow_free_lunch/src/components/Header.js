import { useContext, useEffect, useState, createRef, forwardRef, useLayoutEffect, useRef, } from 'react';
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

import { CSSTransition } from 'react-transition-group'

import logo from '../assets/logo.png';

import { useWindowDimensions } from '../hooks/WindowDimensions';

import { Faction, FactionContext } from '../state/FactionContext';
import { Nav, NavContext } from '../state/NavContext';
import { Profession, ProfessionContext } from '../state/ProfessionContext';
import { RealmContext } from '../state/RealmContext';

import '../styles.css';


// ===========
// Nav Section
// ===========


// component for nav buttons in header
// TODO: remove hard-coded navkey prop
const NavButtons = () => {
  return (
    <ButtonGroup colorScheme='teal' spacing={0}>
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
        borderBottomRightRadius='0px'
        borderBottomLeftRadius='0px'
        borderTopLeftRadius='10px'
        borderTopRightRadius='10px'
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
  
  const { nav } = useContext(NavContext);
  const { profession, setProfession } = useContext(ProfessionContext);
  
  const [ isProfessionNav, setIsProfessionNav ] = useState(false);
  
  const variant = (profession.name === props.profession ? "solid" : "ghost");
  
  useEffect(() => {
    
    // transition requires a toggle switching from false -> true
    setIsProfessionNav(nav.display_profession);
  }, [nav])  

  return (
      <CSSTransition
        timeout={500}
        in={isProfessionNav}
        classNames='professionbarbutton'
        unmountOnExit={true}
      >
        <Button 
          variant={variant}
          onClick={() => {setProfession({name: props.profession})}}
          m='6px'
        >
          {props.name}
        </Button>
      </CSSTransition>
  )
}

// component for Profession Bar
// TODO: change this to a map function
const ProfessionBar = forwardRef((props, ref) => {

  const { nav } = useContext(NavContext);

  return (
    <Box ref={ref}
        display='flex'
        width='100%' 
        bg='gray.100'
    >
      <ButtonGroup 
        width='100%' 
        colorScheme='blue' 
        size='sm' 
        spacing='0px' 
        alignItems='center'
        justifyContent='center' 
        flexWrap='wrap'
      >
        <ProfessionButton name='Alchemy' profession={Profession.ALCHEMY}/>
        <ProfessionButton name='Blacksmithing' profession={Profession.BLACKSMITHING}/>
        <ProfessionButton name='Cooking' profession={Profession.COOKING}/>
        <ProfessionButton name='Engineering' profession={Profession.ENGINEERING}/>
        <ProfessionButton name='Inscription' profession={Profession.INSCRIPTION}/>
        <ProfessionButton name='Jewelcrafting' profession={Profession.JEWELCRAFTING}/>
        <ProfessionButton name='Leatherworking' profession={Profession.LEATHERWORKING}/>
        <ProfessionButton name='Tailoring' profession={Profession.TAILORING}/>
      </ButtonGroup>
    </Box>
  )
})

// manager displaying the Realm Selector
const ProfessionBarManager = () => {
  
  const { nav } = useContext(NavContext);
  
  const [ isProfessionNav, setIsProfessionNav ] = useState(false);

  const { width } = useWindowDimensions();

  const nodeRef = createRef();
  
  
  useEffect(() => {
    
    // transition requires a toggle switching from false -> true
    setIsProfessionNav(nav.display_profession);
  }, [nav])
  
  
  useEffect(() => {
    
    // set the CSS height property for the ProfessionBar
    if (nodeRef.current?.offsetHeight !== undefined) {
      nodeRef.current?.style?.setProperty('--h', nodeRef.current?.offsetHeight + 'px');
    }
  }, [width])


  useEffect(() => {
    
    // set the CSS height property for the ProfessionBar
    if (width < 450) {
      nodeRef.current?.style?.setProperty('--h', '112px');
    } else if (width < 845) {
      nodeRef.current?.style?.setProperty('--h', '80px');
    }
  }, [nav])


  return (
    <>
      <CSSTransition 
        nodeRef={nodeRef}
        timeout={500}
        in={isProfessionNav}
        classNames='professionbar'
      >
        <ProfessionBar ref={nodeRef}/>
      </CSSTransition>
    </>
  )
}


// ==============
// Main Component
// ==============


// Header content
export const Header = () => {
  
  const [ realmSelectorLocation, setRealmSelectorLocation ] = useState('bottom');
  
  const { width } = useWindowDimensions();
  
  useEffect(() => {
    setRealmSelectorLocation(width < 525 ? 'top' : 'bottom')
  }, [width])
  
  
  return (
    <>
      <Box display='flex' bg='gray.300' flexWrap='wrap' borderBottom='4px' borderColor='teal.500'>
        <Image src={logo} h='100'/>
        <Box display='flex' flexGrow={1} flexDirection='column'>
        
          <Box display='flex' width='100%' flexGrow={1} justifyContent='flex-end'>
            <Spacer />
            {realmSelectorLocation === 'top' && <RealmSelectorManager />}
          </Box>
          
          <Box display='flex'>
            <Box display='flex' flexGrow={1} justifyContent='flex-start' alignItems='flex-end'>
              <NavButtons />
            </Box>
            <Spacer flexGrow={1} />
            <Box display='flex' flexGrow={1} justifyContent='flex-end'>
              {realmSelectorLocation === 'bottom' && <RealmSelectorManager />}
            </Box>
          </Box>
          
        </Box>
      </Box>    
      <ProfessionBarManager />
    </>
  )
}