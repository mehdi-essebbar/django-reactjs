import React, { Component } from "react";
import PropTypes from "prop-types";
import { connect } from "react-redux";
import { Link } from "react-router-dom";
import { getShop, dislikeShop } from "../../actions/serviceActions";
import ShopCard from "./ShopCard";

class NearbyShops extends Component {

    constructor(props){
        super(props)
        this.state={...this.state,
            dislikeThisShop: Array(1).fill(true)
        };
        this.handleDislike = this.handleDislike.bind(this);
    }
    
    static propTypes = {
        getShop: PropTypes.func.isRequired,
        shops: PropTypes.array,
        
    };

    componentWillMount() {
        this.props.getShop();
    }
    
    componentWillReceiveProps(nextProps){
        if(nextProps.shops)
            this.setState({...this.state, dislikeThisShop:Array(nextProps.shops.length).fill(true)});
        
    }

    handleDislike(shop_id)
    {
        //this.props.dislikeShop(shop_id, i);
    }
    /*
    renderShop(shop, i)
    {
        if (this.state.dislikeThisShop[i])
            return (<ShopCard key={i} value={shop} removeShopCard={(id, k) => this.handleDislike(id, k)}/>);
        
        return null;
    }
    */
    renderShops() {
        const shops = this.props.shops;
        
        if (shops) {
            
            const listItems = shops.map( (shop) => <ShopCard key={shop.id} value={shop} /> )
            
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
        shops: state.service.shops
    };
}

export default connect(mapStateToProps, { getShop } )(NearbyShops);