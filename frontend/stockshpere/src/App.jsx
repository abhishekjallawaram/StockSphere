import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import React from 'react'; // No need to import useState and useEffect here anymore
import './App.css';
import Login from './pages/Login';
import Register from "./pages/Register";
import PrivateRoute from "./utils/PrivateRoute";
import Dashboad from './pages/Dashboad';



function App() {
  // The token state is no longer necessary here since the validation is handled within PrivateRoute

  return (
    <div className=""> {/* Use the container class */}
      <Router className="">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={
            <PrivateRoute>
              <Dashboad/>
            </PrivateRoute>
          } />
        </Routes>
      </Router>
     </div>
  );
}

export default App;
