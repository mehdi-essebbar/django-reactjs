import React, { Component } from "react";
import PropTypes from "prop-types";
import { connect } from "react-redux";
import {Popover, Tooltip, Modal, Button, OverlayTrigger} from "react-bootstrap";
import { withScriptjs, withGoogleMap, GoogleMap, Marker } from "react-google-maps";
import { withState, withHandlers, compose, withProps } from "recompose";
//import  from "react-bootstrap";

class CaptureUserLocation extends Component {
    constructor(...args) {
		super(...args);

		this.handleShow = this.handleShow.bind(this);
		this.handleClose = this.handleClose.bind(this);

		this.state = { showModal: false, currentLocation:{ lat: 34.016425960458186, lng: -6.835730738195826 } };
	}
 
	handleClose() {
		this.setState({ showModal: false });
	}

	handleShow() {
		this.setState({ showModal: true });
	}
    
    handleCurrentPosition() {
        // recenter the map on the user's current position
        if (navigator && navigator.geolocation) {
            navigator.geolocation.getCurrentPosition((pos) => {
                const coords = pos.coords;
                console.log(coords);
                document.getElementById('lat').value = coords.latitude;
                document.getElementById('lng').value = coords.longitude;
                this.setState({
                    currentLocation: {
                        lat: coords.latitude,
                        lng: coords.longitude
                    }
                })
            })
        }
    }
    
    handleSave(){
        // This function should save the user location choice
        // in the state as 'location'
        //let mpDiv = map.getDiv();
        //document.getElementById('map').appendChild(mpDiv);
        
    }
    positionChanged(newPos){
        this.setState({position: newPos})
    }
    
	render() {
        
        const MyMapComponent = compose(
              withProps({
                googleMapURL: "https://maps.googleapis.com/maps/api/js?key=AIzaSyAnZVU-6BxMYhnhySbu2BIqJXKlBGDrZ-U&v=3.exp&libraries=geometry,drawing,places",
                loadingElement: <div style={{ height: `100%` }} />,
                containerElement: <div style={{ height: `400px` }} />,
                mapElement: <div style={{ height: `100%` }} />,
              }),
              withState('editedCenter', 'onCenterChange', this.state.currentLocation),
              withHandlers(() => {
                const refs = {
                  map: undefined,
                }

                return {
                  onMapMounted: () => ref => {
                    refs.map = ref
                  },
                  onCenterChanged: ({ onCenterChange }) => () => {
                    
                    let pos = refs.map.getCenter()
                    document.getElementById('lat').value = pos.lat()
                    document.getElementById('lng').value = pos.lng()
                    onCenterChange({lat:pos.lat(), lng:pos.lng()})
                  }
                }
              }),
              withScriptjs,
              withGoogleMap,
            )((props) =>
              <GoogleMap
                defaultZoom={8}
                defaultCenter={{ lat:props.currentLocation.lat, lng: props.currentLocation.lng }}
                zoom={props.zoom}
                editedCenter={props.editedCenter}
                center={props.currentLocation}
                ref={props.onMapMounted}
                onZoomChanged={props.onZoomChanged}
                onCenterChanged={props.onCenterChanged}
              >
                {props.isMarkerShown && <Marker position={{ lat: props.editedCenter.lat, lng: props.editedCenter.lng }} />}
              </GoogleMap>
            )
        
		return (
			<div>
				<p>Click to get the full Modal experience!</p>

				<Button bsStyle="primary" bsSize="small" onClick={this.handleShow}>
					Launch demo modal
				</Button>

				<Modal show={this.state.showModal} onHide={this.handleClose}>
					<Modal.Header closeButton>
						<Modal.Title>Modal heading</Modal.Title>
					</Modal.Header>
					<Modal.Body>
						<p> Hey, this is your test for Modals with react-bootsrap module!</p>
                        <MyMapComponent currentLocation={this.state.currentLocation} isMarkerShown positionChanged={(newPos)=> this.positionChanged(newPos)}/>
                    </Modal.Body>
                    <Modal.Footer>
                        <input type="text" id="lat" readonly="yes" />
                        <input type="text" id="lng" readonly="yes" />
                        <Button onClick={() => this.handleCurrentPosition()}>Current Position</Button>
                        <Button onClick={this.handleSave}>Save</Button>
                        <Button onClick={this.handleClose}>Close</Button>
                    </Modal.Footer>
                </Modal>
            </div>);
    }
    
    //render(){ return <span> bzzz</span>; }
}

export default CaptureUserLocation;