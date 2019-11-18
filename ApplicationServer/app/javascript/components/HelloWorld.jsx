import PropTypes from 'prop-types';
import React from 'react';
import About from './About';
import Meeting from './Meeting';
import { Link } from 'react-router-dom'
import "../../assets/stylesheets/index.css";
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
        <div className="index">
          <body body id="page-top">
          <Navbar class="navbar" expand="lg" sticky="top">
            <Navbar.Brand href="#home">SMART MEETING</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
              <Nav className="ml-auto">
                <Nav.Link class="a1" href="#about">About</Nav.Link>
                <Nav.Link class="a1" href="/meeting">Meeting</Nav.Link>
              </Nav>
            </Navbar.Collapse>
          </Navbar>

            <header class="text-white">
              <div class="container text-center">
                <h1>Welcome to Smart Meeting</h1>
                <p class="lead">We provide powerful tools to keep your conferences efficient and meaningful</p>
                <Button bsClass="custom-btn" href="/meeting"> Get Started </Button>
              </div>
            </header>

            <section id="about">
              <div class="container">
                <div class="row">
                  <div class="col-lg-8 mx-auto">
                    <h2>About the product</h2>
                    <p class="lead">Smart Meeting currently features:</p>
                    <ul>
                      <li>Raw transcription with speaker labels.</li>
                      <li>Summary of your meeting.</li>
                      <li>List of action items to be completed.</li>
                      <li>List of questions asked during the meeting.</li>
                    </ul>
                  </div>
                </div>
              </div>
            </section>

            <footer class="py-5 bg-dark">
              <div class="container">
                <p class="m-0 text-center text-white">2019-2020 CS Capstone</p>
              </div>
            </footer>

            <script src="js/scrolling-nav.js"></script>
          </body>
      </div>
    );
  }
}
