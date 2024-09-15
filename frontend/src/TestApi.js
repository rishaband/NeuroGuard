import React, { useEffect, useState } from 'react';
import axios from 'axios';

const TestApi = () => {
  const [message, setMessage] = useState('');

  useEffect(() => {
    // Call the /test endpoint
    axios.get('http://127.0.0.1:5000/test')
      .then(response => {
        setMessage(response.data);
      })
      .catch(error => {
        console.error('There was an error making the request:', error);
      });
  }, []);

  return (
    <div>
      {/* <h1>Test API Response</h1> */}
      <h1>{message}</h1>
    </div>
  );
};

export default TestApi;