import React, { useState } from 'react';
import { Button, Modal, Input, Message } from 'semantic-ui-react'; 

const LoginPopup = ({ isOpen, onClose, onLogin }) => {
  const [userId, setUserId] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const handleLoginClick = async () => {
    const success = await onLogin(userId); 
    if (!success) {
      setErrorMessage('Login unsuccessful. Please try again.');
    }
  };

  return (
    <Modal open={isOpen} onClose={onClose} size="tiny">
      <Modal.Header>Login</Modal.Header>
      <Modal.Content>
        {errorMessage && <Message negative>{errorMessage}</Message>} {}
        <p>Enter your user ID:</p>
        <Input fluid value={userId} onChange={(e) => setUserId(e.target.value)} autoFocus />
      </Modal.Content>
      <Modal.Actions>
        <Button onClick={onClose}>Cancel</Button>
        <Button positive onClick={handleLoginClick}>Confirm</Button>
      </Modal.Actions>
    </Modal>
  );
};

export default LoginPopup;
