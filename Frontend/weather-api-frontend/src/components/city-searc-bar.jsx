import React, { useState } from 'react';

const SearchBar = ({ onSearch }) => {
  // State to track the search input
  const [query, setQuery] = useState('');

  // Handle input change
  const handleInputChange = (event) => {
    setQuery(event.target.value);
    onSearch(event.target.value);  // Call the onSearch callback (optional)
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Keress rá egy városra..."
        value={query}
        onChange={handleInputChange}
        style={{
          padding: '8px',
          width: '300px',
          border: '1px solid #ccc',
          borderRadius: '4px',
        }}
      />
    </div>
  );
};

export default SearchBar;
