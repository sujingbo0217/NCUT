import './App.css'
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';

import Login from "./pages/users/Login.tsx";
import Register from "./pages/users/Register.tsx";
import Home from "./pages/images/Home.tsx";
import Predict from "./pages/images/Predict.tsx";
import Gallery from "./pages/images/Gallery";

function App() {
  return (
      <Router>
        <Routes>
          <Route path="/" element={<Login/>}/>
          <Route path="/register" element={<Register/>}/>
          <Route path="/home" element={<Home/>}/>
          <Route path="/upload" element={<Predict/>}/>
          <Route path="/gallery" element={<Gallery/>}/>
        </Routes>
      </Router>
  );
}

export default App
