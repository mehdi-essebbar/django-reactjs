import React, { Component } from "react";
import PropTypes from "prop-types";
import { connect } from "react-redux";
import { Link } from "react-router-dom";
import { likeShop, dislikeShop } from "../../actions/serviceActions";


class ShopCard extends Component {
    constructor(props){
        super(props)
        this.state = { disableLikeButton: "", removeCard:null };
    }
    
    static propTypes = {
        likeShop: PropTypes.func.isRequired,
        dislikeShop: PropTypes.func.isRequired,
        liked: PropTypes.string,
        disliked: PropTypes.string
    };
    
    dislikeFunc(shop_id)
    {
        this.props.dislikeShop(shop_id);
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
            this.setState({disableLikeButton:" disabled"});
        
        if(this.props.value.id==nextProps.disliked)
            this.setState({removeCard:{display: "none"}});   
    }
    
    renderLikeButton(isFavoriteList, id)
    {
        // if the component is being rendred in the favorite list, no need to add a like button.
        if(!this.props.favoriteList){
            if(isFavoriteList>0)
                return (<button className="btn btn-primary disabled">Like</button>);
            return (<button className={"btn btn-primary"+this.state.disableLikeButton} onClick={()=> this.likeFunc(id)}>Like</button>);
        }
        return null
    }
    render()
    {
        const shop = this.props.value;
        return (
            <div className="card"  style={this.state.removeCard}>
                {/*<img className="card-img-top" src={shop.picture} alt="Card image cap"></img>*/}
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
            liked: state.service.liked,
            disliked: state.service.disliked
        };
}

export default connect(mapStateToProps, { dislikeShop, likeShop  } )(ShopCard);