// src/components/UpdateContact.jsx
import React, { useState, useEffect } from 'react';

const UpdateContact = ({ contact, onUpdate }) => {
  const [formData, setFormData] = useState({
    firstName: contact.first_name,
    lastName: contact.last_name,
    email: contact.email,
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch(`http://localhost:5000/update_contact/${contact.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const result = await response.json();
      if (response.ok) {
        alert(result.message);
        onUpdate(); // Callback to refresh the contact list
      } else {
        alert(result.message);
      }
    } catch (error) {
      console.error('Error updating contact:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        name="firstName"
        value={formData.firstName}
        onChange={handleChange}
        placeholder="First Name"
        required
      />
      <input
        type="text"
        name="lastName"
        value={formData.lastName}
        onChange={handleChange}
        placeholder="Last Name"
        required
      />
      <input
        type="email"
        name="email"
        value={formData.email}
        onChange={handleChange}
        placeholder="Email"
        required
      />
      <button type="submit">Update Contact</button>
    </form>
  );
};

export default UpdateContact;
