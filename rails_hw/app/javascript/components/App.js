/* eslint-disable */
import React from 'react';
import HelloWorld from './HelloWorld';
import About from './About';
import { Route, Switch }  from 'react-router-dom';

class App extends React.Component {
  render () {
    return (
      <div>
        <Switch>
          <Route exact path="/" component={HelloWorld} />
          <Route exact path="/about" component={About} />
        </Switch>
      </div>
    )
  }
}

export default App;
