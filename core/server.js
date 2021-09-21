const express = require('express');
const app = express();
const configRoutes = require('./routes');
const routeNum = '8888'
//Loads the handlebars module
const exphbs = require('express-handlebars');
//Sets our app to use the handlebars engine
app.engine('handlebars', exphbs({ defaultLayout: 'main' }));
app.set('view engine', 'handlebars');

app.use(express.json());

//-------------------------------------------------------------//
configRoutes(app)
//-------------------------------------------------------------//

app.listen('8888', function () {
  console.log(`Your app is listening on port ${routeNum}.`);
});