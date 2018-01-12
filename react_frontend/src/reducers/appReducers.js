import { AuthTypes, ServiceTypes } from "../constants/actionTypes";

export function authReducer(state = {}, action) {
    switch(action.type) {
        case AuthTypes.LOGIN:
            return { ...state, authenticated: true, token: action.payload};
        case AuthTypes.LOGOUT:
            return { ...state, authenticated: false, token: null};
        case AuthTypes.USER_PROFILE:
            return { ...state, user: action.payload};
    }
    return state;
}

export function serviceReducer(state = {}, action) {
    switch(action.type) {
        case ServiceTypes.SHOPS:
            return { ...state, shops: action.payload};
        case ServiceTypes.LIKED:
            return { ...state, liked: action.payload};
        case ServiceTypes.DISLIKED:
            return { ...state, disliked: action.payload};
        case ServiceTypes.LOCATION:
            return { ...state, userLocation: action.payload};
    }
    return state;
}