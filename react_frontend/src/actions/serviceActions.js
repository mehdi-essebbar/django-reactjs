import axios from "axios";
import { SubmissionError } from 'redux-form';
import history from "../utils/historyUtils";
import { actions as notifActions } from 'redux-notifications';
const { notifSend } = notifActions;

import { ServiceTypes } from "../constants/actionTypes";
import { ServiceUrls } from "../constants/urls";
import store from "../store";
import { getUserToken } from "../utils/authUtils";


function setShop(payload) {
    return {
        type: ServiceTypes.SHOPS,
        payload: payload
    };
}

export function getShops(isFavoriteList) {
    return function(dispatch) {
        let url = "";
        if (isFavoriteList)
            url = ServiceUrls.FAVORITE_SHOPS;
        else
            url = ServiceUrls.SHOPS;
        
        const token = getUserToken(store.getState());
        if (token) {
            axios.get(url, {
                headers: {
                    authorization: 'Token ' + token
                }
            }).then(response => {
                dispatch(setShop(response.data))
            }).catch((error) => {
                // If request is bad...
                // Show an error to the user
                console.log(error);
                // TODO: send notification and redirect
            });
        }
    };
}

function setLiked(payload) {
    return {
        type: ServiceTypes.LIKED,
        payload: payload
    };
}

export function likeShop(shop_id) {
    return function(dispatch) {
        const token = getUserToken(store.getState());
        if (token) {
            axios.post(ServiceUrls.FAVORITE_SHOPS, { id: shop_id }, {
                headers: {
                    authorization: 'Token ' + token
                }
            }).then(response => {
                dispatch(setLiked(shop_id));
                //console.log(response.data);
                
            }).catch((error) => {
                // If request is bad...
                // Show an error to the user
                console.log(error);
                // TODO: send notification and redirect
                //dispatch(setLiked(false));
            });
        }
    };
}

function setDisliked(payload) {
    return {
        type: ServiceTypes.DISLIKED,
        payload: payload
    };
}

export function dislikeShop(shop_id, isFavoriteList) {
    return function(dispatch) {
        let url = "";
        let method = "";
        if (isFavoriteList){
            url = ServiceUrls.FAVORITE_SHOPS;
            method = 'delete';
        }
        else{
            method = 'post';
            url = ServiceUrls.DISLIKE_SHOP;
        }
        
        const token = getUserToken(store.getState());
        if (token) {
            axios({ method: method, 
                    url: url,
                    headers: {
                        authorization: 'Token ' + token
                    },
                    data:{ id: shop_id }
            }).then(response => {
                dispatch(setDisliked(shop_id));
                //console.log(response.data);
                
            }).catch((error) => {
                // If request is bad...
                // Show an error to the user
                console.log(error);
                // TODO: send notification and redirect
                //dispatch(setDisliked(false));
            });
        }
    };
}