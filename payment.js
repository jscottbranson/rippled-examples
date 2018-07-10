// This script will prepare, sign, and submit a payment. It is offered as is,
// and may contain errors or bugs. Use it at your own risk.


'use strict';
//use ripple-lib
const RippleAPI = require('ripple-lib').RippleAPI;

//sending address (string)
const address = 'rxxxxxxxxxxxxxx';

//Secret for sending address (string)
const secret = 'ssh... It's secret.';

//Destination (DT must be an integer)
const dstAddress = 'r......';
const dstTag = 000000;


//Rippled server - Don't use servers you don't control/trust
const api = new RippleAPI({server: 'wss://10.10.10.10'});

const fee = {
	maxFee: '.000012'
};

const payment = {
  source: {
	  address: address,
      maxAmount: {
	    value: '01.000012',
	    currency: 'XRP'
	  },
  },
  destination: {
    address: dstAddress,
    //Comment the next line if no destination tag is required
    tag: dstTag,
    amount: {
      value: '01',
      currency: 'XRP'
    }
  }
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
  console.log('Preparing the payment transaction...');
  return api.preparePayment(address, payment, fee).then(prepared => {
    console.log('Success! Payment transaction prepared...');
    const {signedTransaction} = api.sign(prepared.txJSON, secret);
    console.log('Payment transaction signed...');
    api.submit(signedTransaction).then(quit, fail);
  });
}).catch(fail);
