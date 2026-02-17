package com.client.paymentapp.auth

import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.lifecycle.lifecycleScope
import com.client.paymentapp.MainActivity
import kotlinx.coroutines.launch

class AuthActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContent {
            MaterialTheme {
                AuthScreen(
                    onSuccess = {
                        SessionManager.authenticate()
                        startActivity(Intent(this, MainActivity::class.java))
                        finish()
                    }
                )
            }
        }
    }

    @Composable
    fun AuthScreen(
        onSuccess: () -> Unit
    ) {
        var password by remember { mutableStateOf("") }
        var status by remember { mutableStateOf("") }
        var hasUser by remember { mutableStateOf<Boolean?>(null) }
        var loading by remember { mutableStateOf(false) }

        LaunchedEffect(Unit) {
            hasUser = UserRepository.hasUser(applicationContext)
        }

        if (hasUser == null) {
            Box(
                modifier = Modifier.fillMaxSize(),
                contentAlignment = Alignment.Center
            ) {
                CircularProgressIndicator()
            }
            return
        }

        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(24.dp),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {

            Text(
                text = if (hasUser == true) "Autentificare" else "Creare cont",
                style = MaterialTheme.typography.headlineMedium
            )

            Spacer(modifier = Modifier.height(16.dp))

            OutlinedTextField(
                value = password,
                onValueChange = { password = it },
                label = { Text("Parolă") },
                visualTransformation = PasswordVisualTransformation(),
                enabled = !loading
            )

            Spacer(modifier = Modifier.height(16.dp))

            Button(
                enabled = !loading && password.isNotBlank(),
                onClick = {

                    lifecycleScope.launch {
                        loading = true
                        status = ""
                        try {
                            val result = kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.IO){
                                if (hasUser == true) {
                                    UserRepository.login(
                                        context = applicationContext,
                                        password = password
                                    )
                                } else {
                                    UserRepository.createUser(
                                        context = applicationContext,
                                        password = password
                                    )
                                    true
                                }
                            }
                            if (result) {
                                onSuccess()
                            } else {
                                status = "Parolă incorectă"
                            }

                        } catch (e: Exception) {
                            status = "Eroare: ${e.message}"
                        } finally {
                            loading = false
                        }
                    }
                }
            ) {
                Text(if (hasUser == true) "Login" else "Creează cont")
            }

            Spacer(modifier = Modifier.height(16.dp))

            TextButton(
                onClick = {
                    loading = true
                    lifecycleScope.launch {
                        try {
                            UserRepository.deleteUser(applicationContext)
                            SessionManager.logout()

                            recreate()
                        } finally {
                            loading = false
                        }
                    }
                }
            ) {
                Text("Reset cont (test)")
            }


            Spacer(modifier = Modifier.height(12.dp))

            if (loading) {
                CircularProgressIndicator(modifier = Modifier.size(24.dp))
            }

            if (status.isNotBlank()) {
                Spacer(modifier = Modifier.height(8.dp))
                Text(status, color = MaterialTheme.colorScheme.error)
            }
        }
    }
}
