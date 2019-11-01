import ReactOnRails from 'react-on-rails';
import React from 'react';
import ReactDOM from 'react-dom';
import App from '../components/App';
import { BrowserRouter as Router, Route} from 'react-router-dom';
import HelloWorld from '../components/HelloWorld';
import About from '../components/About';

// This is how react_on_rails can see the HelloWorld in the browser.
ReactOnRails.register({
  HelloWorld,
  About,
});

document.addEventListener('DOMContentLoaded', () => {
  ReactDOM.render(
      <Router>
        <Route path="/" component={App} />
      </Router>,
      document.body.appendChild(document.createElement('div')),
  );
});
