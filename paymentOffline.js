// This script will prepare, sign, and submit a payment. It is offered as is,
// and may contain errors or bugs. Use it at your own risk.


'use strict';
//use ripple-lib
const RippleAPI = require('ripple-lib').RippleAPI;
const api = new RippleAPI();

//sending address (string)
const address = 'rMH4UxPrbuMa1spCBR98hLLyNJp4d8p4tM';

//Secret for sending address (string)
const secret = 'secretkey';

//Destination (DT must be an integer)
const dstAddress = 'rpZc4mVfWUif9CRoHRKKcmhu1nx2xktxBo'
const dstTag = 030301;

const instructions = {
	"fee": '.000012',
	//Adjust sequence number so it is equal to the previous transaction's sequence + 1
	"sequence": 1,
	//Adjust maxLedgerVersion to specify by which ledger the transaction must be included
	"maxLedgerVersion": 4000000
	};

const payment = {
  "source": {
	  "address": address,
      "maxAmount": {
	    "value": '1',
	    "currency": 'XRP'
	  },
  },
  "destination": {
    "address": dstAddress,
    //Comment the next line if no destination tag is required
    "tag": dstTag,
    "amount": {
      "value": '1',
      "currency": 'XRP'
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
  return api.preparePayment(address, instructions, payment).then(prepared => {
    console.log('Success! Payment transaction prepared...');
    //const {signedTransaction} = api.sign(prepared.txJSON, secret);
    //console.log('Payment transaction signed...');
    //api.submit(signedTransaction).then(quit, fail);
  });
}).catch(fail);
