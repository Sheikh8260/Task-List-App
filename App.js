import React from 'react';
import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import TaskList from './components/TaskList';
import Task from './components/Task';

function App() {
  return (
    <Router>
      <Switch>
        <Route path="/login" component={Login} />
        <Route path="/register" component={Register} />
        <Route path="/task-lists" component={TaskList} />
        <Route path="/tasks/:id" component={Task} />
        <Redirect from="/" to="/login" />
      </Switch>
    </Router>
  );
}

export default App;