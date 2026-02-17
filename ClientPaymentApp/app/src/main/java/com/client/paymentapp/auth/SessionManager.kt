package com.client.paymentapp.auth

object SessionManager {

    private var authenticated = false

    fun authenticate() {
        authenticated = true
    }

    fun logout() {
        authenticated = false
    }

    fun isAuthenticated(): Boolean {
        return authenticated
    }
}
