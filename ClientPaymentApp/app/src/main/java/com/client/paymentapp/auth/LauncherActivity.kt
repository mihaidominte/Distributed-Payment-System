package com.client.paymentapp.auth

import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import com.client.paymentapp.MainActivity

class LauncherActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val hasUser = UserRepository.hasUser(this)
        val isAuthenticated = SessionManager.isAuthenticated(this)

        val intent = if (!hasUser || !isAuthenticated) {
            Intent(this, AuthActivity::class.java)
        } else {
            Intent(this, MainActivity::class.java)
        }


        startActivity(intent)
        finish()
    }
}