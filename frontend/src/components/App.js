import React, {Component} from 'react';
import ReactDOM from 'react-dom';

class App extend Component {
    render() {
        return <h1>React App</h1>
    }
}

ReactDOM.render(<App />, document.getElementById('app'));