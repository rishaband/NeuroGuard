// src/FixedButton.js
import React from 'react';
import './FixedButton.css'; // Import the CSS file for styling

function FixedButton() {
  const handleClick = () => {
    // Define what happens when the button is clicked
    alert('Button clicked!');
  };

  return (
    <button className="fixed-button" onClick={handleClick}>
      ChatBot
    </button>
  );
}

export default FixedButton;