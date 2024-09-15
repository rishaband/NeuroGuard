import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Cookies from 'js-cookie';
import Login from './Login';
import Main from './Main';
import Navbar from './Navbar';
import FallHistory from './FallHistory';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  // const location = useLocation();
  const fallData = [
    {'time': '2023', 'timeOnGround': 2, 'fall': 1},
    {'time': '2024', 'timeOnGround': 1, 'fall': 0},
    {'time': '2022', 'timeOnGround': 10, 'fall': 1},
  ];

  useEffect(() => {
    const authToken = Cookies.get('authToken');
    if (authToken) {
      setIsAuthenticated(true);
    }
  }, []);

  return (
    <Router>
      {/* {isAuthenticated && location.pathname !== '/login' && <Navbar />} */}
      <Routes>
        <Route
          path="/login"
          element={isAuthenticated ? <><Navbar /> <Navigate to="/main" /></> : <Login setIsAuthenticated={setIsAuthenticated} />}
        />
        <Route
          path="/main"
          element={isAuthenticated ? <><Navbar /> <Main /> </> : <Navigate to="/login" />}
        />
        <Route
          path="/fallHistory"
          element={isAuthenticated ? <><Navbar /> <FallHistory fallData={fallData} /> </> : <Navigate to="/login" />}
        />
        <Route
          path="*"
          element={<Navigate to={isAuthenticated ? "/main" : "/login"} />}
        />
      </Routes>
    </Router>
  );
}

export default App;
