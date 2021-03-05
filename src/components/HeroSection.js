import React from 'react';
import '../App.css';
import { Button } from './Button';
import './HeroSection.css';

function HeroSection() {
    return (
        <div className='hero-container'>
            {/*
            <video src='/videos/video-2.mp4' autoPlay loop muted/>*/}
            <h1>WELCOME, STAFFNAME!</h1>
            
            <div className="hero-btns">
                <Button 
                    className='btns' 
                    buttonStyle='btn--outline'
                    buttonSize='btn--large'
                >
                    VIEW LIST OF ALL TENANTS
                </Button>
                &nbsp;
                <Button
                    className='btns'
                    buttonStyle='btn--outline'
                    buttonSize='btn--large'
                    >
                        VIEW ALL COMPLIANCE REPORTS
                </Button>
            </div>
        </div>
    )
}
export default HeroSection
