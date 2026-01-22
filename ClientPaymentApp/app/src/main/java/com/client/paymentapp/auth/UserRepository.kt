package com.client.paymentapp.auth

import android.content.Context

object UserRepository {

    fun hasUser(context: Context): Boolean {
        // TEMPORAR: SharedPreferences / Room / file
        val prefs = context.getSharedPreferences("user_prefs", Context.MODE_PRIVATE)
        return prefs.contains("user_id")
    }
}
