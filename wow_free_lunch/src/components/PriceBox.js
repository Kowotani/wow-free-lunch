import {useState } from 'react';
import {
  Box,
  Image,
} from '@chakra-ui/react';
import goldCoin from '../assets/gold_coin.png'
import silverCoin from '../assets/silver_coin.png'
import copperCoin from '../assets/copper_coin.png'


// coin enum
const Coin = {
  GOLD: 'gold',
  SILVER: 'silver',
  COPPER: 'copper'
}


// ============
// Currency Box
// ============


// CurrencyBox component
export const CurrencyBox = (props) => {
  
  let coin;
  switch (props.coin) {
    case Coin.GOLD:
      coin = goldCoin;
      break;
    case Coin.SILVER:
      coin = silverCoin;
      break;
    case Coin.COPPER:
      coin = copperCoin;
      break;
  }
  
  return (
    <Box display="flex" height="20px" alignItems="center">
      <Box p={1}>{props.value}</Box>
      <Image src={coin} p={1}/>
    </Box>
  )
}


// ==============
// Main Component
// ==============


// PriceBox component
export const PriceBox = (props) => {
  
  const goldAmount = Math.floor(props.price / 10000);
  const silverAmount = Math.floor((props.price / 100)) % 100;
  const copperAmount = props.price % 100;
  
  return (
    <Box display="flex" height="20px">
      {goldAmount > 0 && <CurrencyBox value={goldAmount} coin={Coin.GOLD} />}
      {(props.price >= 100 || silverAmount > 0) && <CurrencyBox value={silverAmount} coin={Coin.SILVER} />}
      <CurrencyBox value={copperAmount} coin={Coin.COPPER} />
    </Box>
  )
};