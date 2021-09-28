const express = require('express');
const app = express();
const configRoutes = require('./routes');
const routeNum = '8888'
//Loads the handlebars module
const session = require('express-session');
const exphbs = require('express-handlebars');
const cors = require('cors');
//Sets our app to use the handlebars engine
app.engine('handlebars', exphbs({ defaultLayout: 'main' }));
app.set('view engine', 'handlebars');
var uuid = require('uuid');
//var exphbs = require('express-handlebars');
app.use(cors());
app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", '*');
  res.header("Access-Control-Allow-Credentials", true);
  res.header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS');
  res.header("Access-Control-Allow-Headers", 'Origin,X-Requested-With,Content-Type,Accept,content-type,application/json');
  next();
});
app.use(session({secret: uuid.v4()}));
app.use(express.json());

//-------------------------------------------------------------//
configRoutes(app)
//-------------------------------------------------------------//

app.listen(process.env.PORT || '8888', function () {
  console.log(`Your app is listening on port ${routeNum}.`);
});