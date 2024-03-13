import React, { useState } from 'react';
import SidebarExampleVisible from './SidebarExampleVisible';
import MapComponent from './MapComponent';
import SearchContent from './SearchContent';
import RecommendationsContent from './RecommendationsContent';
import LoginPopup from './LoginPopup';
import 'semantic-ui-css/semantic.min.css';

function App() {
  const [activeItem, setActiveItem] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [center, setCenter] = useState([39.50, -98.35]);
  const [zoom, setZoom] = useState(5);
  const [isLoggedIn, setIsLoggedIn] = useState(false); 
  const [showLoginPopup, setShowLoginPopup] = useState(false); 

  const handleLogin = async (userId) => {
    try {
      const response = await fetch('http://localhost:5000/api/validate_user_id', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_id: userId }),
      });
  
      const data = await response.json();
      if (data.valid) {
        setIsLoggedIn(true);
        setShowLoginPopup(false); 
        return true; 
      } else {
        return false;
      }
    } catch (error) {
      console.error('Error during login:', error);
      return false; 
    }
  };
  const handleLoginSuccess = () => {
    setIsLoggedIn(true); 
    setShowLoginPopup(false);
  };

  const handleLogout = () => {
    setIsLoggedIn(false); 
  };

  const handleItemSelect = (itemName) => {
    setActiveItem(itemName === activeItem ? '' : itemName);
  };
  
  const selectLocation = (latitude, longitude) => {
    setCenter([latitude, longitude]);
    setZoom(10); 
  };
  const handleDirectAction = (actionType) => {
    if (actionType === 'login') {
      setShowLoginPopup(true); 
    }
  };
  return (
    <div className="App" style={{ display: 'flex', height: '100vh' }}>
      <div style={{ width: '150px' }}>
      <SidebarExampleVisible
        activeItem={activeItem}
        onItemSelect={handleItemSelect}
        onDirectAction={handleDirectAction} 
        isLoggedIn={isLoggedIn}
        onLogout={handleLogout}
      />
      </div>
      <div style={{ display: 'flex', flexGrow: 1 }}>
        {activeItem === 'search' && (
          <SearchContent 
            setSearchResults={setSearchResults} 
            setSearchCenter={setCenter} 
            selectLocation={selectLocation} />
        )}
        {activeItem === 'recommendations' && (<RecommendationsContent
            setSearchResults={setSearchResults} 
            setSearchCenter={setCenter} 
            selectLocation={selectLocation} />)
        }
        <MapComponent searchResults={searchResults} center={center} zoom={zoom} />
        <LoginPopup isOpen={showLoginPopup} onClose={() => setShowLoginPopup(false)} onLogin={handleLogin} />
      </div>
    </div>
  );
}


export default App;
