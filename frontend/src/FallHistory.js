// // src/FallChart.js
// import React, { useEffect, useRef } from 'react';
// import Chart from 'chart.js/auto'; // Automatically registers the necessary components

// const FallChart = ({ fallData }) => {
//   const canvasRef = useRef(null);
//   const chartRef = useRef(null);

//   useEffect(() => {
//     const ctx = canvasRef.current.getContext('2d');

//     // Destroy the previous chart instance if it exists
//     if (chartRef.current) {
//       chartRef.current.destroy();
//     }

//     const data = {
//       datasets: [
//         {
//           label: 'Fall Data',
//           data: fallData.map((entry, index) => ({
//             x: index, // Use index as x-coordinate
//             y: 0, // Single row
//             backgroundColor: entry.fall === 1 ? 'red' : 'green', // Color based on fall value
//             radius: 15, // Size of each block
//           })),
//           borderColor: 'rgba(0, 0, 0, 0.1)',
//           borderWidth: 1,
//         }
//       ]
//     };

//     const options = {
//       responsive: true,
//       plugins: {
//         legend: {
//           position: 'top',
//         },
//         title: {
//           display: true,
//           text: 'Fall Data Pixel Graph',
//         },
//       },
//       scales: {
//         x: {
//           type: 'linear',
//           position: 'bottom',
//           ticks: {
//             stepSize: 1,
//             callback: (value) => fallData[value]?.time || '' // Show the time on x-axis
//           },
//           grid: {
//             display: false
//           }
//         },
//         y: {
//           type: 'linear',
//           position: 'left',
//           min: -1,
//           max: 1,
//           ticks: {
//             display: false // Hide y-axis ticks
//           },
//           grid: {
//             display: false
//           }
//         }
//       }
//     };

//     chartRef.current = new Chart(ctx, {
//       type: 'scatter',
//       data: data,
//       options: options
//     });

//     // Cleanup function to destroy the chart instance
//     return () => {
//       if (chartRef.current) {
//         chartRef.current.destroy();
//       }
//     };
//   }, [fallData]);

//   return (
//     <div>
//       <canvas ref={canvasRef} />
//     </div>
//   );
// };

// export default FallChart;


import React from 'react';
import './FallHistory.css'; // Import the CSS file for styling

function TimeList({ fallData }) {
  return (
    <div className="time-list">
      <div className="list-header">
        <div className="header-item">Time</div>
        <div className="header-item">Time on the Ground</div>
      </div>
      {fallData.map((item, index) => (
        <div key={index} className="list-item">
          <div className="item-field">{item.time}</div>
          <div className="item-field">{item.timeOnGround}</div>
        </div>
      ))}
    </div>
  );
}

export default TimeList;