import {
  Box,
  Button,
  ButtonGroup,
  Heading,
  Highlight,
  Icon,  
  Link,
  List,
  ListIcon,
  ListItem,
  Popover,
  PopoverArrow,
  PopoverTrigger,
  PopoverContent,
  PopoverBody,  
  Text,
} from '@chakra-ui/react';

import { BiChevronRight } from 'react-icons/bi'
import { CgCheckO } from 'react-icons/cg'
import { SiGithub, SiGmail, SiLinkedin, SiInstagram, } from 'react-icons/si'

import { BattleDotNetIcon, DiscordIcon } from '../assets/Icons'
import { useWindowDimensions } from '../hooks/WindowDimensions'

// ==================
// Section Components
// ==================


// Section Header

const SectionHeader = (props) => {
  return (
    <Box display='flex' alignItems='center' justifyContent='center' height='48px' fontWeight='medium' bg='teal.500' color='white' p='10px 14px'>
      {props.content}
    </Box>
  )
}


// What Is

const WhatIs = () => {
  
  const { width } = useWindowDimensions();
  
  const freeLunchWiki = 'https://en.wikipedia.org/wiki/There_ain%27t_no_such_thing_as_a_free_lunch'
  const npcWiki = 'https://en.wikipedia.org/wiki/Non-player_character'
  
  return (
    <Box m='10px 0px'>
      <SectionHeader content='What is WoW Free Lunch?' />
      <Text p='10px 14px' textAlign='center'>
        WoW Free Lunch helps players identify opportunities to 
        earn risk-free, in-game gold (ie. a "
        <Link fontWeight='medium' color='teal' href={freeLunchWiki} isExternal>
          Free Lunch
        </Link>
        )" by crafting and selling items 
      </Text>
      <Box bg='gray.200' borderRadius='12px' maxWidth='475px' m={width >= 500 ? 'auto' : '10px 14px'}>
        <Text p='10px' fontStyle='italic' fontSize='2xl' color='teal' textAlign='center'>
          "There's no such thing as a free lunch"
          <br/>
          ...except in Azeroth
        </Text>
      </Box>
      <Text p='10px 14px' textAlign='center'>
        The idea is to use reagent prices from the auction house to identify craftable 
        items using those reagents that can be sold profitably to{' '}
        <Link href={npcWiki} isExternal>NPCs</Link> 
      </Text>
    </Box>
  )
}


// How to Use

const ChevronIcon = () => {
  return (
    <ListIcon as={BiChevronRight} color='teal' boxSize='20px' m='2px'/>
  )
}

const ListBlurb = (props) => {
  return (
    <ListItem p='0px 14px'>
      <Box display='flex'>
        <ChevronIcon />
        <Text>
          <Highlight 
            query={props.query || []} 
            styles={{fontWeight: 'medium', color: 'teal'}}
          >
            {props.content}
          </Highlight>
        </Text>
      </Box>
    </ListItem>    
  )
}

const HowToUse = () => {
  
  return (
    <Box m='10px 0px'>
      <SectionHeader content='How do I use this website?' />
      
      <Heading p='10px 14px' as='h2' size='sm' color='teal' textAlign='center'>
        How to Use Each Page
      </Heading>
      <List spacing='6px'>
        <ListBlurb 
          query='home'
          content='Home: Displays all identified Free Lunches across all 
            professions'
        />
        <ListBlurb 
          query='profession:'
          content='Profession: Displays all craftable items for a profession in
            addition to the reagent prices used in calculations'
        />
      </List>
      
      <Heading p='20px 14px 10px 14px' as='h2' size='sm' color='teal' textAlign='center'>
        How to Read Each Table
      </Heading>
      <List spacing='6px'>
        <ListBlurb 
          query='vendor price:'
          content='Vendor Price: The price at which the crafted item can
            be sold to an NPC'
        />
        <ListBlurb 
          query='cost:'
          content='Cost: The estimated cost (based on auction prices) to
            craft the item'
        />
        <ListBlurb 
          query='unit profit:'
          content='Unit Profit: The expected profit from buying the
            reagents, crafting the item, then selling the item to an NPC'
        />
        <ListBlurb 
          query='profit margin:'
          content='Profit Margin: The Unit Profit divided by the Cost'
        />
      </List>      
      
      <Text p='20px 10px 10px 10px' fontStyle='italic' textAlign='center'>
        Note that Free Lunches are identified only for select WoW Classic realms
      </Text>
    </Box>
  )
}


