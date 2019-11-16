import PropTypes from 'prop-types';
import React from 'react';
import About from './About';
import { Link } from 'react-router-dom'
import Jumbotron from "react-bootstrap/Jumbotron";
import Container from "react-bootstrap/Container";
import Button from "react-bootstrap/Button";
import Navbar from "react-bootstrap/Navbar";
import Nav from "react-bootstrap/Nav";
import NavItem from "react-bootstrap/NavItem";
import NavDropdown from "react-bootstrap/NavDropdown";

export default class HelloWorld extends React.Component {
  static propTypes = {
    name: PropTypes.string.isRequired, // this is passed from the Rails view
  };
  /**
   * @param props - Comes from your rails view.
   */
  constructor(props) {
    super(props);

    // How to set initial state in ES6 class syntax
    // https://reactjs.org/docs/state-and-lifecycle.html#adding-local-state-to-a-class
    this.state = { name: this.props.name };
  }

  updateName = (name) => {
    this.setState({ name });
  };

  render() {
    return (

      <div>
        <Navbar bg="light" expand="lg">
          <Navbar.Brand href="/">SMART MEETING</Navbar.Brand>
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="mr-auto">
               <Nav.Link href="/about">About</Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Navbar>
        <Container className="p-3">
           <Jumbotron>
             <h1 className="header">Welcome To SMART MEETING</h1>
             <h2 className="summary">We provide powerful tools to keep your conferences efficient and meaningful.</h2>
           </Jumbotron>
         </Container>

        <h3>
          Hello, {this.state.name}!
        </h3>

        <form >
          <label htmlFor="name">
            Say hi to:
          </label>
          <input
            id="name"
            type="text"
            value={this.state.name}
            onChange={(e) => this.updateName(e.target.value)}
          />
        </form>
      </div>
    );
  }
}
