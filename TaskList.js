import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

function TaskList() {
  const [taskLists, setTaskLists] = useState([]);

  useEffect(() => {
    const fetchTaskLists = async () => {
      const token = localStorage.getItem('token');
      const response = await axios.get('/lists', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setTaskLists(response.data);
    };

    fetchTaskLists();
  }, []);

  return (
    <div>
      <h2>Task Lists</h2>
      <ul>
        {taskLists.map((taskList) => (
          <li key={taskList._id}>
            <Link to={`/tasks/${taskList._id}`}>{taskList.name}</Link>
          </li>
        ))}
      </ul