import React, { Component } from 'react';
import SetupForm from './SetupForm';

class App extends Component {
    render() {
      return (
        <div>
          <h3>Cosine similarity simulation</h3>
          <div className="row">
            <div className="col-md-12">
              <SetupForm />
            </div>
          </div>
        </div>
      );
    }
  }
  
const formContainer = document.querySelector('#formContainer')
ReactDOM.render(App, formContainer);
