// src/VideoStream.js
import React from 'react';

const VideoStream = () => {
  return (
    <div>
      <h1>Video Stream</h1>
      <img
        src="http://localhost:5000/video_feed"
        alt="Video Stream"
        style={{ width: '100%', height: 'auto' }}
      />
    </div>
  );
};

export default VideoStream;