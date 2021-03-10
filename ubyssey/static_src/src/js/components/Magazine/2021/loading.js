import React, { Component } from 'react'




export default class loading extends Component {
    render() {
        return (
            <div className="loading_container">

                <h1 style={{ color: 'white' }} className="fade-in-title"> THE UBYSSEY MAGAZINE </h1>

                <div className="loader">
                    <div className="loading_1"></div>
                </div>

                <div className="video_wrapper">

                    <video className='video' autoPlay loop muted>
                        <source src={'https://storage.googleapis.com/ubyssey/images/Cover_home_2.mp4'} type='video/mp4' />
                    </video>

                </div>

            </div>
        )
    }
}