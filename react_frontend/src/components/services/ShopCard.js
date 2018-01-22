import React, { Component } from "react";
import PropTypes from "prop-types";
import { connect } from "react-redux";
import { Link } from "react-router-dom";
import { likeShop, dislikeShop } from "../../actions/serviceActions";
import {Thumbnail, Button} from "react-bootstrap";


class ShopCard extends Component {
    constructor(props){
        super(props)
        this.state = { disableLikeButton: false, removeCard:null };
    }
    
    static propTypes = {
        likeShop: PropTypes.func.isRequired,
        dislikeShop: PropTypes.func.isRequired,
        liked: PropTypes.string,
        disliked: PropTypes.string
    };
    
    dislikeFunc(shop_id)
    {
        this.props.dislikeShop(shop_id, this.props.isFavoriteList);
    }
    
    likeFunc(shop_id)
    {
        if (this.props.isFavoriteList)
            this.props.likeShop(shop_id, true);
        else
            this.props.likeShop(shop_id, false);
    }
    
    componentWillReceiveProps(nextProps)
    {
        //console.log(nextProps);
        if(this.props.value.id==nextProps.liked)
            this.setState({disableLikeButton:true});
        
        if(this.props.value.id==nextProps.disliked)
            this.setState({removeCard:{display: "none"}});   
    }
    
    renderLikeButton(isFavorite, id)
    {
        // if the component is being rendred in the favorite list, no need to add a like button.
        if(!this.props.isFavoriteList){
            if(isFavorite)
                return (<Button bsStyle="primary" disabled>Like</Button>);
            return (<Button bsStyle="primary" disabled={this.state.disableLikeButton} onClick={()=> this.likeFunc(id)}>Like</Button>);
        }
        return null;
    }
    render()
    {
        const shop = this.props.value;
        return (
            <div style={this.state.removeCard}>
                <Thumbnail src={shop.picture} alt="Card image cap">
                    <h4 >Name: {shop.name}</h4>
                    <p >Email: {shop.email}</p>
                    <p >City: {shop.city}</p>                        
                    {" "}
                    <hr />
                    <Button bsStyle="danger" onClick={() => this.dislikeFunc(shop.id)}>{this.props.isFavoriteList?"Remove":"Dislike"}</Button>
                    {this.renderLikeButton(shop.is_favorite, shop.id)}
                </Thumbnail>
            </div>
        );
    }
}

function mapStateToProps(state) {
        return {
            liked: state.service.liked,
            disliked: state.service.disliked
        };
}

export default connect(mapStateToProps, { dislikeShop, likeShop  } )(ShopCard);