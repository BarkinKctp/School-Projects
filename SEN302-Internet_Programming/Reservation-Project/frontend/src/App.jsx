import './css/App.css'
import {NavBar} from './components/NavBar'
import { Routes, Route } from 'react-router-dom'
import {Home} from './pages/Home'
import DataPage from './pages/DataPage'


function App() {  
  return (
    <>
      <NavBar />
      <main className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/Data" element={<DataPage />} />
        </Routes>
      </main>
    </>
  );
}

export default App
