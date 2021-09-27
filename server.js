const express = require('express');
const app = express();
const configRoutes = require('./routes');
const routeNum = '8888'
//Loads the handlebars module
const session = require('express-session');
const exphbs = require('express-handlebars');
//Sets our app to use the handlebars engine
app.engine('handlebars', exphbs({ defaultLayout: 'main' }));
app.set('view engine', 'handlebars');
var uuid = require('uuid');
//var exphbs = require('express-handlebars');
app.disable('etag');
app.use(session({secret: uuid.v4()}));
app.use(express.json());

//-------------------------------------------------------------//
configRoutes(app)
//-------------------------------------------------------------//

app.listen(process.env.PORT || '8888', function () {
  console.log(`Your app is listening on port ${routeNum}.`);
});