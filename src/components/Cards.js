import React from 'react';
import CardItem from './CardItem';
import './Cards.css';

function Cards() {
    return (
        <div className='cards'>
            <h1>See all the functions on TecWatch for Staff</h1>
                <div className="cards__container">
                    <div className="cards__wrapper">    
                        <ul className="cards__items">
                            <CardItem 
                            src="images/starbucks_front.jpg"
                            text="View All Tenants"
                            label='Sorted by: Shops'
                            path='/view-all-tenants'
                            />
                            <CardItem 
                            src="images/unresolvedreports.png"
                            text="View All Reports"
                            label='Sorted by: Latest'
                            path='/view-all-reports'
                            />
                    </ul>

                    <ul className="cards__items">
                            <CardItem 
                            src="images/audit.jpg"
                            text="Create New Audit Report"
                            label='Audit Form'
                            path='/create-report'
                            />
                            <CardItem 
                            src="images/reports.png"
                            text="View Unresolved Rectifications"
                            label='Sorted by: Latest'
                            path='/view-unresolved-reports'
                            />
                    </ul>

                </div>
            </div>
        </div>
    );
}

export default Cards;
