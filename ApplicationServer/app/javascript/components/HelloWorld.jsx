import PropTypes from 'prop-types';
import React from 'react';
import About from './About';
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
          <div class="container-fluid">
            <Nav class="navbar navbar-expand-lg fixed-top" id="mainNav">
            <a class="navbar-brand js-scroll-trigger text-white" href="#page-top">SMART MEETING</a>
              <Button class="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
                <i class="fas fa-bars"></i>
                <span class="navbar-toggler-icon"></span>
             </Button>

                <div class="collapse navbar-collapse" id="navbarResponsive">
                  <ul class="navbar-nav ml-auto">
                    <li class="nav-item">
                      <a class="nav-link js-scroll-trigger a1" href="#about">About</a>
                    </li>
                  </ul>
                </div>
            </Nav>
           </div>

            <header class="text-white">
              <div class="container text-center">
                <h1>Welcome to Smart Meeting</h1>
                <p class="lead">We provide powerful tools to keep your conferences efficient and meaningful</p>
                <Button bsClass="custom-btn" href="#"> Get Started </Button>
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
