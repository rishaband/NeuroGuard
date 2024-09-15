// src/Main.js
import React, { useRef, useEffect } from 'react';
import './Main.css'; // For styling
import FixedButton from './FixedButton';

function Main() {
  const videoRef = useRef(null);

  useEffect(() => {
    const video = videoRef.current;

    const startVideo = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        video.play();
      } catch (err) {
        console.error("Error accessing webcam:", err);
      }
    };

    startVideo();
  }, []);

  return (
    <div className="main-container">
      <h1>Live Webcam Feed</h1>
      <div className="video-container">
        <video ref={videoRef} width="640" height="480" autoPlay />
      </div>
      <FixedButton />
    </div>
  );
}

export default Main;
