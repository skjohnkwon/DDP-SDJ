import React from 'react';
import './Search.css';
import { useState, useEffect } from 'react';
import axios from 'axios';
import CreateComment from '../CreateComment/CreateComment';
import Table from '../Tables/Tables';

const Search = () => {

    const [entry, setEntry] = useState('');
    const [data, setData] = useState([]);
    const [selectedRow, setSelectedRow] = useState(null);

    const search = async () => {

        
        try {
            const response = await axios.get('http://127.0.0.1:8000/search/', {
                params: { entry: entry },
            });

            if (response.status === 200) {
                console.log('Database initialized!');
                console.log(response.data);
                setData(response.data);
                
            }
        } catch (error) {
            console.log('Error during database initialization!', error);
        }
    }

    const init_db = async () => {

        console.log('Initializing database...');
        try {
            const response = await axios.post('http://127.0.0.1:8000/init-db/');

            if (response.status === 201) {
                
                console.log(response.data);
                
            }

        } catch (error) {
            
            console.log('Error during database initialization!', error);
        }
    }

    const handleTableRowSelect = (selectedData) => {

        setSelectedRow(selectedData);
    };

    useEffect(() => {
        console.log('Updated selected row:', selectedRow);
    }, [selectedRow]);

    return (
        <div className='search'>
    
            <div className='left-div'>
    
                <div className="input-div">
    
                    <input
                        className='input-field'
                        type="text"
                        placeholder="Search for a category"
                        onChange={e => setEntry(e.target.value)}
                    />

                    <button className='search-bttn' onClick={search}>Search</button>
    
                </div>
    
                <div className="result-window">
                    <Table data={data} onRowSelect={handleTableRowSelect}/>
                </div>
                    
                <div className='button-div'>
                    <button className='init-db-bttn' onClick={init_db}>Initialize Database</button>
                </div>
    
            </div>
    
            <div className='right-div'>
                <CreateComment 
                    username={selectedRow ? selectedRow.username : null}
                    item={selectedRow ? selectedRow.title : null}
                    item_id={selectedRow ? selectedRow.id : null}
                />
            </div>
    
        </div>
    )
}

export default Search;
