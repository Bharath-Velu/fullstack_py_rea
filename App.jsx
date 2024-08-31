// src/App.jsx
import React from 'react';
import ContactList from './contactList.jsx';
import CreateContact from './CreateContact.jsx';

function App() {
  return (
    <div className="App">
      <h1>Contact Management</h1>
      <CreateContact />
      <ContactList />
    </div>
  );
}

export default App;
