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

export function getShop() {
    return function(dispatch) {
        const token = getUserToken(store.getState());
        if (token) {
            axios.get(ServiceUrls.SHOPS, {
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
            axios.post(ServiceUrls.FAVORITE_SHOP, { id: shop_id }, {
                headers: {
                    authorization: 'Token ' + token
                }
            }).then(response => {
                dispatch(setLiked(true));
                console.log(response.data);
                
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

export function dislikeShop(shop_id, k) {
    return function(dispatch) {
        const token = getUserToken(store.getState());
        if (token) {
            axios.post(ServiceUrls.DISLIKE_SHOP, { id: shop_id }, {
                headers: {
                    authorization: 'Token ' + token
                }
            }).then(response => {
                dispatch(setDisliked(k));
                console.log(response.data);
                
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