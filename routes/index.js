const spotifyApiRoutes = require('./spotify-api');
const clientRoutes = require('./client-routes');

const constructorMethod = (app) => {
  app.use('/', spotifyApiRoutes);
  app.use('/u', clientRoutes);

  app.use('*', (req, res) => {
    res.sendStatus(404);
  });
};

module.exports = constructorMethod;