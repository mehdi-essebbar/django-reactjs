import React, { Component } from "react";
import PropTypes from "prop-types";
import { Link } from "react-router-dom";
import { connect } from "react-redux";
import CaptureUserLocation from "./services/CaptureUserLocation";
import {Nav, Navbar, NavItem } from "react-bootstrap";

class Header extends Component {

    static propTypes = {
        authenticated: PropTypes.bool
    };

    renderLinks() {
        if (this.props.authenticated) {
            return (
                [<Nav key={1}>
                    <NavItem key={1} componentClass={Link} href="/shops/nearby" to="/shops/nearby">
                        Nearby Shops
                    </NavItem>
                    <NavItem key={2} componentClass={Link} href="/shops/favorite" to="/shops/favorite">
                        My Favorite Shops
                    </NavItem>
                    <NavItem key={3} componentClass={Link} href="/profile" to="/profile">
                        Profile
                    </NavItem>
                    <NavItem key={4} componentClass={Link} href="/logout" to="/logout">
                        Logout
                    </NavItem>
                </Nav>,
                <Nav key={2} pullRight>
                    <NavItem >
                        <CaptureUserLocation />
                    </NavItem>
                </Nav>]
            );

        } else {
            return (
                
                <Nav>
                    <NavItem key={1} componentClass={Link} href="/login" to="/login">
                        Login
                    </NavItem>
                    <NavItem key={2} componentClass={Link} href="/signup" to="/signup">
                        Sign Up
                    </NavItem>
                </Nav>
                
            );
        }
    }

    render() {
        return (
            <Navbar>
                <Navbar.Header>
                    <Navbar.Brand>
                        <Link to="/">Demo Shops</Link>
                    </Navbar.Brand>
                </Navbar.Header>
                {this.renderLinks()}
            </Navbar>
        )
    }
}

function mapStateToProps(state) {
    return {
        authenticated: state.auth.authenticated
    }
}
export default connect(mapStateToProps)(Header);