const express = require('express');
const app = express();
const configRoutes = require('./routes');
const routeNum = '8888'
app.use(express.json());

//-------------------------------------------------------------//
configRoutes(app)
//-------------------------------------------------------------//

app.listen('8888', function () {
  console.log(`Your app is listening on port ${routeNum}.`);
});
