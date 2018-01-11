import React, { Component } from "react";
import PropTypes from "prop-types";
import { connect } from "react-redux";
import { Link } from "react-router-dom";
import { getShops, dislikeShop } from "../../actions/serviceActions";
import ShopCard from "./ShopCard";
import CaptureUserLocation from "./CaptureUserLocation";


class NearbyShops extends Component {

    constructor(props){
        super(props)
        this.state={...this.state,
            dislikeThisShop: Array(1).fill(true)
        };
    }
    
    static propTypes = {
        getShops: PropTypes.func.isRequired,
        shops: PropTypes.array,
    };

    componentWillMount() {
        if (this.props.isFavoriteList)
            this.props.getShops(true);
        else
            this.props.getShops(false);
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
            <CaptureUserLocation />
            {this.renderShops()}
            </div>
        );
    }
}

function mapStateToProps(state) {
    
    return {
        shops: state.service.shops
    };
}

export default connect(mapStateToProps, { getShops } )(NearbyShops);