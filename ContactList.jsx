// src/components/ContactList.jsx
import React, { useEffect, useState } from 'react';
import UpdateContact from './UpdateContact';

const ContactList = () => {
  const [contacts, setContacts] = useState([]);
  const [selectedContact, setSelectedContact] = useState(null);

  useEffect(() => {
    fetchContacts();
  }, []);

  const fetchContacts = async () => {
    try {
      const response = await fetch('http://localhost:5000/contacts');
      const data = await response.json();
      setContacts(data.Contacts);
    } catch (error) {
      console.error('Error fetching contacts:', error);
    }
  };

  const handleUpdateClick = (contact) => {
    setSelectedContact(contact);
  };

  const handleUpdate = () => {
    fetchContacts();
    setSelectedContact(null);
  };

  return (
    <div>
      <h2>Contact List</h2>
      <ul>
        {contacts.map((contact) => (
          <li key={contact.id}>
            {contact.first_name} {contact.last_name} - {contact.email}
            <button onClick={() => handleUpdateClick(contact)}>Update</button>
            <button onClick={() => handleDelete(contact.id)}>Delete</button>
          </li>
        ))}
      </ul>
      {selectedContact && (
        <UpdateContact contact={selectedContact} onUpdate={handleUpdate} />
      )}
    </div>
  );
};

// src/components/ContactList.jsx (continued)

const handleDelete = async (contactId) => {
    const confirmDelete = window.confirm('Are you sure you want to delete this contact?');
  
    if (!confirmDelete) return;
  
    try {
      const response = await fetch(`http://localhost:5000/delete_contact/${contactId}`, {
        method: 'DELETE',
      });
  
      const result = await response.json();
      if (response.ok) {
        alert(result.message);
        fetchContacts(); // Refresh the contact list after deletion
      } else {
        alert(result.message);
      }
    } catch (error) {
      console.error('Error deleting contact:', error);
    }
  };
  

export default ContactList;
