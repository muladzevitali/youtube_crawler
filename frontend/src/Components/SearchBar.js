import React from 'react'
import {Button, Col, Form, Image, InputGroup} from 'react-bootstrap'
import '../Styles/SearchBar.css'


class SearchBar extends React.Component {
    constructor(props) {
        super(props);
        this.isNumber = /^[0-9\b]+$/;
        this.filterCommas = new RegExp(',', 'g');
        this.state = {
            showFilters: false,
            validated: null,
            errorMessage: 'null',
            ...props.state
        }
    }

    filterButtonHandler = () => {
        const showFilters = this.state.showFilters;
        this.setState({showFilters: !showFilters})
    };
    onChange = (event) => {
        this.setState({[event.target.name]: event.target.value})
    };
    onChangeNumber = (event) => {
        let value = event.target.value.replace(this.filterCommas, '');
        if (value === '' || this.isNumber.test(value)) {
            this.setState({[event.target.name]: value})

        }
    };

    isFormValid = data => {
        const {queryWord, minViews, maxViews} = {...data};
        if (!queryWord || !minViews || !maxViews) {
            this.setState({errorMessage: 'Please fill in the search word before proceed'});
            return false
        } else if (queryWord.length < 3) {
            this.setState({errorMessage: 'Please fill in the search word with more letters'});
            return false
        } else if (isNaN(minViews) || isNaN(maxViews) || minViews.indexOf('.') !== -1 || maxViews.indexOf('.') !== -1) {
            this.setState({errorMessage: 'Please check whether minimum or maximum views number are whole numbers'});
            return false
        } else if (parseInt(minViews) >= parseInt(maxViews)) {
            this.setState({errorMessage: 'Please check whether minimum number of views is smaller than maximum'});
            return false
        } else {
            return true
        }

    };
    onFormSubmit = event => {
        event.preventDefault();
        const data = {
            queryWord: event.target[1].value,
            minViews: event.target[3].value.replace(this.filterCommas, ''),
            maxViews: event.target[4].value.replace(this.filterCommas, '')
        };

        if (!this.isFormValid(data)) {
            event.stopPropagation();
            this.setState({validated: false});
            return
        }

        this.setState({validated: true});
        this.props.onSubmit(data)

    };

    render() {
        let searchButtonStyle = this.state.queryWord.length > 2 ? {filter: 'invert(0.6) brightness(2.0)'} : {filter: 'invert(0.3)'};

        return (
            <Form noValidate onSubmit={this.onFormSubmit}>
                <Form.Row>
                    <Form.Group as={Col}>
                        <InputGroup size="lg" className={this.state.validated === false && 'is-invalid'}>
                            <InputGroup.Prepend>
                                <Button variant='none' className='searchButton' type='submit'>
                                    <Image src={'/searchButton.png'} alt="searchButton"
                                           style={searchButtonStyle}/>
                                </Button>
                            </InputGroup.Prepend>
                            <Form.Control aria-label="Word"
                                          className='queryWord'
                                          name='queryWord'
                                          type="text"
                                          defaultValue={this.state.queryWord}
                                          onChange={this.onChange}
                                          placeholder='Search for a music genre'
                                          required
                            />

                            <InputGroup.Append>
                                <Button variant='none' className='filterButton'
                                        size='sm'
                                        onClick={this.filterButtonHandler}
                                        onAnimationEnd={this.filterButtonHandler}>
                                    <Image alt="filterButton"
                                           src='filterButtonGreen.png'
                                           style={!this.state.showFilters ? {filter: 'invert(0.5)'} : {}}/>
                                </Button>
                            </InputGroup.Append>
                        </InputGroup>
                        <Form.Control.Feedback type='invalid'>
                            {this.state.errorMessage}
                        </Form.Control.Feedback>
                    </Form.Group>
                </Form.Row>

                <Form.Row className='searchFilterRow'
                          style={{
                              display: this.state.showFilters || 'none',
                              left: this.props.header ? '35%' : '42%'
                          }}>
                    <Form.Group as={Col} controlId="minViews" md='4'>
                        <Form.Control aria-label='minViews'
                                      onChange={this.onChangeNumber}
                                      className='viewsCount'
                                      name='minViews'
                                      value={new Intl.NumberFormat().format(this.state.minViews)}
                                      placeholder='1000000'/>
                    </Form.Group>
                    <h5>to</h5>
                    <Form.Group as={Col} controlId="formGridZip" md='4'>
                        <Form.Control aria-label="maxViews"
                                      onChange={this.onChangeNumber}
                                      className='viewsCount'
                                      name='maxViews'
                                      value={new Intl.NumberFormat().format(this.state.maxViews)}
                                      placeholder='2000000'/>
                    </Form.Group>
                    <h5>views</h5>
                </Form.Row>

            </Form>
        )
    }

}

export default SearchBar