import React, { Component } from "react";
import PropTypes from "prop-types";
import { connect } from "react-redux";
import { Link } from "react-router-dom";
import { getShops, dislikeShop } from "../../actions/serviceActions";
import ShopCard from "./ShopCard";
import {Pager} from "react-bootstrap";

class NearbyShops extends Component {

    constructor(props){
        super(props)
        this.state={
            dislikeThisShop: Array(1).fill(true),
            pageNumber: 1
        };
    }
    
    static propTypes = {
        getShops: PropTypes.func.isRequired,
        shops: PropTypes.object,
        userLocation: PropTypes.object,
    };

    componentWillMount() {
        if (this.props.isFavoriteList)
            this.props.getShops(true, this.state.pageNumber);
        else
            this.props.getShops(false, this.state.pageNumber);
    }
    
    componentWillReceiveProps(nextProps){
        // the first time receiving props
        if(!this.props.userLocation && nextProps.userLocation)
            this.props.getShops(this.props.isFavoriteList, this.state.pageNumber)
        
        if (nextProps.userLocation && this.props.userLocation
        && nextProps.userLocation.lat !== this.props.userLocation.lat 
        && nextProps.userLocation.lng !== this.props.userLocation.lng) 
        {
            console.log(nextProps.userLocation)
            this.props.getShops(this.props.isFavoriteList, this.state.pageNumber)
        }
    }
    
    handlePrevious(){
        const minusOne = this.state.pageNumber - 1;
        this.setState({pageNumber: minusOne});
        this.props.getShops(this.props.isFavoriteList, minusOne);
    }
    
    handleNext(){
        const plusOne = this.state.pageNumber + 1
        this.setState({pageNumber: plusOne});
        this.props.getShops(this.props.isFavoriteList, plusOne)
    }
    
    renderShops() {
        const shops = this.props.shops;
        
        if (shops) {
            
            const listItems = shops.results.map( (shop) => <ShopCard key={shop.id} value={shop} isFavoriteList={this.props.isFavoriteList} /> )
            
            return listItems;
        }
        return null;
    }
    
    renderPagination(){
        let pages = []
        
        if (this.props.shops){
            if( this.props.shops.previous){
                pages.push(<Pager.Item key={1} previous onClick={()=> this.handlePrevious()}>&larr; Previous</Pager.Item>);
            }
            pages.push(<span key={2}> {this.state.pageNumber} </span>)
            if( this.props.shops.next){
                pages.push(<Pager.Item key={3} next onClick={()=> this.handleNext()}>Next &rarr;</Pager.Item>)
            }
        }
        if (pages)
            return <Pager> {pages} </Pager>;
    }

    render() {
        return ([
            <div key={1}>
            {this.renderShops()}
            </div>,
            <div key={2}>
            {this.renderPagination()}
            </div>]
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