// Accuracy

const Accuracy = () => {
  
  return (
    <Box m='10px 0px'>
      <SectionHeader content='Are these Free Lunches real?' />
      <Text p='10px 14px 20px' textAlign='center'>
        This website is designed to indicate whether opportunities exist and 
        should not be used at face value due to challenges such as
      </Text>
      
      <List spacing='6px'>
        <ListBlurb 
          content='Refreshing auction data at 3 hour intervals'
        />
        <ListBlurb 
          content='Simplifying calculations by using only the lowest prices 
          instead of the "order book"'
        />
        <ListBlurb 
          content='Using API data with known issues'
        />
      </List>
      
      <Text p='20px 14px 10px' textAlign='center'>
        Despite these challenges, if an item is frequently identified
        as a Free Lunch it is probably worth looking into
      </Text>
    </Box>
  )
}


// Contact

const ButtonLink = (props) => {
  return (
    <Box p='6px 0px'>
      <Link href={props.url} isExternal style={{textDecoration: 'none'}}>
        <Button 
          bg={props.bgColor} 
          _hover={{bg: props.hoverColor}} 
          leftIcon={<Icon as={props.icon} boxSize='16px'/>}
        >
          {props.label}
        </Button>
      </Link>
    </Box>
  )
}


const copyBattleTagToClipboard = async () => {

  const battleTag = 'Kowotani#1229'
    
  await navigator.clipboard.writeText(battleTag)
}


const ButtonCopyToClipboard = (props) => {
  return (
    
    <Box p='6px 0px'>
      <Popover gutter={12}>
        <PopoverTrigger>
          <Button 
            bg={props.bgColor} 
            _hover={{bg: props.hoverColor}} 
            leftIcon={<Icon as={props.icon} boxSize='16px'/>}
            onClick={props.onClick}
          >
            {props.label}
          </Button>
        </PopoverTrigger>
        <PopoverContent h='40px' w='190px' borderRadius='20px' bg='green.400' borderColor='green.400' color='white'>
          <PopoverArrow bg='green.400'/>
          <PopoverBody display='flex' alignItems='center' justifyContent='center'>
            <Icon as={CgCheckO} boxSize='20px' p='0px 4px 0px 0px'/>
            <Box>
              Copied to Clipboard
            </Box>
          </PopoverBody>
        </PopoverContent>
      </Popover>
    </Box>
  )
}


const Contact = () => {
  
  const urlDiscord = 'https://discord.com/users/283464182253355008'
  const urlEmail = 'mailto:wowfreelunch@gmail.com'
  const urlGithub = 'https://github.com/Kowotani'
  const urlInstagram = 'https://www.instagram.com/kowotani/'
  const urlLinkedIn = 'https://www.linkedin.com/in/jckyoung/'
  
  return (
    <Box m='10px 0px'>
      <SectionHeader content='How can I contact you?' />
      <Text p='10px 14px' textAlign='center'>
        Feel free to reach out via any of the following
      </Text>
      <Box display='flex'>
        <ButtonGroup
          width='100%'
          color='white'
          size='md' 
          spacing='10px' 
          alignItems='center'
          justifyContent='center' 
          flexWrap='wrap'
        >
          <ButtonLink label='Email' url={urlEmail} bgColor='#DB4437' hoverColor='#AD332E' icon={SiGmail}/>
          <ButtonLink label='LinkedIn' url={urlLinkedIn} bgColor='#0077B5' hoverColor='#005682' icon={SiLinkedin}/>
          <ButtonLink label='Discord' url={urlDiscord} bgColor='#7289da' hoverColor='#687DC4' icon={DiscordIcon}/>
          <ButtonCopyToClipboard label='Battle.net' onClick={copyBattleTagToClipboard} bgColor='#148EFF' hoverColor='#0F71C6' icon={BattleDotNetIcon}/>
          <ButtonLink label='Instagram' url={urlInstagram} bgColor='#833AB4' hoverColor='#612C87' icon={SiInstagram}/>
          <ButtonLink label='GitHub' url={urlGithub} bgColor='#333' hoverColor='#545454' icon={SiGithub}/>
        </ButtonGroup>
      </Box>
    </Box>
  )
}


// ==============
// Main Component
// ==============

// About component

export const About = () => {
  return (
    <>
      <WhatIs />
      <HowToUse />
      <Accuracy />
      <Contact />
    </>
  )
}