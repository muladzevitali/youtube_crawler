import React from 'react'
import axios from 'axios'
import {crawlerUrl} from "../Config";
import {Card, Table, Image, Form, Toast} from 'react-bootstrap'
import '../Styles/ResultsTable.css'
import abbreviateNumber from '../Utils/abbreviateNumber'


class ResultsTable extends React.Component {
    constructor(props) {
        super(props);
        const modifiedData = this.props.data.map(item => {
            item['artistNameInputDisabled'] = true;
            item['artistNameToastShow'] = false;
            return item
        });
        this.state = {data: modifiedData}
    }

    getItemWithYoutubeId = youtubeId => {
        const currentData = this.state.data;
        let item = currentData.find(item => item['youtube_id'] === youtubeId);
        const itemIndex = currentData.indexOf(item);
        return {'item': item, 'itemIndex': itemIndex}
    };
    onDoubleClickArtistName = youtubeId => event => {
        const currentData = this.state.data;
        let {item, itemIndex} = {...this.getItemWithYoutubeId(youtubeId)};
        item['artistNameInputDisabled'] = !item['artistNameInputDisabled'];
        if (event === 'submitted') {
            item['artistNameToastShow'] = true;
        }
        currentData[itemIndex] = item;
        this.setState({data: currentData});

    };
    onChangeArtistName = youtubeId => event => {
        const currentData = this.state.data;
        let {item, itemIndex} = {...this.getItemWithYoutubeId(youtubeId)};
        item['artist_name'] = event.target.value;
        currentData[itemIndex] = item;
        this.setState({data: currentData});
    };
    onArtistNameFormSubmit = youtubeId => event => {
        event.preventDefault();
        const data = {'youtube_id': youtubeId, 'artist_name': event.target[0].value};
        axios.post(crawlerUrl, data)
            .then(response => {
                let {itemIndex} = {...this.getItemWithYoutubeId(youtubeId)};
                let currentData = this.state.data;
                currentData[itemIndex] = response.data['data'];
                this.setState({data: currentData});
                this.onDoubleClickArtistName(youtubeId)('submitted');
            })
            .catch(error => console.log(error));

    };
    onCloseToast = youtubeId => event => {
        const currentData = this.state.data;
        let {item, itemIndex} = {...this.getItemWithYoutubeId(youtubeId)};
        item['artistNameToastShow'] = false;
        currentData[itemIndex] = item;
        this.setState({data: currentData});

    };
    getToasts = _ => {
        const changedArtistNameItems = this.state.data.filter(item => item['artistNameToastShow'] === true);
        return changedArtistNameItems.map((item, index) => {
            return (
                <Toast onClose={this.onCloseToast(item['youtube_id'])}
                       show={item['artistNameToastShow']}
                       delay={3000}
                       autohide
                       className='artistNameChangeToast'
                       key={index}>
                    <Toast.Header>
                        <strong className="mr-auto">Success</strong>
                    </Toast.Header>
                    <Toast.Body>Name Changed to {item['artist_name']}</Toast.Body>
                </Toast>)
        })
    };

    render() {
        return (
            <div>
                <div aria-live="polite" aria-atomic="true" style={{position: 'relative'}}>
                    <div style={{position: 'absolute', top: '-10rem', right: '-25rem'}}>
                        {this.getToasts()}
                    </div>
                </div>
                <Card className="resultsCard">

                    <Card.Body>
                        <Table striped responsive='md' variant="dark" className='resultsTable'>
                            <thead>
                            <tr>
                                <th>Video Title</th>
                                <th style={{width: '10%'}}>Views #</th>
                                <th style={{width: '10%'}} className='tableItemToLeft'>Artist Name</th>
                                <th/>
                            </tr>
                            </thead>
                            <tbody>
                            {this.state.data.map((item, index) => {
                                return (

                                    <tr key={index}>
                                        <td className='tableItemToLeft'>
                                            <a href={item['url']} target='_blank' rel="noopener noreferrer">
                                                {item['title']}
                                            </a>
                                        </td>
                                        <td>{abbreviateNumber(item['views'])}</td>
                                        <td className='tableItemToLeft' onDoubleClick={this.onDoubleClickArtistName(item['youtube_id'])}>
                                            <Form onSubmit={this.onArtistNameFormSubmit(item['youtube_id'])}>
                                                <div className='artistNameDiv'>
                                                    {item['artistNameInputDisabled'] ?
                                                        (item['artist_name'] || (<p>  </p>)) :
                                                        (
                                                            <Form.Control aria-label="Word"
                                                                          className='artistNameInput'
                                                                          name='artistName'
                                                                          type="text"
                                                                          autoFocus
                                                                          value={item['artist_name'] || ''}
                                                                          readOnly={item['artistNameInputDisabled']}
                                                                          onChange={this.onChangeArtistName(item['youtube_id'])}
                                                            />
                                                        )}
                                                </div>

                                            </Form>
                                        </td>
                                        <td className='spotifyFollowers'>
                                            {item['total_followers'] ? (
                                                <div><Image src={'/spotifyIcon.png'} className='spotifyIcon'/>
                                                    <span>{abbreviateNumber(item['total_followers'])}</span></div>
                                            ) : (<div/>)}

                                        </td>
                                    </tr>
                                )
                            })}

                            </tbody>
                        </Table>
                    </Card.Body>

                </Card>
            </div>
        );
    }
}

export default ResultsTable;