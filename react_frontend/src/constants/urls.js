const ROOT_URL = "http://localhost:8000/";

export const AuthUrls = {
    LOGIN: `${ROOT_URL}rest-auth/login/`,
    LOGOUT: `${ROOT_URL}rest-auth/logout/`,
    SIGNUP: `${ROOT_URL}rest-auth/registration/`,
    CHANGE_PASSWORD: `${ROOT_URL}rest-auth/password/change/`,
    RESET_PASSWORD: `${ROOT_URL}rest-auth/password/reset/`,
    RESET_PASSWORD_CONFIRM: `${ROOT_URL}rest-auth/password/reset/confirm/`,
    USER_ACTIVATION: `${ROOT_URL}rest-auth/registration/verify-email/`,
    USER_PROFILE: `${ROOT_URL}rest-auth/user/`,
};

export const ServiceUrls = {
    SHOPS: `${ROOT_URL}shops/`,
    FAVORITE_SHOPS: `${ROOT_URL}shops/favorite/`,
    DISLIKE_SHOP: `${ROOT_URL}shops/dislike/`,
};