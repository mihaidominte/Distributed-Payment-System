package com.client.paymentapp.auth

import android.content.Context

object SessionManager {

    private const val PREFS_NAME = "session_prefs"
    private const val KEY_AUTH = "authenticated"

    fun authenticate(context: Context) {
        val prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
        prefs.edit().putBoolean(KEY_AUTH, true).apply()
    }

    fun logout(context: Context) {
        val prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
        prefs.edit().clear().apply()
    }

    fun isAuthenticated(context: Context): Boolean {
        val prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
        return prefs.getBoolean(KEY_AUTH, false)
    }
}
