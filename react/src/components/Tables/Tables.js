import React, { useState } from 'react';

import './Tables.css';

function Table({ data, onRowSelect }) {
    const [selectedRow, setSelectedRow] = useState(null);
    const [sortField, setSortField] = useState(null);
    const [sortOrder, setSortOrder] = useState('asc'); // 'asc' or 'desc'
  
    const handleRowClick = (index, rowData) => {
      setSelectedRow(index);
      // console.log('Row clicked:', rowData);
      if (onRowSelect) onRowSelect(rowData);
    };

    const handleSort = (field) => {
      if (sortField === field) {
          setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
      } else {
          setSortField(field);
          setSortOrder('asc');
      }
    };

    const sortedData = [...data].sort((a, b) => {
        if (!sortField) return 0;

        if (a[sortField] < b[sortField]) return sortOrder === 'asc' ? -1 : 1;
        if (a[sortField] > b[sortField]) return sortOrder === 'asc' ? 1 : -1;
        return 0;
    });

    function formatShortDate(isoString) {
        const date = new Date(isoString);
        
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');  // Months are 0-based, so +1
        const day = String(date.getDate()).padStart(2, '0');
        const hour = String(date.getHours()).padStart(2, '0');
        const minute = String(date.getMinutes()).padStart(2, '0');
        
        return `${year}-${month}-${day} ${hour}:${minute}`;
    }
  
    return (
      <table>
        <thead>
          <tr>
              <th onClick={() => handleSort('username')}>Username</th>
              <th onClick={() => handleSort('title')}>Title</th>
              <th onClick={() => handleSort('description')}>Description</th>
              <th onClick={() => handleSort('price')}>Price</th>
              <th onClick={() => handleSort('categories')}>Category</th>
              <th onClick={() => handleSort('created_at')}>Created</th>
          </tr>
        </thead>
        <tbody>
          {sortedData.map((row, index) => (
            <tr
              key={index}
              onClick={() => handleRowClick(index, row)}
              className={selectedRow === index ? 'selected' : ''}
            >
                <td>{row.username}</td>
                <td>{row.title}</td>
                <td id='description_cell'>{row.description}</td>
                <td>{row.price}</td>
                <td>{row.categories ? row.categories.join(', ') : 'N/A'}</td>
                <td>{formatShortDate(row.created_at) || 'N/A'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    );
}

export default Table;
