package com.client.paymentapp

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.lifecycle.lifecycleScope
import com.client.paymentapp.network.Client
import kotlinx.coroutines.launch
import org.json.JSONObject

class SendMoneyActivity : ComponentActivity() {
    val client = Client()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        lifecycleScope.launch {
            client.connect()
        }

        setContent {
            MaterialTheme {
                SendMoneyScreen()
            }
        }
    }

    @Composable
    fun SendMoneyScreen() {
        var receiverId by remember { mutableStateOf("") }
        var amount by remember { mutableStateOf("") }
        var status by remember { mutableStateOf("") }

        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text("Send Money", style = MaterialTheme.typography.headlineMedium)

            Spacer(modifier = Modifier.height(16.dp))

            OutlinedTextField(
                value = receiverId,
                onValueChange = { receiverId = it },
                label = { Text("Receiver ID") }
            )

            Spacer(modifier = Modifier.height(8.dp))

            TextField(
                value = amount,
                onValueChange = { amount = it },
                label = { Text("Sumă de trimis") },
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number)
            )

            Spacer(modifier = Modifier.height(16.dp))

            Button(onClick = {
                val receiver = receiverId.toIntOrNull()
                val amt = amount.toDoubleOrNull()
                if (receiver != null && amt != null) {
                    lifecycleScope.launch {
                        val success = sendMoneyOnline(receiver, amt)
                        status = if (success) "Transaction Success" else "Transaction Failed"
                    }
                } else {
                    status = "Invalid input"
                }
            }) {
                Text("Send Money")
            }

            Spacer(modifier = Modifier.height(16.dp))
            Text(status)
        }
    }

    private suspend fun sendMoneyOnline(receiverId: Int, amount: Double): Boolean {
        val message = JSONObject()
        message.put("activity", "send_money")
        message.put("id", 1)
        message.put("sender_id", 1)
        message.put("receiver_id", receiverId)
        message.put("amount", amount)

        val response = client.sendAndWait(message)

        return response.getString("activity") == "success"
    }

    override fun onDestroy() {
        super.onDestroy()
        client.disconnect()
    }
}