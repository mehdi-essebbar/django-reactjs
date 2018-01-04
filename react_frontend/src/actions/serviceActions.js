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
