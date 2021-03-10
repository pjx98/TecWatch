import React from 'react';
import './Button.css';
import { Link } from 'react-router-dom';

const STYLES = ['btn--primary','btn--outline']; //full background vs outlined version

const SIZES = ['btn--medium','btn--large'];

export const Button = ({children, type, onClick, buttonStyle, buttonSize}) => {
    const checkButtonStyle = STYLES.includes(buttonStyle) 
    ? buttonStyle : STYLES[0];

    const checkButtonSize = SIZES.includes(buttonSize) ? buttonSize :SIZES[0]

    return(
<<<<<<< HEAD
        <Link to='login/' className='btn-mobile'>
=======
        <Link to='/log-out' className='btn-mobile'>
>>>>>>> fafc9891cfad13827301349b2c59fc512a39176f
            <button
            className={'btn ${checkButtonStyle} ${checkButtonSize}'}
            onClick={onClick}
            type={type}
            >
                {children}
            </button>
        </Link>
    )
};

class button extends React.Component {
    state = {
        title = "",
        date_created = "",
        score = 0,
        picture = null,
        deadline = "",
        suggestions = "",
        notes = "",
        
        
    };

    componentDidMount() {
        if (this.props.complaint) {
            const {title, date_created, score, picture, deadline, suggestions, notes} = this.props.complaint;
            this.setState({title, date_created, score, picture, deadline, suggestions, notes});
        }
    }

    onChange = e => {
        this.setState({e.target.name: e.target.value});
    }
    
    createComplaint = e=> {
        e.preventDefault();
        axios.post(API_URL, this.state).then(() => {
            this.props.resetState();
            this.props.toggle():
        })
    }
}