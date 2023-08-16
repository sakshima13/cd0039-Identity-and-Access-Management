export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'coffee-shop-udacity01.us', // the auth0 domain prefix
    audience: 'http://127.0.0.1:5000/api/v2', // the audience set for the auth0 app
    clientId: 'NmPvTxKFj23u51uSasVtTsMPd8692rZM', // the client id generated for the auth0 app
    callbackURL: 'https://localhost:3000', // the base url of the running ionic application. 
  }
}