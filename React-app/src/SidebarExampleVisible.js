import React from 'react';
import { Icon, Menu, Sidebar } from 'semantic-ui-react';

const SidebarExampleVisible = ({ activeItem, onItemSelect, onDirectAction, isLoggedIn, onLogout }) => {
  return (
    <Sidebar
      as={Menu}
      animation="overlay"
      icon="labeled"
      inverted
      vertical
      visible={true}
      width="thin"
      style={{ display: 'flex', flexDirection: 'column', height: '100%' }}
    >
      <Menu.Item as='a' active={activeItem === 'search'} onClick={() => onItemSelect('search')}>
        <Icon name='search' />
        Search
      </Menu.Item>
      <Menu.Item as='a' active={activeItem === 'recommendations'} onClick={() => onItemSelect('recommendations')}>
        <Icon name='map outline' />
        Recommendations
      </Menu.Item>
      {}
      <div style={{ flexGrow: 1 }}></div>
      {}
      {isLoggedIn ? (
        <Menu.Item as='a' onClick={onLogout}>
          <Icon name='log out' />
          Logout
        </Menu.Item>
      ) : (
        <Menu.Item as='a' onClick={() => onDirectAction('login')}>
          <Icon name='user' />
          Login
        </Menu.Item>
      )}
    </Sidebar>
  );
};

export default SidebarExampleVisible;
