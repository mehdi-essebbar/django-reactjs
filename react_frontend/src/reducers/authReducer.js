import { AuthTypes } from "../constants/actionTypes";
import { ServiceTypes } from "../constants/actionTypes";


export default function(state = {}, action) {
    switch(action.type) {
        case AuthTypes.LOGIN:
            return { ...state, authenticated: true, token: action.payload};
        case AuthTypes.LOGOUT:
            return { ...state, authenticated: false, token: null};
        case AuthTypes.USER_PROFILE:
            return { ...state, user: action.payload};
        case ServiceTypes.SHOPS:
            return { ...state, shops: action.payload};
    }
    return state;
}