import React from 'react'
import {Spinner} from 'react-bootstrap'
import '../Styles/PageLoader.css'

class PageLoader extends React.Component {
    render() {
        return (
            <div>
            <div className='pageLoader'>
                <Spinner animation='border' variant='success'/>
                <p className='pageLoaderText'>Your request is loading</p>
            </div>
            </div>
        )
    }
}


export default PageLoader