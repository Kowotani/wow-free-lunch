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
    default:
      console.log('Expected coin paramter in CurrencyBox props');
  }
  
  return (
    <Box 
      display='flex' 
      height='20px' 
      padding='0px 4px'
      alignItems='center' 
      justifyContent='flex-end' 
      color={props.isNegative ? 'red' : 'black'} 
    >
      {props.hasNegativeSign ? <Box color='red'>-</Box>: null}
      <Box padding={coin === goldCoin ? '0px 2px 0px 0px' : '0px 2px 0px 2px'}>{props.zeroPad ? '0' : null}{props.amount}</Box>
      <Image src={coin} />
    </Box>
  )
}


// ==============
// Main Component
// ==============


// PriceBox component
export const PriceBox = (props) => {
  
  const isNegative = props.price < 0;
  
  const goldAmount = Math.floor(Math.abs(props.price) / 10000);
  const silverAmount = Math.floor((Math.abs(props.price) / 100)) % 100;
  const copperAmount = Math.abs(props.price) % 100;
  
  return (
    <Box 
      display='flex' 
      height='20px'
      minWidth='140px'
      justifyContent='flex-end'
    >
      {goldAmount > 0 &&
        <CurrencyBox 
          amount={goldAmount} 
          coin={Coin.GOLD} 
          isNegative={isNegative}
          hasNegativeSign={isNegative && goldAmount > 0}
        />
      }
      {(goldAmount > 0 || silverAmount > 0) &&
        <CurrencyBox 
          amount={silverAmount} 
          coin={Coin.SILVER} 
          isNegative={isNegative}
          hasNegativeSeign={isNegative && goldAmount === 0 && silverAmount > 0}
          zeroPad={goldAmount > 0 && silverAmount < 10}
        />
      }
      <CurrencyBox 
        amount={copperAmount} 
        coin={Coin.COPPER} 
        isNegative={isNegative}
        hasNegativeSign={isNegative && goldAmount === 0 && silverAmount === 0}
        zeroPad={silverAmount > 0 && copperAmount < 10}
      />
    </Box>
  )
};