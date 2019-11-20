import React from 'react';
import PropTypes from 'prop-types';

export default class Meeting extends React.Component {
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
    this.state = { users: this.props.users };
  }

  updateName = (users) => {
    this.setState({ users });
  };

  render() {
    return (
      <div>
        <h3>
          This is the Meeting page! It is {this.state.users}.
        </h3>
      </div>
    );
  }
}
