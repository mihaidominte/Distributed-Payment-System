package com.client.paymentapp.auth

import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.lifecycle.lifecycleScope
import com.client.paymentapp.MainActivity
import kotlinx.coroutines.launch

class LauncherActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        lifecycleScope.launch {
            val hasUser = UserRepository.hasUser(this@LauncherActivity)
            val isAuthenticated = SessionManager.isAuthenticated()

            val intent = if (!hasUser || !isAuthenticated) {
                Intent(this@LauncherActivity, AuthActivity::class.java)
            } else {
                Intent(this@LauncherActivity, MainActivity::class.java)
            }

            startActivity(intent)
            finish()
        }
    }
}
