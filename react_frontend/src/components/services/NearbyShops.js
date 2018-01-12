import React, { Component } from "react";
import PropTypes from "prop-types";
import { connect } from "react-redux";
import { Link } from "react-router-dom";
import { getShops, dislikeShop } from "../../actions/serviceActions";
import ShopCard from "./ShopCard";

class NearbyShops extends Component {

    constructor(props){
        super(props)
        this.state={
            dislikeThisShop: Array(1).fill(true)
        };
    }
    
    static propTypes = {
        getShops: PropTypes.func.isRequired,
        shops: PropTypes.array,
        userLocation: PropTypes.object,
    };

    componentWillMount() {
        if (this.props.isFavoriteList)
            this.props.getShops(true);
        else
            this.props.getShops(false);
    }
    
    componentWillReceiveProps(nextProps){
        // the first time receiving props
        if(!this.props.userLocation && nextProps.userLocation)
            this.props.getShops(this.props.isFavoriteList)
        
        if (nextProps.userLocation && this.props.userLocation
        && nextProps.userLocation.lat !== this.props.userLocation.lat 
        && nextProps.userLocation.lng !== this.props.userLocation.lng) 
        {
            console.log(nextProps.userLocation)
            this.props.getShops(this.props.isFavoriteList)
        }
    }
    
    renderShops() {
        const shops = this.props.shops;
        
        if (shops) {
            
            const listItems = shops.map( (shop) => <ShopCard key={shop.id} value={shop} isFavoriteList={this.props.isFavoriteList} /> )
            
            return listItems;
        }
        return null;
    }

    render() {
        return (
        
            <div>
            {this.renderShops()}
            </div>
        );
    }
}

function mapStateToProps(state) {
    
    return {
        shops: state.service.shops,
        userLocation: state.service.userLocation
    };
}

export default connect(mapStateToProps, { getShops } )(NearbyShops);