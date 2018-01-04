import React, { Component } from "react";
import PropTypes from "prop-types";
import { connect } from "react-redux";
import { Link } from "react-router-dom";
import { getShop } from "../../actions/serviceActions";

class NearbyShops extends Component {

    static propTypes = {
        getShop: PropTypes.func.isRequired,
        shops: PropTypes.object
    };

    componentWillMount() {
        this.props.getShop();
    }

    renderShop() {
        const shops = this.props.shops;
        console.log(shops);
        if (shops) {
            var rows = [];
            for(var i = 0; i<shops.length; i++){
                rows.push(<div className="card">
                    <img className="card-img-top" src="http://via.placeholder.com/350x150" alt="Card image cap"></img>
                    <div className="card-block">
                        <h4>Name: {shops[i].name}</h4>
                        <h4>Description: {shops[i].description}</h4>
                        <h4>Picture: {shops[i].picture}</h4>
                        {" "}
                        <hr />
                        <Link className="btn btn-primary mr-2" to={"/dislike/" + shops[i].id}>Dislike</Link>
                        <Link className="btn btn-primary" to={"/like/"+shops[i].id}>Like</Link>
                    </div>
                </div>)
            }
            
            return rows;
        }
        return null;
    }

    render() {
        return (
            <div>
            {this.renderShop()}
                
            </div>
        );
    }
}

function mapStateToProps(state) {
    return {
        shops: state.auth.shops
    }
}

export default connect(mapStateToProps, { getShop } )(NearbyShops);