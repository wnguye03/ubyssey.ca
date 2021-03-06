import React, { Component } from 'react'

export default class memoryLeak extends Component {
    render() {
        return (
            <div>

                <div className="wrapper">

                    <div className="grid_container fade-in">

                        <h1 style={{ color: 'white' }}>{this.props.title}</h1>

                        <div className="article_1 nested one">

                            <div>
                                {/* <img className="photo_vertical" src={Dog} /> */}

                            </div>
                            <div> </div>
                            <div className="card__overlay"> <span>Read More</span> </div>
                        </div>

                        <div className="article_2 nested two">


                            <div className="img__wrap">
                                {/* <img className="photo_vertical" src={Dog} /> */}

                            </div>


                            <div> </div>
                            <div className="card__overlay"> <span>Read More</span> </div>

                        </div>

                        <div className="article_3 nested three">
                            <div>
                                {/* <img className="photo_vertical" src={Dog} /> */}

                            </div>


                            <div> </div>
                            <div className="card__overlay"> <span>Read More</span> </div>


                        </div>

                        <div className="article_4 nested four">


                            <div>
                                {/* <img className="photo_vertical" src={Dog} /> */}

                            </div>


                            <div> </div>
                            <div className="card__overlay"> <span>Read More</span> </div>
                        </div>

                        <div className="article_5 nested five">


                            <div>
                                {/* <img className="photo_vertical" src={Dog} /> */}

                            </div>


                            <div> </div>

                            <div className="card__overlay"> <span>Read More</span> </div>

                        </div>

                        <div className="article_6 nested six">


                            <div>
                                {/* <img className="photo_vertical" src={Dog} /> */}

                            </div>


                            <div> </div>
                            <div className="card__overlay"> <span>Read More</span> </div>


                        </div>



                    </div>
                </div>


            </div>
        )
    }
}
