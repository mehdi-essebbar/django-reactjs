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
        dislikeShop: PropTypes.func.isRequired,
        disliked: PropTypes.number
    };

    componentWillMount() {
        this.props.getShop();
    }
    
    componentWillReceiveProps(nextProps){
        if(nextProps.shops)
            this.setState({...this.state, dislikeThisShop:Array(nextProps.shops.length).fill(true)});
        
        console.log(nextProps);
        
        if(nextProps.disliked)
        {
            const arr = this.state.dislikeThisShop.slice();
            arr[nextProps.disliked] = false;
            this.setState({...this.state, dislikeThisShop:arr});
            console.log("hi");
        }
    }

    handleDislike(shop_id, i)
    {
        this.props.dislikeShop(shop_id, i);
    }
    
    renderShop(shop, i)
    {
        if (this.state.dislikeThisShop[i])
            return (<ShopCard key={i} value={shop} removeShopCard={(id, k) => this.handleDislike(id, k)}/>);
        
        return null;
    }
    
    renderShops() {
        const shops = this.props.shops;
        
        if (shops) {
            const rows = [];
            for(var i=0; i<shops.length; i++)
                rows.push(this.renderShop(shops[i], i));
            
            return rows;
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
    if(state.service.disliked){
        console.log("hello");
        return {
        disliked: state.service.disliked
        };
    }
    
    return {
        shops: state.service.shops
    };
}

export default connect(mapStateToProps, { getShop, dislikeShop } )(NearbyShops);