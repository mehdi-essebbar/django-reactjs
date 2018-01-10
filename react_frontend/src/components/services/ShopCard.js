import React, { Component } from "react";
import PropTypes from "prop-types";
import { connect } from "react-redux";
import { Link } from "react-router-dom";
import { likeShop } from "../../actions/serviceActions";


class ShopCard extends Component {
    constructor(props){
        super(props)
        this.state = { disableLikeButton: "" };
    }
    
    static propTypes = {
        likeShop: PropTypes.func.isRequired,
        liked: PropTypes.bool
    };
    
    dislikeFunc(shop_id)
    {
        this.props.removeShopCard(shop_id, this.props.key);
    }
    
    likeFunc(shop_id)
    {
        // Send request with axios to like the shop
        this.props.likeShop(shop_id);
    }
    
    componentWillReceiveProps(nextProps)
    {
        if(nextProps.liked)
            this.setState({...this.state, disableLikeButton:" disabled"});            
    }
    
    renderLikeButton(is_favorite, id)
    {
        if(is_favorite>0)
            return (<button className="btn btn-primary disabled">Like</button>);
        return (<button className={"btn btn-primary"+this.state.disableLikeButton} onClick={()=> this.likeFunc(id)}>Like</button>);
    }
    render()
    {
        const shop = this.props.value;
        return (
            <div className="card">
                <img className="card-img-top" src={shop.picture} alt="Card image cap"></img>
                <div className="card-block">
                    <h4>Name: {shop.name}</h4>
                    <h4>Email: {shop.email}</h4>
                    <h4>City: {shop.city}</h4>                        
                    {" "}
                    <hr />
                    <button className="btn btn-primary mr-2"  onClick={() => this.dislikeFunc(shop.id)}>Dislike</button>
                    {this.renderLikeButton(shop.is_favorite, shop.id)}
                </div>
            </div>
        );
    }
}

function mapStateToProps(state) {
    return {
    liked: state.service.liked
    };
}

export default connect(mapStateToProps, { likeShop } )(ShopCard);