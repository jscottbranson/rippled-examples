//NOTE: This sample code is provided as is. It has not been tested. Use at your own risk.
//You are the only person responsible for what you do with this code
//
//
//ALSO NOTE: This code will not set the appropriate flag to prevent your balances from rippling.
//if you trust more than one counterparty with IOUs, you risk your balances changing
//without your control, unless you disable rippling on ALL trust lines


'use strict';
//use ripple-lib
const RippleAPI = require('ripple-lib').RippleAPI;


//Your wallet info
const address = 'Put your wallet address as a string here';
const secret = 'Put your secret as a string here';

//Other variables
const fee = {
	maxFee: '.000010'
	};

//Adjust this to the current ledger + ~4.
//Ideally, use an API call to do this automatically
const last_ledger = {
		'LastLedgerSequence': 37910550
	};


//Rippled server - change as needed
const api = new RippleAPI({server: 'wss//s1.ripple.com:443'});

//Change the following settings according to your needs
//limit is the most value you trust the counterparty to issue to you
const settings = {
		'currency': 'USD',
		'counterparty': 'rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B',
		'limit': '1000'
};
	

function quit(message) {
  console.log(message);
  process.exit(0);
}

function fail(message) {
  console.error(message);
  process.exit(1);
}

api.connect().then(() => {
  console.log('Preparing the transaction...');
  return api.prepareTrustline(address, settings, fee, last_ledger).then(prepared => {
    console.log('Success! Transaction prepared...');
    const {signedTransaction} = api.sign(prepared.txJSON, secret);
    console.log('Transaction signed...');
    api.submit(signedTransaction).then(quit, fail);
  });
}).catch(fail);
